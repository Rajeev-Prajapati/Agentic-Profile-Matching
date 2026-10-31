import os
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=os.getenv("CHROMA_DIR", "data/chroma_db")
)

collection = client.get_or_create_collection(
    name="candidate_resumes"
)


def index_resume(candidate_id: str, text: str):
    embedding = model.encode(text).tolist()

    collection.upsert(
        ids=[candidate_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[{"candidate_id": candidate_id}]
    )


def search_resumes(query: str, top_k: int = 10):
    embedding = model.encode(query).tolist()

    count = collection.count()
    if count == 0:
        return []

    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(top_k, count),
        include=["documents", "distances", "metadatas"]
    )

    candidates = []

    for i, candidate_id in enumerate(results["ids"][0]):
        candidates.append({
            "candidate_id": candidate_id,
            "resume": results["documents"][0][i],
            "distance": results["distances"][0][i]
        })

    return candidates