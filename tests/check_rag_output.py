
from tools.rag_tool import search_resumes

results = search_resumes(
    "Python Django PostgreSQL developer",
    top_k=3
)

print("\n--- RAG Search Output ---")

for candidate in results:
    print("\nCandidate:", candidate.get("candidate_id"))
    print("Available keys:", list(candidate.keys()))
    print("Distance:", candidate.get("distance"))
    print("Years:", candidate.get("years_experience"))

    resume = candidate.get("resume", "")
    print("Resume preview:", resume[:200])
