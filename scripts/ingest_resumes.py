from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from services.resume_loader import load_resume
from tools.rag_tool import index_resume

resume_dir = Path("data/resumes")

for path in resume_dir.iterdir():
    if path.suffix.lower() not in (".pdf", ".docx", ".txt"):
        continue

    text = load_resume(str(path))

    if not text.strip():
        print(f"Skipped empty resume: {path.name}")
        continue

    index_resume(path.stem, text)
    print(f"Indexed: {path.name}")

print("Resume ingestion completed.")