from functools import lru_cache

from backend.embeddings.embedder import embed_query, load_model
from backend.generation.groq_client import generate_response
from backend.generation.prompt_builder import generate_prompt
from backend.retrival.retriver import retrieve


@lru_cache(maxsize=1)
def get_model():
    return load_model()


def full_flow(query: str) -> str:
    """
    Full flow: Embed query -> Retrieve similar chunks -> Generate response
    """
    query_embedding = embed_query(get_model(), query)
    retrieved_chunks = retrieve(query_embedding, top_k=5)
    # print(f"Retrieved Chunks: {retrieved_chunks[0]}")  # Debugging output

    # `generate_prompt` expects context chunks first, then the user question.
    prompt = generate_prompt(retrieved_chunks, query)
    # print(f"Generated Prompt: {prompt}")  # Debugging output
    response = generate_response(prompt)
    # print(f"Generated Response: {response}")  # Debugging output
    return response


if __name__ == "__main__":
    while True:
        query = input("Enter your query (or 'exit' to quit): ")
        if query.lower() == "exit":
            print("Exiting the program.")
            break
        response = full_flow(query)
        print("Response:")
        print(response)
