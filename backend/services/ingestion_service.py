from backend.ingestion.chunker import chunk_text
from backend.ingestion.cleaner import clean_text
from backend.ingestion.pdf_loader import extract_pdf_text
from backend.embeddings.embedder import embed_query, load_model
from backend.vectorstore.chroma_store import store_chunks

def ingest_pdf(pdf_path: str) -> list[str]:
    """
    Ingests a PDF file and returns a list of cleaned, chunked text.

    Args:
        pdf_path (str): Path to the PDF file
    Returns:
        list[str]: List of cleaned, chunked text strings
    """  
    raw = extract_pdf_text(pdf_path)
    cleaned = clean_text(raw)
    chunks = chunk_text(cleaned)
    loaded_model = load_model()
    embeddings = embed_query(loaded_model, chunks)
    store_chunks(chunks, embeddings)
    return chunks
  
if __name__ == "__main__":
    pdf=input("Enter the name of the PDF (without .pdf extension): ")
    pdf_path = f"backend/data/raw/{pdf}.pdf"
    chunks = ingest_pdf(pdf_path)
    print(f"Ingested {len(chunks)} chunks from the PDF.")
