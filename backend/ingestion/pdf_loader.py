def extract_pdf_text(pdf_path:str) -> str:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF is not installed. Run `pip install -r backend/requirements.txt`."
        ) from exc

    doc = fitz.open(pdf_path)
    text_parts = []
    page_count = 0
    for page in doc:
        try:
            text_parts.append(page.get_text())
            page_count += 1
            # print(page.get_text())
        except Exception as e:
            print(f"Error extracting text from page {page_count + 1}: {e}")

    print(f"Extracted text from {page_count} pages.")
    doc.close()
    return "".join(text_parts)
