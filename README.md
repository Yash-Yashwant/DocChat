# DocChat - Complete Setup Guide

## What's Been Built

Your DocChat application is now fully functional with:

1. **Frontend (React)** - Modern UI with drag-and-drop upload and chat
2. **Backend (FastAPI)** - REST API connected to your RAG pipeline
3. **RAG Pipeline** - PDF ingestion and Q&A using Gemini + Pinecone

---

## How to Run

### Terminal 1: Start the Backend API

```bash
cd /home/yaga23/Documents/DocChat/DocChat
conda activate datacenter
python3 -m uvicorn fastApi.api:app --reload --port 8000
```

You should see: `INFO: Application startup complete`

### Terminal 2: Start the Frontend

```bash
cd /home/yaga23/Documents/DocChat/DocChat/frontend
npm run dev
```

You should see: `Local: http://localhost:5173/`

---

## How to Use

1. **Open your browser** to `http://localhost:5173`
2. **Upload a PDF**:
   - Drag and drop or click "Browse Files"
   - Wait for "File uploaded and processed successfully!"
3. **Ask questions**:
   - Type your question in the chat
   - The AI will answer based on your uploaded documents

---

## What Each Part Does

### Backend API (`fastApi/api.py`)
- `POST /upload` - Receives PDFs, saves them, calls `src/ingestion.py` to process into Pinecone
- `POST /chat` - Receives questions, calls `src/graph.py` (LangGraph agent) to generate answers

### Frontend (`frontend/src/`)
- `FileUpload.jsx` - Handles PDF uploads, sends to `/upload` endpoint
- `ChatInterface.jsx` - Handles chat messages, sends to `/chat` endpoint
- `App.jsx` - Main layout with gradient background

### RAG Pipeline (`src/`)
- `config.py` - API keys and settings
- `ingestion.py` - PDF → chunks → embeddings → Pinecone
- `retrieval.py` - Search Pinecone for relevant chunks
- `graph.py` - LangGraph agent that retrieves + generates answers

---

## Troubleshooting

**Backend won't start?**
- Make sure you're in the `DocChat` directory (not `fastApi`)
- Activate conda: `conda activate datacenter`

**Frontend won't start?**
- Make sure you're in the `frontend` directory
- Run `npm install` if needed

**Upload fails?**
- Check that backend is running on port 8000
- Check browser console for errors

**Chat doesn't work?**
- Make sure you've uploaded a document first
- Check that your `.env` file has `GOOGLE_API_KEY` and `PINECONE_API_KEY`

---

## Project Structure

```
DocChat/
├── fastApi/
│   └── api.py              # FastAPI backend
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx
│   │   │   └── ChatInterface.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
├── src/
│   ├── config.py
│   ├── ingestion.py
│   ├── retrieval.py
│   └── graph.py
├── .env                    # API keys (create this!)
└── requirements.txt
```

---

## Next Steps (Optional)

1. **GCS Integration** - Upload PDFs to Google Cloud Storage
2. **User Authentication** - Add login/signup
3. **Deploy** - Deploy to Google Cloud E2 VM
4. **Citations** - Show which page/section the answer came from

---

## Environment Variables

Make sure your `.env` file contains:

```
GOOGLE_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
```

---

**You're all set!**
