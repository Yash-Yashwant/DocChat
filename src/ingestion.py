import os
from langchain_community.document_loaders import PDFMinerLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from src.config import settings

def get_embeddings():
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    return GoogleGenerativeAIEmbeddings(model=settings.EMBEDDING_MODEL, google_api_key=settings.GOOGLE_API_KEY)

def init_pinecone_index():
    if not settings.PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY not found in environment variables")
    
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    
    if not pc.has_index(settings.PINECONE_INDEX_NAME):
        print(f"Creating index: {settings.PINECONE_INDEX_NAME}")
        pc.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=768, 
            metric="dotproduct",
            spec=ServerlessSpec(
                cloud=settings.PINECONE_CLOUD,
                region=settings.PINECONE_REGION
            )
        )
    return pc.Index(settings.PINECONE_INDEX_NAME)

def ingest_pdf(file_path: str):
    print(f"Loading PDF: {file_path}")
    loader = PDFMinerLoader(file_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"Split into {len(splits)} chunks")
    
    embeddings = get_embeddings()
    index = init_pinecone_index()
    
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    vector_store.add_documents(documents=splits)
    print("Ingestion complete!")
