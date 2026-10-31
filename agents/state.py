
from typing import TypedDict, Annotated, Any
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    messages: Annotated[list, add_messages]

    user_query: str
    intent: str

    job_description: str
    requirements: dict[str, Any]
    requirement_changes: dict[str, Any]

    retrieved_candidates: list[dict[str, Any]]
    shortlist: list[dict[str, Any]]
    previous_ranking: list[dict[str, Any]]

    ranking_reasoning: dict[str, Any]
    selected_candidate_ids: list[str]

    screening_round: int

    report: str
    feedback: str
    feedback_status: str
    approval_status: str

    deep_analyses: list[dict]
    screening_report: str

    review_candidate_ids: list[str]
    review_notes: str