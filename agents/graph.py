
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from agents.nodes import request_review_node

from agents.state import AgentState

from agents.nodes import (
    parse_jd_node,
    extract_requirements_node,
    search_resumes_node,
    rank_candidates_node,
    generate_report_node,
    intent_router_node,
    refine_requirements_node,
    compare_candidates_node,
    explain_ranking_node,
    interview_questions_node,
    approve_shortlist_node,
    deep_analysis_node,
    screening_report_node,
)


def route_intent(state: AgentState):
    intent = state.get("intent", "new_search")

    routes = {
        "new_search": "parse_jd",
        "refine": "refine_requirements",
        "compare": "compare_candidates",
        "explain": "explain_ranking",
        "interview": "interview_questions",
        "approve": "approve_shortlist"
    }

    # Follow-up actions require an existing shortlist.
    if intent != "new_search" and not state.get("shortlist"):
        return "parse_jd"
    if intent == "review":
        return "request_review"
    return routes.get(intent, "parse_jd")

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node(
        "intent_router", intent_router_node
    )
    builder.add_node(
        "parse_jd", parse_jd_node
    )
    builder.add_node(
        "extract_requirements",
        extract_requirements_node
    )
    builder.add_node(
        "refine_requirements",
        refine_requirements_node
    )
    builder.add_node(
        "search_resumes",
        search_resumes_node
    )
    builder.add_node(
        "rank_candidates",
        rank_candidates_node
    )
    builder.add_node(
        "generate_report",
        generate_report_node
    )
    builder.add_node(
        "compare_candidates",
        compare_candidates_node
    )
    builder.add_node(
        "explain_ranking",
        explain_ranking_node
    )
    builder.add_node(
        "interview_questions",
        interview_questions_node
    )
    builder.add_node(
        "request_review",
        request_review_node
    )
    builder.add_node(
        "approve_shortlist",
        approve_shortlist_node
    )

    builder.add_edge(START, "intent_router")

    builder.add_conditional_edges(
        "intent_router",
        route_intent
    )

    # New job description
    builder.add_edge(
        "parse_jd",
        "extract_requirements"
    )
    builder.add_edge(
        "extract_requirements",
        "search_resumes"
    )

    # Refined requirements
    builder.add_edge(
        "refine_requirements",
        "search_resumes"
    )

    # Shared search and ranking workflow
    builder.add_edge(
        "search_resumes",
        "rank_candidates"
    )

    builder.add_edge("rank_candidates", "deep_analysis"),
    builder.add_edge("deep_analysis", "screening_report"),
    builder.add_edge("screening_report", END)

    builder.add_edge(
        "generate_report", END
    )

    # Conversational actions
    builder.add_edge(
        "compare_candidates", END
    )
    builder.add_edge(
        "explain_ranking", END
    )
    builder.add_edge(
        "interview_questions", END
    )
    builder.add_edge(
        "approve_shortlist", END
    )

    builder.add_node(
        "deep_analysis",
        deep_analysis_node
    )
    
    builder.add_node(
        "screening_report",
        screening_report_node
    )
    builder.add_edge(
        "request_review",
        END
    )

    return builder.compile(
        checkpointer=InMemorySaver()
    )

   