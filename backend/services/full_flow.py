from backend.generation.groq_client import generate_response
from backend.generation.prompt_builder import generate_prompt
from backend.retrival.retriver import retrieve


def full_flow(query: str) -> str:
    """
    Full flow: Search corpus -> Build prompt -> Generate response
    """
    retrieved_chunks = retrieve(query, top_k=5)
    prompt = generate_prompt(retrieved_chunks, query)
    response = generate_response(prompt)
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
