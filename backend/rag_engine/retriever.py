
from backend.rag_engine.embeddings import generate_embeddings
from backend.rag_engine.vector_store import collection


# --------------------------------------------------
# 1. RETRIEVER CONFIGURATION
# --------------------------------------------------

MAX_COSINE_DISTANCE = 0.65
DEFAULT_TOP_K = 5


# --------------------------------------------------
# 2. DEVOPS DOMAIN VALIDATION
# --------------------------------------------------

DEVOPS_KEYWORDS = {
    "docker", "container", "kubernetes", "kubectl",
    "jenkins", "pipeline", "deployment", "devops",
    "server", "sql", "database", "connection",
    "timeout", "network", "api", "fastapi", "python",
    "linux", "nginx", "apache", "cloud", "aws",
    "azure", "monitoring", "grafana", "prometheus",
    "build", "crash", "error", "exception", "logs",
    "memory", "cpu", "disk", "port", "firewall",
    "dns", "git", "github", "redis", "mongodb",
    "ci/cd", "latency", "performance", "authentication",
    "ssl", "tls", "database", "connection pool"
}


def is_devops_query(query_text: str) -> bool:

    words = set(
        query_text.lower()
        .replace("-", " ")
        .replace("/", " ")
        .replace(".", " ")
        .split()
    )

    return bool(words.intersection(DEVOPS_KEYWORDS))


# --------------------------------------------------
# 3. RETRIEVE RELEVANT CHUNKS
# --------------------------------------------------

def retrieve_relevant_chunks(
    query_text: str,
    top_k: int = DEFAULT_TOP_K,
    max_distance: float = MAX_COSINE_DISTANCE
):

    if not query_text or not query_text.strip():
        raise ValueError("Query text cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    print("\n========== RETRIEVER STARTED ==========")
    print("User Query:", query_text)

    # --------------------------------------------------
    # STEP 1: DOMAIN VALIDATION
    # --------------------------------------------------

    if not is_devops_query(query_text):

        print("Query rejected: Outside DevOps domain.")

        return []

    # --------------------------------------------------
    # STEP 2: CHECK CHROMADB COLLECTION
    # --------------------------------------------------

    total_chunks = collection.count()

    print("Collection:", collection.name)
    print("Total chunks in ChromaDB:", total_chunks)

    if total_chunks == 0:

        print("WARNING: ChromaDB collection is empty.")

        return []

    # --------------------------------------------------
    # STEP 3: GENERATE QUERY EMBEDDING
    # --------------------------------------------------

    print("\nGenerating query embedding...")

    query_embedding = generate_embeddings([query_text])

    if query_embedding is None or len(query_embedding) == 0:
        raise RuntimeError("Failed to generate query embedding.")

    query_vector = query_embedding.tolist()

    # --------------------------------------------------
    # STEP 4: SEARCH CHROMADB
    # --------------------------------------------------

    print("\nSearching relevant chunks...")

    results = collection.query(
        query_embeddings=query_vector,
        n_results=min(top_k, total_chunks),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    # --------------------------------------------------
    # STEP 5: APPLY RELEVANCE FILTERING
    # --------------------------------------------------

    retrieved_chunks = []

    for chunk_id, document, metadata, distance in zip(
        ids, documents, metadatas, distances
    ):

        if not document:
            continue

        distance = float(distance)

        metadata = metadata or {}

        print("\n----------------------------------")
        print("Chunk ID:", chunk_id)
        print(f"Cosine Distance: {distance:.4f}")
        print("Source:", metadata.get("source", "Unknown"))

        if distance > max_distance:

            print("Rejected: Below relevance threshold.")

            continue

        retrieved_chunks.append({
            "id": chunk_id,
            "text": document,
            "source": metadata.get(
                "source", "Unknown source"
            ),
            "distance": distance
        })

        print("Accepted: Relevant chunk found.")

        print("Text Preview:", document[:200])

    # --------------------------------------------------
    # STEP 6: RETRIEVAL SUMMARY
    # --------------------------------------------------

    print("\n========== RETRIEVAL SUMMARY ==========")

    print("Total chunks available:", total_chunks)
    print("Chunks searched:", len(ids))
    print("Relevant chunks found:", len(retrieved_chunks))

    if not retrieved_chunks:
        print("No chunks passed the relevance threshold.")

    return retrieved_chunks


# --------------------------------------------------
# 4. STANDALONE TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_query = "My SQL Server is showing too many connections."

    chunks = retrieve_relevant_chunks(test_query)

    print("\n========== FINAL RESULTS ==========")

    for chunk in chunks:

        print("\nSource:", chunk["source"])
        print("Distance:", chunk["distance"])
        print("Content:", chunk["text"])
