from services.deep_analyzer import analyze_shortlist
from services.recommendation_service import (
    generate_recommendation_report
)
from tools.intent_tool import (
    detect_intent,
    extract_requirement_changes
)
from agents.state import AgentState
from tools.comparison_tool import compare_candidates
from tools.interview_tool import generate_interview_questions
from services.requirement_refiner import update_requirements
from tools.requirement_tool import extract_requirements
from tools.rag_tool import search_resumes
from langchain_core.messages import AIMessage

# Requirement refinement
from services.requirement_refiner import update_requirements

from services.advanced_ranker import rank_candidates


def parse_jd_node(state: AgentState) -> dict:
    """Store the user's job description."""

    query = state.get("user_query", "").strip()

    if not query:
        raise ValueError("Job description cannot be empty")

    return {
        "job_description": query,
        "screening_round": 1
    }


def extract_requirements_node(state: AgentState) -> dict:
    """Extract structured requirements using Groq."""

    requirements = extract_requirements(
        state["job_description"]
    )

    return {
        "requirements": requirements
    }


def search_resumes_node(state: AgentState):
    requirements = state["requirements"]

    query_parts = [
        requirements.get("role", ""),
        *requirements.get("must_have", []),
        *requirements.get("nice_to_have", []),
        f"{requirements.get('min_experience', 0)} years experience"
    ]

    search_query = " ".join(query_parts)

    candidates = search_resumes(
        search_query,
        top_k=100
    )

    return {
        "retrieved_candidates": candidates
    }

def rank_candidates_node(state: AgentState) -> dict:
    """Rank candidates against job requirements."""

    ranked = rank_candidates(
        state["retrieved_candidates"],
        state["requirements"]
    )

    shortlist = ranked[:10]

    reasoning = {
        candidate["candidate_id"]: {
            "score": candidate["score"],
            "strengths": candidate["strengths"],
            "gaps": candidate["gaps"]
        }
        for candidate in shortlist
    }

    return {
        "shortlist": shortlist,
        "ranking_reasoning": reasoning
    }



def deep_analysis_node(state: AgentState) -> dict:
    """
    Round 2: Deep analysis of top 10 candidates.
    """

    shortlist = state.get("shortlist", [])
    requirements = state.get("requirements", {})

    if not shortlist:
        return {
            "deep_analyses": [],
            "screening_round": 0
        }

    analyses = analyze_shortlist(
        shortlist=shortlist,
        requirements=requirements
    )

    return {
        "deep_analyses": analyses,
        "screening_round": 2
    }



def screening_report_node(state: AgentState) -> dict:
    """
    Round 3: Generate screening recommendation report.
    """

    analyses = state.get("deep_analyses", [])
    requirements = state.get("requirements", {})

    if not analyses:
        report = (
            "No candidates are available for screening."
        )
    else:
        report = generate_recommendation_report(
            analyses=analyses,
            requirements=requirements
        )

    return {
        "screening_report": report,
        "report": report,
        "screening_round": 3,
        "approval_status": "pending",
        "feedback_status": "pending",
        "review_candidate_ids": [],
        "review_notes": "",
    }



def request_review_node(state: AgentState) -> dict:
    """
    Record a request for additional human review.

    This node does not make a hiring decision
    or fabricate missing candidate evidence.
    """

    shortlist = state.get("shortlist", [])
    selected_ids = state.get("selected_candidate_ids", [])
    user_query = state.get("user_query", "")

    valid_ids = {
        candidate["candidate_id"]
        for candidate in shortlist
    }

    # Only accept IDs belonging to the current shortlist.
    review_ids = [
        candidate_id
        for candidate_id in selected_ids
        if candidate_id in valid_ids
    ]

    if not review_ids:
        report = (
            "Please specify a shortlisted candidate ID "
            "for additional review."
        )

        return {
            "report": report,
            "feedback_status": "candidate_selection_required",
            "messages": [AIMessage(content=report)]
        }

    report = (
        "Additional human review requested for: "
        + ", ".join(review_ids)
        + "\n\nReview notes: "
        + user_query
        + "\n\nStatus: Awaiting additional evidence "
          "or recruiter assessment."
    )

    return {
        "review_candidate_ids": review_ids,
        "review_notes": user_query,
        "feedback": user_query,
        "feedback_status": "review_requested",
        "approval_status": "pending",
        "report": report,
        "messages": [AIMessage(content=report)]
    }



def generate_report_node(state: AgentState):
    requirements = state["requirements"]
    shortlist = state.get("shortlist", [])

    lines = [
        "# Candidate Matching Report",
        "",
        f"**Role:** {requirements.get('role', 'N/A')}",
        f"**Must-have:** {requirements.get('must_have', [])}",
        f"**Nice-to-have:** {requirements.get('nice_to_have', [])}",
        f"**Experience:** {requirements.get('min_experience', 0)}+ years",
        "",
        "## Top Candidates",
        ""
    ]

    for rank, c in enumerate(shortlist, 1):
        lines.extend([
            f"### {rank}. {c['candidate_id']}",
            f"- Preliminary score: {c['score']}/100",
            f"- Matched skills: {c['strengths']}",
            f"- Missing evidence: {c['gaps']}",
            ""
        ])

    previous = state.get("previous_ranking", [])

    if state.get("intent") == "refine" and previous:
        lines.extend([
            "## Ranking Changes",
            "",
            *ranking_changes(previous, shortlist)
        ])

    if not shortlist:
        lines.append("No candidates found.")

    report = "\n".join(lines)

    return {
        "report": report,
        "feedback_status": "awaiting_feedback",
        "approval_status": "pending",
        "messages": [AIMessage(content=report)]
    }

