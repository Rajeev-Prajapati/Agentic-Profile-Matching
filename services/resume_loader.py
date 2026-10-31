from pathlib import Path
from pypdf import PdfReader
from docx import Document


def load_resume(file_path: str) -> str:
    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        reader = PdfReader(path)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if path.suffix.lower() == ".docx":
        doc = Document(path)
        return "\n".join(
            p.text for p in doc.paragraphs
        )

    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    raise ValueError(f"Unsupported format: {path.suffix}")