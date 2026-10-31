
import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

load_dotenv(override=True)


class IntentResult(BaseModel):
    action: Literal[
        "new_search",
        "refine",
        "compare",
        "explain",
        "interview",
        "approve",
        "review"
    ]

    candidate_ids: list[str] = Field(
        default_factory=list
    )

    top_n: int = 3


class RequirementChanges(BaseModel):
    add_must_have: list[str] = Field(
        default_factory=list
    )
    remove_must_have: list[str] = Field(
        default_factory=list
    )

    add_nice_to_have: list[str] = Field(
        default_factory=list
    )
    remove_nice_to_have: list[str] = Field(
        default_factory=list
    )

    min_experience: float | None = None


def get_llm():
    return ChatGroq(
        model=os.getenv("GROQ_MODEL"),
        temperature=0
    )


def detect_intent(query: str, has_shortlist: bool):
    llm = get_llm().with_structured_output(
        IntentResult
    )

    result = llm.invoke([
        SystemMessage(content=f"""
You are an intent classification assistant for
an AI-powered recruitment application.

Classify the user's recruitment request.

Existing shortlist: {has_shortlist}

Available actions and rules:

1. new_search:
   - User provides a new job description.
   - User wants to start a new candidate search.

2. refine:
   - User changes existing job criteria.
   - User adds or removes required skills.
   - User changes minimum experience.
   - User modifies preferred skills.

3. compare:
   - User asks to compare candidates.
   - User asks to compare the top N candidates.

4. explain:
   - User asks why a candidate has a particular rank.
   - User asks why one candidate ranks above another.
   - User requests a ranking explanation.

5. interview:
   - User requests technical interview questions.
   - User asks for candidate-specific interview questions.

6. approve:
   - User explicitly approves the candidate shortlist.
   - User confirms candidates can proceed to interviews.

7. review:
   - User requests additional human review of a candidate.
   - User wants to flag a candidate for manual verification.
   - User asks to recheck a candidate's qualifications.
   - User wants to investigate missing skill evidence.
   - User requests further screening of a candidate.

Important rules:
- Choose review for additional review or verification.
- Do NOT classify review requests as approve.
- Choose approve only for explicit approval.
- Use candidate IDs only if explicitly provided.
- Extract all explicitly mentioned candidate IDs
  into candidate_ids.
- For "top 3", return top_n=3.
- For "top 5", return top_n=5.
- Do not invent candidate IDs.
- If an existing shortlist is available, interpret
  follow-up requests in that context.
- Return only the structured output.
"""),
        HumanMessage(content=query)
    ])

    return result.model_dump()


def extract_requirement_changes(
    query: str,
    current_requirements: dict
):
    llm = get_llm().with_structured_output(
        RequirementChanges
    )

    result = llm.invoke([
        SystemMessage(content="""
Extract ONLY requested changes to job criteria.

Do not replace all existing requirements.
Do not invent new requirements.

Examples:
"Also require Docker" -> add_must_have=["Docker"]
"Remove AWS" -> remove from the relevant category
"Make TypeScript mandatory" ->
  add_must_have=["TypeScript"],
  remove_nice_to_have=["TypeScript"]

Only set min_experience if the user explicitly
changes the experience requirement.
"""),
        HumanMessage(content=f"""
Current requirements:
{current_requirements}

User instruction:
{query}
""")
    ])

    return result.model_dump()
