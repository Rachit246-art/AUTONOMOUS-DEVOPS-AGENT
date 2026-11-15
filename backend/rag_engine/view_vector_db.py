
import json
from pathlib import Path

from backend.rag_engine.vector_store import collection


# Step 1: Check total stored records
total_records = collection.count()

print("\n========== VECTOR DATABASE DETAILS ==========")
print("Collection:", collection.name)
print("Total stored chunks:", total_records)


# Step 2: Retrieve all stored records and vectors
results = collection.get(
    include=["documents", "metadatas", "embeddings"]
)

# Step 3: Display first 5 records
print("\n========== FIRST 5 STORED VECTORS ==========")

for i in range(min(5, len(results["ids"]))):

    print("\nRecord ID:", results["ids"][i])
    print("Source:", results["metadatas"][i]["source"])
    print("Text:", results["documents"][i][:150])

    vector = results["embeddings"][i].tolist()

    print("Vector dimensions:", len(vector))
    print("Vector values:", vector)


# Step 4: Export ALL records and vectors into JSON
all_records = []

for i in range(len(results["ids"])):

    record = {
        "id": results["ids"][i],
        "source": results["metadatas"][i]["source"],
        "text": results["documents"][i],
        "embedding": results["embeddings"][i].tolist()
    }

    all_records.append(record)


# Save outside the ChromaDB directory
project_root = Path(__file__).resolve().parents[2]
output_file = project_root / "data" / "vector_export.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(all_records, file, indent=2)

print("\n========== EXPORT COMPLETED ==========")
print("Total exported records:", len(all_records))
print("Export location:", output_file)
