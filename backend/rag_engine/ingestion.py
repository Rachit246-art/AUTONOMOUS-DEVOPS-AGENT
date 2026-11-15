from backend.rag_engine.document_loader import load_all_documents
from backend.rag_engine.chunking import chunk_text
from backend.rag_engine.embeddings import generate_embeddings
from backend.rag_engine.vector_store import (
    store_embeddings,
    collection,
)


# --------------------------------------------------
# 1. DOCUMENT INGESTION PIPELINE
# --------------------------------------------------

def ingest_documents():

    print("\n========== DOCUMENT INGESTION STARTED ==========\n")

    # Step 1: Load documents
    print("[1] Loading documents...")

    documents = load_all_documents()

    if not documents:
        print("ERROR: No documents found.")
        print("Please check your documents folder.")
        return

    print(f"Documents loaded: {len(documents)}")

    # Step 2: Generate chunks
    print("\n[2] Generating text chunks...")

    all_chunks = []
    all_sources = []

    for document in documents:

        text = document.get("text", "")
        source = document.get("source", "unknown")

        if not text or not text.strip():
            print(f"WARNING: Empty document skipped: {source}")
            continue

        chunks = chunk_text(
            text,
            chunk_size=500,
            overlap=100
        )

        if not chunks:
            print(f"WARNING: No chunks generated: {source}")
            continue

        all_chunks.extend(chunks)
        all_sources.extend([source] * len(chunks))

        print(f"{source}: {len(chunks)} chunks")

    print(f"\nTotal chunks generated: {len(all_chunks)}")

    if not all_chunks:
        print("ERROR: No chunks available for embedding.")
        return

    # Step 3: Generate embeddings
    print("\n[3] Generating embeddings...")

    embeddings = generate_embeddings(all_chunks)

    if embeddings is None or len(embeddings) != len(all_chunks):
        raise ValueError(
            "Embedding count does not match chunk count."
        )

    print(f"Embeddings generated: {len(embeddings)}")

    # Step 4: Store in ChromaDB
    print("\n[4] Storing data in ChromaDB...")

    stored_count = store_embeddings(
        chunks=all_chunks,
        embeddings=embeddings,
        sources=all_sources
    )

    # Step 5: Verify storage
    print("\n[5] Verifying ChromaDB storage...")

    total_count = collection.count()

    print("Collection:", collection.name)
    print("New chunks submitted:", stored_count)
    print("Total chunks in ChromaDB:", total_count)

    if total_count == 0:
        raise RuntimeError(
            "Document ingestion finished but ChromaDB is empty."
        )

    # Final result
    print("\n========== INGESTION COMPLETED ==========")
    print("Documents processed:", len(documents))
    print("Chunks generated:", len(all_chunks))
    print("Embeddings generated:", len(embeddings))
    print("Total stored chunks:", total_count)


# --------------------------------------------------
# 6. EXECUTE INGESTION
# --------------------------------------------------

if __name__ == "__main__":
    ingest_documents()