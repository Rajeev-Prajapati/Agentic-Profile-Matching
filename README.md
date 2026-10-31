
# Agentic Profile Matching

An AI-powered resume screening and candidate matching application built with LangGraph, Groq, ChromaDB, HuggingFace embeddings, Python, and Streamlit.

## Overview

Agentic Profile Matching helps recruiters analyze job descriptions, retrieve relevant resumes, rank candidates, compare qualifications, generate technical interview questions, and review candidate shortlists.

The application supports conversational refinement of job requirements without restarting the entire process.

All screening recommendations are preliminary and require human review.

## Key Features

- Natural-language job description processing
- Structured requirement extraction
- Conversational requirement refinement
- Semantic resume retrieval using ChromaDB
- Weighted candidate ranking
- Top-10 candidate shortlisting
- Candidate comparison and ranking explanations
- Deep candidate screening analysis
- Technical interview question generation
- Human review and shortlist approval
- Screening report generation and download
- Streamlit dashboard
- LangGraph state management and checkpointing

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend implementation |
| LangGraph | Agent orchestration and state |
| Groq | LLM inference |
| ChromaDB | Vector database |
| HuggingFace | Text embeddings |
| Streamlit | Web interface |
| Pydantic | Structured LLM outputs |
| Pytest | Automated testing |

## System Architecture

```text
Recruiter
   |
   v
Streamlit Application
   |
   v
LangGraph Intent Router
   |
   +-- New Job Description
   |      |
   |      v
   |   Requirement Extraction
   |      |
   |      v
   |   ChromaDB Resume Search
   |      |
   |      v
   |   Candidate Ranking
   |      |
   |      v
   |   Deep Analysis
   |      |
   |      v
   |   Screening Report
   |
   +-- Refine Requirements
   |      |
   |      v
   |   Search and Rank Again
   |
   +-- Compare Candidates
   |
   +-- Explain Ranking
   |
   +-- Generate Interview Questions
   |
   +-- Request Human Review
   |
   +-- Approve Shortlist
```

## Candidate Ranking

The preliminary ranking formula is:

Score = 0.40M + 0.25E + 0.20S + 0.15P

Where:

- M = Mandatory skill coverage
- E = Experience score
- S = Semantic similarity
- P = Preferred skill coverage

The implementation may redistribute weights when evidence is unavailable. This behavior must be considered when interpreting scores.

Skill matching and experience extraction are heuristic and do not independently verify candidate qualifications.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure the Groq API key.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
RESUME_DIR=data/resumes
CHROMA_DIR=data/chroma_db
```

Never commit the actual `.env` file.

### 5. Prepare the resume database

Place supported resumes in `data/resumes/`.

Run the project's resume ingestion script to populate ChromaDB.

The ingestion command must be confirmed against the actual repository.

### 6. Start Streamlit

```bash
streamlit run app.py
```

Open:

http://localhost:8501

## Example Conversation

User:
We need a Python Backend Developer with 4 years of experience. Python, Django, and PostgreSQL are mandatory. Docker and Redis are preferred.

Agent:
Extracts requirements, searches resumes, ranks candidates, and generates a screening report.

User:
Make Docker mandatory and remove Redis.

Agent:
Updates requirements and reruns screening.

User:
Compare the top 3 candidates.

Agent:
Compares candidate scores, matched skills, and missing evidence.

User:
Generate interview questions for candidate_002.

Agent:
Generates candidate-specific technical questions.

User:
Request additional review for candidate_002.

Agent:
Records a human-review request.

User:
Approve the shortlist.

Agent:
Marks the shortlist approved for interview screening.

## Running Tests

Run all unit tests:

```bash
python -m pytest tests/ -v
```

Run the live integration tests:

```bash
python -m pytest tests/test_e2e_workflow.py -v -m integration
```

Live integration tests require configured API credentials and an available resume collection.

## Project Limitations

- Resume skills are identified using text matching.
- Experience extraction relies on explicit resume statements.
- Missing evidence is not proof that a candidate lacks a skill.
- Semantic scoring depends on the configured ChromaDB distance metric.
- The initial dataset contains synthetic resumes.
- In-memory checkpoints are not persistent across application restarts.
- Screening recommendations are not validated hiring predictions.
- Final hiring decisions must remain with qualified human reviewers.

## Future Enhancements

- Persistent LangGraph checkpoints
- Resume uploads through Streamlit
- Evidence citations from source resumes
- Improved relevant-experience extraction
- Ranking evaluation with labeled datasets
- Fairness and reliability evaluation
- PDF report export
- Authentication and role-based access control

## Disclaimer

This application is an educational prototype. It is designed to assist human reviewers, not to make autonomous employment decisions.
```
