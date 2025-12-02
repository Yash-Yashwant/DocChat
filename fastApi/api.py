from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from google.cloud import storage

# Add parent directory to path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion import ingest_pdf
from src.graph import graph

app = FastAPI(title="DocChat API", version="1.0.0")

# Add CORS middleware so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow ALL origins for demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GCS Configuration
GCS_BUCKET_NAME = "pdf-drop"  # Your bucket name
GCS_PROJECT_ID = "do-c-479403"

# Initialize GCS client (will automatically use gcloud auth credentials)
storage_client = storage.Client(project=GCS_PROJECT_ID)
bucket = storage_client.bucket(GCS_BUCKET_NAME)

# Define request/response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "DocChat API is running"}


@app.post("/upload")
async def upload_files(file: UploadFile = File(...)):
    """Upload and process a PDF document to GCS"""
    # validate its a pdf 
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Read file content
        content = await file.read()
        print(f"[DEBUG] File read successfully: {file.filename}, size: {len(content)} bytes")
        
        # Upload to GCS
        blob = bucket.blob(f"pdfs/{file.filename}")
        print(f"[DEBUG] Uploading to GCS: gs://{GCS_BUCKET_NAME}/pdfs/{file.filename}")
        blob.upload_from_string(content, content_type="application/pdf")
        print(f"[DEBUG] Upload to GCS successful")
        
        # Get the GCS URI
        gcs_uri = f"gs://{GCS_BUCKET_NAME}/pdfs/{file.filename}"
        
        # Download to temp location for processing
        temp_path = f"/tmp/{file.filename}"
        print(f"[DEBUG] Downloading to temp: {temp_path}")
        blob.download_to_filename(temp_path)
        print(f"[DEBUG] Download successful")
        
        # Process the PDF through your ingestion pipeline
        print(f"[DEBUG] Starting ingestion...")
        ingest_pdf(temp_path)
        print(f"[DEBUG] Ingestion complete")
        
        # Clean up temp file
        os.remove(temp_path)
        
        return {
            "message": "File uploaded and processed successfully!",
            "filename": file.filename,
            "gcs_uri": gcs_uri
        }
    except Exception as e:
        print(f"[ERROR] Upload failed: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")




@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message using the RAG pipeline"""
    try:
        # Run the LangGraph agent
        result = None
        for step in graph.stream(
            {"messages": [{"role": "user", "content": request.message}]},
            stream_mode="values",
        ):
            # Get the last message (the AI's response)
            result = step["messages"][-1]
        
        # Extract the text content from the AI message
        if hasattr(result, 'content'):
            response_text = result.content
        else:
            response_text = str(result)
        
        return ChatResponse(response=response_text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")
    