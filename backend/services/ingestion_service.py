from pathlib import Path

from backend.ingestion.chunker import chunk_text
from backend.ingestion.cleaner import clean_text
from backend.ingestion.pdf_loader import extract_pdf_text
from backend.vectorstore.chroma_store import reset_collection, store_chunks


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PDF_DIR = BASE_DIR / "data" / "raw"

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
    store_chunks(chunks, source=Path(pdf_path).name)
    return chunks


def ingest_all_pdfs(raw_pdf_dir: Path = RAW_PDF_DIR) -> int:
    """
    Rebuilds the local Chroma DB from every PDF in backend/data/raw.
    """

    reset_collection()
    total_chunks = 0
    pdf_paths = sorted(raw_pdf_dir.glob("*.pdf"))
    for pdf_path in pdf_paths:
        chunks = ingest_pdf(str(pdf_path))
        total_chunks += len(chunks)
        print(f"Ingested {len(chunks)} chunks from {pdf_path.name}.")
    return total_chunks
  
if __name__ == "__main__":
    pdf = input("Enter pdf name:")
    ingest_pdf(f"backend/data/raw/{pdf}.pdf")
    # total = ingest_all_pdfs()
    # print(f"Ingested a total of {total} chunks from {len(RAW_PDF_DIR.glob('*.pdf'))} PDFs.")  
