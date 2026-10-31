import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field


class JobRequirements(BaseModel):
    role: str = ""
    must_have: list[str] = Field(default_factory=list)
    nice_to_have: list[str] = Field(default_factory=list)
    min_experience: float = 0


def extract_requirements(jd: str) -> dict:
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    structured_llm = llm.with_structured_output(
        JobRequirements
    )

    result = structured_llm.invoke([
        SystemMessage(
            content=(
                "Extract explicit hiring requirements. "
                "Do not invent requirements. "
                "Separate mandatory from preferred skills."
            )
        ),
        HumanMessage(content=jd)
    ])

    return result.model_dump()