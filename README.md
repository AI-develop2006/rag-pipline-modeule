# Acme QuantumWidget RAG Application

A full-stack Retrieval-Augmented Generation (RAG) system with a FastAPI backend and a Next.js (App Router) frontend, integrated with Google's Gemini API (`gemini-1.5-flash`) for deterministic document-based question-answering.

## Project Architecture

```
my-rag-app/
├── backend/
│   ├── main.py              # FastAPI application server
│   ├── requirements.txt     # Python backend dependencies
│   └── knowledge_base.txt   # Mock internal text data file for the RAG pipeline
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx   # Next.js global layout
│   │   │   ├── page.tsx     # Clean chat interface styled with Tailwind CSS
│   │   │   └── api/chat/
│   │   │       └── route.ts # API Route handler to proxy requests to backend
│   ├── package.json         # Frontend dependencies
│   ├── postcss.config.mjs
│   └── tailwind.config.ts
├── .env                     # Backend Environment variables
└── .env.local               # Frontend Environment variables
```

---

## Getting Started (Local Development)

### 1. Prerequisites
- Python 3.9+
- Node.js 18.x or later
- A Google Gemini API Key. You can get one from the [Google AI Studio](https://aistudio.google.com/).

### 2. Environment Variables Configuration
1. Open the root directory environment file: `.env`
2. Change the placeholder to your actual Gemini key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   PORT=8000
   ```
3. Open `.env.local` to verify the frontend refers to the backend server:
   ```env
   BACKEND_API_URL=http://localhost:8000
   ```

### 3. Running the Python Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment (recommended):
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server using Uvicorn:
   ```bash
   python main.py
   ```
   The backend server should now be running at `http://localhost:8000`.

### 4. Running the Next.js Frontend
1. Open a new terminal window/tab and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node packages:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   The frontend app will launch at `http://localhost:3000`. Open it in your web browser to test.

---

## Deployment Instructions

### 1. Backend Deployment (Render, Railway, or Google Cloud Run)
To serve production requests, deploy the Python backend as an independent container service.

#### Option A: Railway (Recommended)
1. Log in to [Railway](https://railway.app/).
2. Click **New Project** -> **Deploy from GitHub repo** and select your repository.
3. In the settings, ensure root directory is set to `backend`.
4. Add the environment variables:
   - `GEMINI_API_KEY`: `your_actual_api_key`
   - `PORT`: `8080` (Railway will assign this automatically, or you can override it).
5. Copy the generated Public URL (e.g., `https://backend-production-xyz.up.railway.app`).

---

### 2. Frontend Deployment (Vercel)
Deploy the Next.js frontend directly to Vercel and link it to your live backend.

1. Log in to [Vercel](https://vercel.com/).
2. Select **Add New...** -> **Project** and import your repository.
3. Under **Framework Preset**, select **Next.js**.
4. Set the **Root Directory** to `frontend`.
5. Under **Environment Variables**, add:
   - `BACKEND_API_URL`: Set this to your deployed backend service's URL (e.g., `https://backend-production-xyz.up.railway.app`). Do NOT include a trailing slash.
6. Click **Deploy**.