def human_feedback_node(state: AgentState) -> dict:
    """Mark the workflow as awaiting human review."""

    return {
        "feedback_status": "awaiting_feedback"
    }


def intent_router_node(state: AgentState):
    result = detect_intent(
        state["user_query"],
        has_shortlist=bool(state.get("shortlist"))
    )

    return {
        "intent": result["action"],
        "selected_candidate_ids": result["candidate_ids"],
        "requirement_changes": {
            "top_n": result["top_n"]
        }
    }


def refine_requirements_node(state: AgentState):
    current = state["requirements"]

    changes = extract_requirement_changes(
        state["user_query"],
        current
    )

    updated = update_requirements(
        current,
        changes
    )

    return {
        "previous_ranking": state.get(
            "shortlist", []
        ),
        "requirements": updated,
        "requirement_changes": changes,
        "feedback": state["user_query"],
        "feedback_status": "refined",
        "approval_status": "pending"
    }


def compare_candidates_node(state: AgentState):
    shortlist = state.get("shortlist", [])

    ids = state.get(
        "selected_candidate_ids", []
    )

    top_n = state.get(
        "requirement_changes", {}
    ).get("top_n", 3)

    if not ids:
        ids = [
            c["candidate_id"]
            for c in shortlist[:top_n]
        ]

    comparison = compare_candidates(
        ids,
        shortlist=shortlist
    )

    if not comparison:
        report = "No matching shortlisted candidates."
    else:
        lines = ["# Candidate Comparison", ""]

        for candidate in comparison:
            lines.extend([
                f"## {candidate['candidate_id']}",
                f"Score: {candidate.get('score', 'N/A')}",
                f"Strengths: {candidate.get('strengths', [])}",
                f"Gaps: {candidate.get('gaps', [])}",
                ""
            ])

        report = "\n".join(lines)

    return {
        "report": report,
        "messages": [AIMessage(content=report)]
    }



def explain_ranking_node(state: AgentState):
    shortlist = state.get("shortlist", [])
    ids = state.get("selected_candidate_ids", [])

    if not ids:
        ids = [
            c["candidate_id"]
            for c in shortlist[:2]
        ]

    lookup = {
        c["candidate_id"]: c
        for c in shortlist
    }

    selected = [
        lookup[cid]
        for cid in ids
        if cid in lookup
    ]

    if not selected:
        report = "No shortlisted candidates found."
    else:
        lines = ["# Ranking Explanation", ""]

        for c in selected:
            breakdown = c.get("score_breakdown", {})

            lines.extend([
                f"## {c['candidate_id']}",
                f"- Overall score: {c['score']}/100",
                f"- Mandatory skills: {breakdown.get('mandatory', 'N/A')}",
                f"- Experience: {breakdown.get('experience', 'N/A')}",
                f"- Semantic similarity: {breakdown.get('semantic', 'N/A')}",
                f"- Preferred skills: {breakdown.get('preferred', 'N/A')}",
                f"- Matched skills: {c.get('strengths', [])}",
                f"- Missing mandatory skill evidence: {c.get('gaps', [])}",
                f"- Years of experience stated: {c.get('years_experience', 'Unknown')}",
                f"- Unavailable evidence: {c.get('missing_evidence', [])}",
                ""
            ])

        if len(selected) >= 2:
            difference = (
                selected[0]["score"]
                - selected[1]["score"]
            )

            lines.append(
                f"Overall score difference: {difference:+.2f}"
            )

        report = "\n".join(lines)

    return {
        "report": report,
        "messages": [AIMessage(content=report)]
    }



def interview_questions_node(state: AgentState):
    ids = state.get(
        "selected_candidate_ids", []
    )

    if not ids:
        shortlist = state.get("shortlist", [])

        if not shortlist:
            report = "No candidates available."
            return {
                "report": report,
                "messages": [AIMessage(content=report)]
            }

        ids = [shortlist[0]["candidate_id"]]

    candidate_id = ids[0]

    result = generate_interview_questions(
        candidate_id,
        state["requirements"]
    )

    questions = result["questions"]

    report = (
        f"# Interview Questions: {candidate_id}\n\n"
        + "\n".join(
            f"{i}. {q}"
            for i, q in enumerate(questions, 1)
        )
    )

    return {
        "report": report,
        "messages": [AIMessage(content=report)]
    }


def approve_shortlist_node(state: AgentState):
    report = (
        "The candidate shortlist has been approved "
        "for the next screening round. "
        "Final hiring decisions require human review."
    )

    return {
        "approval_status": "approved",
        "feedback_status": "completed",
        "report": report,
        "messages": [AIMessage(content=report)]
    }


def ranking_changes(previous, current):
    old_positions = {
        c["candidate_id"]: i
        for i, c in enumerate(previous, 1)
    }

    changes = []

    for position, candidate in enumerate(
        current, 1
    ):
        cid = candidate["candidate_id"]
        old = old_positions.get(cid)

        if old is None:
            movement = "New to top 10"
        elif old > position:
            movement = f"Moved up {old - position}"
        elif old < position:
            movement = f"Moved down {position - old}"
        else:
            movement = "Unchanged"

        changes.append(
            f"- {cid}: {movement}"
        )

    return changes