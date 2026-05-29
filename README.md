# SRMTEAMROBOCON-AI

RAG chatbot with a Vite frontend and a FastAPI backend.

## Vercel-only deployment

This repo is set up for a single Vercel project using Services:

- `frontend/rag` is the web service mounted at `/`
- `backend/main.py` is the API service mounted at `/api`

The routing is defined in [`vercel.json`](vercel.json).

## What changed for Vercel

- The frontend now defaults to the same-origin API path `/api`
- The backend exposes both `/query` and `/api/query`
- Model loading in the backend is lazy so cold starts are a little less painful

## Important caveat

This is still a heavy Python backend because it uses:

- `sentence-transformers`
- `torch`
- `chromadb`
- `groq`

That means a Vercel-only deployment is an experiment, not the most reliable production choice.

## Local development

Frontend:

```bash
cd frontend/rag
npm install
npm run dev
```

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

If you run locally, set the frontend API URL to your backend:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

## Vercel deployment

1. Import the GitHub repo into Vercel.
2. Set the project framework preset to `Services`.
3. Deploy with `vercel.json` at the repo root.
4. Add the `groq_api_key` environment variable in Vercel.

## API

- `GET /api/health`
- `POST /api/query`

The frontend sends chat requests to `/api/query`.
