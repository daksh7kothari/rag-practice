from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.services.full_flow import full_flow

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/query")
@app.post("/api/query")
def query_rag(data: QueryRequest):
    answer = full_flow(data.query)
    return {"answer": answer}

print("Starting FastAPI server...")
