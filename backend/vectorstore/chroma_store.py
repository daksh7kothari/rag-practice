from __future__ import annotations

from collections import Counter
import hashlib
import math
import os
from pathlib import Path
import re
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parents[1]
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "pdf_chunks")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "8192"))

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
}


def _tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOPWORDS
    ]


def _hash_token(token: str) -> int:
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % EMBEDDING_DIMENSIONS


def _embed_text(text: str) -> list[float]:
    tokens = _tokenize(text)
    if not tokens:
        return [0.0] * EMBEDDING_DIMENSIONS

    counts = Counter(tokens)
    vector = [0.0] * EMBEDDING_DIMENSIONS
    for token, count in counts.items():
        vector[_hash_token(token)] += float(count)

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0.0:
        return vector
    return [value / norm for value in vector]


class HashEmbeddingFunction:
    def name(self) -> str:
        return "local_hash_embedding"

    def __call__(self, input: Iterable[str]) -> list[list[float]]:
        return [_embed_text(text) for text in input]

    def embed_query(self, input: str | Iterable[str]) -> list[float] | list[list[float]]:
        if isinstance(input, str):
            return _embed_text(input)
        return [_embed_text(text) for text in input]

    def embed_documents(self, input: Iterable[str]) -> list[list[float]]:
        return [_embed_text(text) for text in input]


def _get_chroma_client():
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError(
            "chromadb is not installed. Run `pip install -r backend/requirements.txt`."
        ) from exc

    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def _get_collection():
    client = _get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=HashEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )


def reset_collection():
    client = _get_chroma_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception as exc:
        if "does not exist" not in str(exc):
            raise
        pass
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=HashEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )


def store_chunks(chunks: list[str], source: str = "unknown.pdf") -> bool:
    """
    Persist PDF chunks into Chroma. This is intended for local ingestion.
    """

    if not chunks:
        return False

    collection = _get_collection()
    source_slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", source).strip("-") or "source"
    ids = [f"{source_slug}-{index}" for index in range(1, len(chunks) + 1)]
    metadatas = [
        {"source": source, "chunk": str(index)}
        for index in range(1, len(chunks) + 1)
    ]
    collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)
    return True


def search(query: str, top_k: int = 5) -> list[str]:
    """
    Search the prebuilt Chroma DB. Runtime does not parse or chunk PDFs.
    """

    if not query.strip():
        return []

    if not CHROMA_DIR.exists():
        return []

    collection = _get_collection()
    if collection.count() == 0:
        return []

    result = collection.query(query_texts=[query], n_results=top_k)
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]

    chunks: list[str] = []
    for document, metadata in zip(documents, metadatas):
        source = metadata.get("source", "unknown.pdf") if metadata else "unknown.pdf"
        chunk = metadata.get("chunk", "?") if metadata else "?"
        chunks.append(f"Source: {source} | Chunk: {chunk}\n{document}")

    return chunks


if __name__ == "__main__":
    collection = _get_collection()
    print(f"Loaded {collection.count()} chunks from {CHROMA_DIR}")
