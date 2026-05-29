def chunk_text(clean_text: str, chunk_size: int = 10, overlap: int = 2) -> list[str]:
    """
    Splits cleaned text into overlapping sentence-based chunks.

    Args:
        clean_text (str): Preprocessed text
        chunk_size (int): Number of sentences per chunk
        overlap (int): Number of overlapping sentences

    Returns:
        list[str]: List of chunked text strings
    """

    import re

    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", clean_text)
        if sentence.strip()
    ]

    if not sentences:
        return []

    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(sentences), step):
        chunk = sentences[i:i + chunk_size]

        if not chunk:
            continue

        chunks.append(" ".join(chunk))

    print(f"Created {len(chunks)} chunks.")
    return chunks

def trim_front_matter(text: str) -> str:
    """
    Trims front matter from the text by removing content before the first occurrence of "Introduction".

    Args:
        text (str): The input text to be trimmed.

    Returns:
        str: The trimmed text starting from "Introduction" or the original text if "Introduction" is not found.
    """
    introduction_index = text.find("Introduction")
    if introduction_index != -1:
        return text[introduction_index:]
    else:
        print("Warning: 'Introduction' not found in text. Returning original text.")
        return text

# Testing
if __name__ == "__main__":
    from backend.ingestion.cleaner import clean_text
    from backend.ingestion.pdf_loader import extract_pdf_text

    raw_text = extract_pdf_text("../data/raw/jain.pdf")
    trimmed = trim_front_matter(raw_text)
    cleaned = clean_text(trimmed)
    chunks = chunk_text(cleaned)

    print(len(chunks))
    print('\n')
    print(chunks[0])
    print('\n')
    print(chunks[1])
