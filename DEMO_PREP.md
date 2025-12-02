# DocChat Demo & Walkthrough Script

Use this guide to record your video. It covers the application flow, code structure, and the technical challenges you solved.

---

## 🎬 Part 1: Application Demo (The "Wow" Factor)

**Goal:** Show what the app does before explaining how it works.

1. **Opening:** "Hi, this is [Your Name], and this is **DocChat**. It's a RAG (Retrieval-Augmented Generation) application that lets you chat with your PDF documents using AI."
2. **The Flow:**
    * **Upload:** "First, I'll upload a lecture slide/PDF." (Drag and drop a file).
    * **Processing:** "Behind the scenes, this is being uploaded to Google Cloud Storage, processed into text chunks, and stored in a Pinecone vector database."
    * **Chat:** "Now that it's processed, I can ask questions." (Ask: *"What is the main topic of this lecture?"*).
    * **Response:** Show the AI response appearing.

---

## 💻 Part 2: Code & Architecture Walkthrough

**Goal:** Briefly explain the tech stack.

1. **Architecture Diagram:** (Open `ARCHITECTURE.md` if you have it rendered, or just explain).
    * "The app has a **React Frontend** (hosted on Vercel) and a **FastAPI Backend** (hosted on a Google Cloud VM)."
    * "We use **Google Cloud Storage** for files, **Gemini** for AI embeddings, and **Pinecone** for vector search."

2. **Frontend (`frontend/src`):**
    * "The frontend is built with React and Tailwind CSS. It handles the file upload and chat interface."

3. **Backend (`fastApi/api.py`):**
    * "The backend is FastAPI. It has endpoints for `/upload` and `/chat`."
    * "It connects to our RAG pipeline."

4. **RAG Pipeline (`src/`):**
    * "This is the core logic. `ingestion.py` handles breaking down the PDF, and `graph.py` uses LangGraph to manage the conversation flow."

---

## 🛠️ Part 3: Challenges & Debugging (The "Engineering" Part)

**Goal:** Show that you can solve complex deployment issues. **This is the most important part for your evaluation.**

"Building this wasn't just about writing code; deployment came with several real-world challenges:"

### 1. The "Mixed Content" Security Issue

* **The Problem:** "My frontend is hosted on Vercel, which forces **HTTPS** (Secure). My backend was on a Google Cloud VM using a raw IP address, which is **HTTP** (Not Secure)."
* **The Error:** "Browsers block this connection for security reasons. You cannot make an insecure HTTP request from a secure HTTPS page. I kept getting `Failed to fetch` errors."

### 2. The Static IP Problem

* **The Problem:** "Every time I restarted my Google Cloud VM, the external IP address changed. This broke the connection to Vercel."
* **The Solution:** "I learned I needed to reserve a **Static External IP** in GCP so the address stays permanent."

### 3. The HTTPS Solution (Cloudflare Tunnel)

* **The Challenge:** "To fix the Mixed Content error, I needed HTTPS on my backend. Usually, this requires buying a domain, configuring DNS, and setting up SSL certificates (Let's Encrypt), which is complex for a quick demo."
* **The Fix:** "I used **Cloudflare Tunnel**. It allowed me to create a secure, encrypted tunnel from my VM directly to the public internet."
  * *Show the command:* `cloudflared tunnel --url http://localhost:8000`
  * "This instantly gave me a secure `https://...trycloudflare.com` URL, which satisfied the browser's security requirements and allowed the Vercel frontend to talk to the backend."

---

## 🎯 Conclusion

"In summary, DocChat is a full-stack RAG application that integrates modern AI tools with a robust cloud deployment, overcoming real-world security and networking challenges."
