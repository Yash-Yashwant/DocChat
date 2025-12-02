# DocChat - Complete Setup Guide

## What's Been Built

Your DocChat application is now fully functional with:

1. **Frontend (React)** - Modern UI with drag-and-drop upload and chat
2. **Backend (FastAPI)** - REST API connected to your RAG pipeline
3. **RAG Pipeline** - PDF ingestion and Q&A using Gemini + Pinecone

---

## Live Demo

**Frontend:** [https://doc-chat-one.vercel.app](https://doc-chat-one.vercel.app)

The application is fully deployed!

- **Frontend:** Hosted on Vercel
- **Backend:** Hosted on Google Cloud VM
- **Database:** Pinecone & Google Cloud Storage

---

## How to Use

1. **Open your browser** to [https://doc-chat-one.vercel.app](https://doc-chat-one.vercel.app)
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

---

## Deployment

### Deploy Frontend to Vercel

The frontend is configured for easy deployment to Vercel:

#### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push to GitHub**:

   ```bash
   cd /home/yaga23/Documents/DocChat/DocChat
   git add .
   git commit -m "Configure for Vercel deployment"
   git push
   ```

2. **Import to Vercel**:
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "Add New Project"
   - Import your GitHub repository
   - Set the **Root Directory** to `frontend`
   - Vercel will auto-detect the Vite configuration

3. **Configure Environment Variable**:
   - In the Vercel project settings, go to "Environment Variables"
   - Add: `VITE_API_URL` = `your-backend-url` (e.g., `https://your-api.com`)
   - Click "Deploy"

#### Option 2: Deploy via Vercel CLI

```bash
cd /home/yaga23/Documents/DocChat/DocChat/frontend
npm install -g vercel
vercel login
vercel --prod
```

When prompted, set the environment variable:

- `VITE_API_URL`: Your backend API URL

#### Important Notes

- **Backend CORS**: Your FastAPI backend must allow requests from your Vercel domain
- **Environment Variables**: The frontend uses `VITE_API_URL` to connect to your backend
- **Local Development**: Without `.env` file, it defaults to `http://localhost:8000`

---

---

### Deploy Backend to GCP VM

Deploy your FastAPI backend to a Google Cloud E2 VM instance.

#### Step 1: Create a GCP VM Instance

1. **Go to Google Cloud Console**:
   - Navigate to [console.cloud.google.com](https://console.cloud.google.com)
   - Select your project: `do-c-479403`

2. **Create VM Instance**:
   - Go to **Compute Engine** → **VM instances**
   - Click **"Create Instance"**
   - Configure:
     - **Name**: `docchat-backend`
     - **Region**: Choose closest to your users (e.g., `us-central1`)
     - **Machine type**: `e2-medium` (2 vCPU, 4 GB memory)
     - **Boot disk**: Ubuntu 22.04 LTS, 20 GB
     - **Firewall**: Check "Allow HTTP traffic" and "Allow HTTPS traffic"
   - Click **"Create"**

3. **Configure Firewall Rule for Port 8000**:
   - Go to **VPC Network** → **Firewall**
   - Click **"Create Firewall Rule"**
   - Name: `allow-fastapi`
   - Targets: All instances in the network
   - Source IP ranges: `0.0.0.0/0`
   - Protocols and ports: `tcp:8000`
   - Click **"Create"**

#### Step 2: SSH into VM and Deploy

1. **SSH into your VM**:

   ```bash
   gcloud compute ssh docchat-backend --zone=us-central1-a
   ```

2. **Clone your repository**:

   ```bash
   cd ~
   git clone https://github.com/Yash-Yashwant/DocChat.git
   cd DocChat
   ```

3. **Run the startup script**:

   ```bash
   chmod +x startup.sh
   ./startup.sh
   ```

4. **Set up environment variables**:

   ```bash
   cp .env.example .env
   nano .env
   ```

   Add your actual API keys:

   ```
   GOOGLE_API_KEY=your_actual_google_api_key
   PINECONE_API_KEY=your_actual_pinecone_api_key
   GOOGLE_APPLICATION_CREDENTIALS=/home/your-username/.config/gcloud/application_default_credentials.json
   ```

5. **Authenticate with Google Cloud** (for GCS access):

   ```bash
   gcloud auth application-default login
   ```

#### Step 3: Set Up Systemd Service

1. **Copy service file**:

   ```bash
   sudo cp docchat.service /etc/systemd/system/
   ```

2. **Update service file with your username**:

   ```bash
   sudo nano /etc/systemd/system/docchat.service
   ```

   Replace `yaga23` with your actual username (run `whoami` to check)

3. **Enable and start the service**:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable docchat
   sudo systemctl start docchat
   ```

4. **Check service status**:

   ```bash
   sudo systemctl status docchat
   ```

#### Step 4: Get Your Backend URL

1. **Find your VM's external IP**:

   ```bash
   gcloud compute instances list
   ```

   Or check in the GCP Console under VM instances

2. **Your backend URL**: `http://YOUR_VM_EXTERNAL_IP:8000`

3. **Test it**:

   ```bash
   curl http://YOUR_VM_EXTERNAL_IP:8000/
   ```

   Should return: `{"message":"DocChat API is running"}`

#### Step 5: Set Up HTTPS with Cloudflare Tunnel (Recommended)

Since Vercel uses HTTPS, your backend must also use HTTPS to avoid "Mixed Content" errors. The easiest way is using Cloudflare Tunnel.

1. **Install Cloudflared on your VM**:

   ```bash
   wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && sudo dpkg -i cloudflared-linux-amd64.deb
   ```

2. **Start the Tunnel**:

   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```

3. **Get your HTTPS URL**:
   - Copy the URL from the output (e.g., `https://random-name.trycloudflare.com`)
   - **Keep this terminal window open!**

#### Step 6: Update Vercel Environment Variable

1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Update `VITE_API_URL` to your Cloudflare URL: `https://your-tunnel-url.trycloudflare.com`
4. Redeploy your frontend

#### Service Management Commands

```bash
# Start service
sudo systemctl start docchat

# Stop service
sudo systemctl stop docchat

# Restart service
sudo systemctl restart docchat

# View logs
sudo journalctl -u docchat -f

# Check status
sudo systemctl status docchat
```

---

## Next Steps (Optional)

1. **Permanent Tunnel** - Configure Cloudflare Tunnel to run as a service
2. **User Authentication** - Add login/signup
3. **Citations** - Show which page/section the answer came from

---

## Environment Variables

Make sure your `.env` file contains:

```
GOOGLE_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
```

---

**You're all set!**
