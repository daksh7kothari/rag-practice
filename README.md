# SRMTEAMROBOCON-AI

RAG chatbot with a Vite frontend and a FastAPI backend.

## Deployment Paths

This repo supports two paths:

- Vercel Services for the frontend + backend experiment
- Render for the lightweight backend test deploy

For the Vercel path:
- `frontend/rag` is the web service mounted at `/`
- `backend/main.py` is the API service mounted at `/api`

The routing is defined in [`vercel.json`](vercel.json).

## What changed for Vercel

- The frontend now defaults to the same-origin API path `/api`
- The backend exposes both `/query` and `/api/query`
- The backend retrieves answers from PDF chunks stored in a persistent Chroma DB

## Important caveat

This repo uses Chroma DB, but PDF extraction and chunking happen locally during ingestion.

The assistant still calls Groq for the final answer, but retrieval is now based on a small
persistent vector database in `backend/chroma_db/`.

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

## Render note

Use [`render.yaml`](render.yaml) to deploy the backend on Render from the repo root.
If you want to set it up manually, the commands are:

```bash
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

The root `requirements.txt` forwards to `backend/requirements.txt`.

This setup is intentionally lightweight so it has a much better chance of staying under
Render's small memory limit during a test deploy.

## Editing Knowledge

Add or replace PDFs in `backend/data/raw/`, rebuild Chroma locally, then push the repo.
At runtime, the backend reads only the stored Chroma DB and answers from those PDF chunks.

Rebuild the local Chroma DB:

```bash
python -m backend.services.ingestion_service
```

Then commit and push the updated `backend/chroma_db/` folder.

Optional chunk controls:

- `PDF_CHUNK_SIZE=10`
- `PDF_CHUNK_OVERLAP=2`

## API

- `GET /api/health`
- `POST /api/query`

The frontend sends chat requests to `/api/query`.
