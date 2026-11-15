
from backend.rag_engine.retriever import retrieve_relevant_chunks
from backend.rag_engine.llm_client import llm


def generate_rag_response(error_message: str):

    if not error_message or not error_message.strip():
        raise ValueError("Error message cannot be empty.")

    print("\n========== RAG PIPELINE STARTED ==========")

    # Step 1: Retrieve relevant chunks
    print("\n[1] Retrieving relevant information from ChromaDB...")

    retrieved_chunks = retrieve_relevant_chunks(
        query_text=error_message,
        top_k=3
    )

    if not retrieved_chunks:
        return {
            "error_message": error_message,
            "retrieved_chunks": 0,
            "sources": [],
            "solution": "No relevant troubleshooting information found."
        }

    print("Retrieved chunks:", len(retrieved_chunks))

    # Step 2: Prepare context
    print("\n[2] Preparing context...")

    context = ""

    for index, chunk in enumerate(retrieved_chunks, start=1):
        context += (
            f"\nSource {index}: {chunk['source']}\n"
            f"Information:\n{chunk['text']}\n"
        )

    print("Context length:", len(context))

    # Step 3: Prepare RAG prompt
    print("\n[3] Preparing RAG prompt...")

    rag_prompt = f"""
You are an expert DevOps troubleshooting assistant.

Answer the user's error using the provided troubleshooting information.

Instructions:
1. Explain the possible cause of the error.
2. Provide step-by-step troubleshooting solutions.
3. Use retrieved information as your primary reference.
4. If the information is insufficient, clearly mention it.
5. Do not invent technical details.
6. Provide practical and easy-to-understand solutions.
7. If the error is not recognized, simply reply with "Error not recognized try rephrasing that". 
Retrieved Troubleshooting Information:

{context}

User's Error:

{error_message}

Provide a clear and structured troubleshooting solution.
"""

    print("Prompt length:", len(rag_prompt))

    # Step 4: Generate response using GPT-5 Chat
    print("\n[4] Generating solution using GPT-5 Chat...")

    response = llm.invoke(
        rag_prompt
    )

    # Step 5: Prepare final result
    sources = list(set(
        chunk["source"] for chunk in retrieved_chunks
    ))

    result = {
        "error_message": error_message,
        "retrieved_chunks": len(retrieved_chunks),
        "sources": sources,
        "solution": response
    }

    print("\n========== RAG PIPELINE COMPLETED ==========")

    return result


if __name__ == "__main__":

    test_error = "My Docker container keeps restarting repeatedly."

    result = generate_rag_response(test_error)

    print("\n========== FINAL RAG RESPONSE ==========")

    print("\nError:")
    print(result["error_message"])

    print("\nRetrieved Chunks:")
    print(result["retrieved_chunks"])

    print("\nSources:")

    for source in result["sources"]:
        print("-", source)

    print("\nGenerated Solution:")
    print(result["solution"])
