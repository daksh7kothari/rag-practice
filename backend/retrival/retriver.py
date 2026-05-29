from backend.vectorstore.chroma_store import search

def retrieve(query, top_k: int = 5) -> list[str]:
    """
    Retrieve similar chunks from the lightweight text corpus.

    Args:
        query: The user query string.
        top_k (int): Number of top similar chunks to retrieve.
    Returns:
        list[str]: List of retrieved chunk texts.
    """
    return search(query, top_k)
if __name__ == "__main__":
    query = "What is the first chunk about?"
    results = retrieve(query, top_k=5)
    print("Retrieved chunks:")
    for idx, chunk in enumerate(results):
        print(f"{idx + 1}. {chunk}")
