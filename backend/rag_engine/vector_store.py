
import chromadb
from pathlib import Path
import hashlib
from typing import List, Dict, Any


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_DB_DIR = PROJECT_ROOT / "data" / "vector_db"

# Ensure database directory exists
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. CHROMADB CLIENT
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)


# --------------------------------------------------
# 3. CREATE OR ACCESS COLLECTION
# --------------------------------------------------

collection = client.get_or_create_collection(
    name="devops_troubleshooting_v2",
    metadata={
        "hnsw:space": "cosine"
    }
)


# --------------------------------------------------
# 4. STORE EMBEDDINGS
# --------------------------------------------------

def store_embeddings(
    chunks: List[str],
    embeddings,
    sources: List[str]
) -> int:

    """
    Store text chunks, embeddings and source metadata
    in ChromaDB.
    """

    # Validate input lengths
    if not (
        len(chunks) == len(embeddings) == len(sources)
    ):
        raise ValueError(
            "Chunks, embeddings and sources must have equal lengths."
        )

    if not chunks:
        print("No chunks available to store.")
        return 0

    # Validate chunks and sources
    for chunk, source in zip(chunks, sources):

        if not isinstance(chunk, str) or not chunk.strip():
            raise ValueError("Empty or invalid text chunk found.")

        if not isinstance(source, str) or not source.strip():
            raise ValueError("Invalid source filename found.")

    # Convert embeddings to Python lists
    if hasattr(embeddings, "tolist"):
        embedding_list = embeddings.tolist()
    else:
        embedding_list = embeddings

    # Validate embedding dimensions
    dimensions = len(embedding_list[0])

    if dimensions == 0:
        raise ValueError("Embedding vectors cannot be empty.")

    for embedding in embedding_list:

        if len(embedding) != dimensions:
            raise ValueError("Inconsistent embedding dimensions.")

    # Generate unique and reproducible IDs
    ids = []

    for index, (chunk, source) in enumerate(
        zip(chunks, sources)
    ):

        unique_string = f"{source}:{index}:{chunk}"

        chunk_id = hashlib.sha256(
            unique_string.encode("utf-8")
        ).hexdigest()

        ids.append(chunk_id)

    # Prepare metadata
    metadata = [
        {
            "source": source,
            "category": "devops"
        }
        for source in sources
    ]

    # Insert or update records
    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embedding_list,
        metadatas=metadata
    )

    print("\n========== VECTOR STORE ==========")
    print(f"Successfully stored {len(chunks)} chunks.")
    print("Collection:", collection.name)
    print("Embedding Dimensions:", dimensions)
    print("Total Chunks:", collection.count())
    print("Vector Database:", VECTOR_DB_DIR)

    return len(chunks)


# --------------------------------------------------
# 5. COLLECTION INFORMATION
# --------------------------------------------------

def get_collection_info() -> Dict[str, Any]:

    return {
        "collection_name": collection.name,
        "total_chunks": collection.count(),
        "metadata": collection.metadata,
        "database_path": str(VECTOR_DB_DIR)
    }


# --------------------------------------------------
# 6. TEST VECTOR DATABASE
# --------------------------------------------------

if __name__ == "__main__":

    print("\n========== CHROMADB INFORMATION ==========")

    info = get_collection_info()

    for key, value in info.items():
        print(f"{key}: {value}")
