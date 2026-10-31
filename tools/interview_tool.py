
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from tools.rag_tool import collection

load_dotenv()


class InterviewQuestions(BaseModel):
    candidate_id: str
    questions: list[str] = Field(
        description="Five technical screening questions"
    )


def generate_interview_questions(
    candidate_id: str,
    requirements: dict | None = None
) -> dict:

    result = collection.get(
        ids=[candidate_id],
        include=["documents"]
    )

    if not result["ids"]:
        raise ValueError(
            f"Candidate not found: {candidate_id}"
        )

    resume = result["documents"][0]

    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL"),
        temperature=0.3
    )

    structured_llm = llm.with_structured_output(
        InterviewQuestions
    )

    messages = [
        SystemMessage(content="""
You are a technical interviewer.

Generate exactly five relevant technical
screening questions.

Rules:
1. Use only job-related criteria.
2. Base questions on the resume and requirements.
3. Test missing or unclear technical evidence.
4. Do not invent candidate qualifications.
5. Avoid personal or protected characteristics.
"""),
        HumanMessage(content=f"""
Candidate ID: {candidate_id}

Resume:
{resume}

Job requirements:
{requirements or {}}
""")
    ]

    response = structured_llm.invoke(messages)

    return response.model_dump()
