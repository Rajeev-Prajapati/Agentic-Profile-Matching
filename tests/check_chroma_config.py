
from tools.rag_tool import collection

print("\n--- ChromaDB Configuration ---")
print("Collection name:", collection.name)
print("Collection metadata:", collection.metadata)
print("Total records:", collection.count())

print("\n--- Sample Record ---")

sample = collection.get(
    limit=1,
    include=["documents", "metadatas"]
)

if sample["ids"]:
    print("Candidate ID:", sample["ids"][0])
    print("Metadata:", sample["metadatas"][0])
    print(
        "Resume preview:",
        sample["documents"][0][:300]
    )
else:
    print("Collection is empty.")
