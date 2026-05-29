def load_model():
    """
    Lightweight compatibility shim.

    The production-like version of this repo used sentence-transformers, but the
    Render test path now uses simple text retrieval to stay within a small memory
    budget.
    """
    return None


def embed_chunks(model, chunks):
    return list(chunks)


def embed_query(model, query):
    return query


if __name__ == "__main__":
    print("Lightweight embedder shim loaded successfully.")
