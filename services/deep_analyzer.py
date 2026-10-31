
from typing import Any

from services.advanced_ranker import score_candidate


def analyze_candidate(
    candidate: dict[str, Any],
    requirements: dict[str, Any]
) -> dict[str, Any]:
    """
    Perform evidence-based screening of one candidate.
    """

    result = score_candidate(candidate, requirements)

    breakdown = result["score_breakdown"]

    mandatory_score = breakdown["mandatory"]
    experience_score = breakdown["experience"]

    missing_skills = result.get("gaps", [])
    missing_evidence = result.get("missing_evidence", [])

    # Recommendation is provisional, not a hiring decision.
    if (
        mandatory_score == 100
        and experience_score is not None
        and experience_score == 100
    ):
        recommendation = "Strong Match"

    elif mandatory_score >= 70:
        recommendation = "Needs Review"

    else:
        recommendation = "Low Match"

    return {
        "candidate_id": result["candidate_id"],
        "overall_score": result["score"],
        "score_breakdown": breakdown,
        "matched_skills": result.get("strengths", []),
        "missing_skill_evidence": missing_skills,
        "years_experience": result.get("years_experience"),
        "missing_evidence": missing_evidence,
        "recommendation": recommendation,
        "requires_human_review": True
    }


def analyze_shortlist(
    shortlist: list[dict[str, Any]],
    requirements: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Analyze the shortlisted candidates.
    """

    analyses = [
        analyze_candidate(candidate, requirements)
        for candidate in shortlist[:10]
    ]

    return sorted(
        analyses,
        key=lambda item: item["overall_score"],
        reverse=True
    )
