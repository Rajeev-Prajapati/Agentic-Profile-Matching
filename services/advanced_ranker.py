
import re
from typing import Any


WEIGHTS = {
    "mandatory": 0.40,
    "experience": 0.25,
    "semantic": 0.20,
    "preferred": 0.15
}


def skill_matches(resume: str, skills: list[str]) -> list[str]:
    """Find explicitly mentioned skills."""

    matches = []

    for skill in skills:
        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, resume, re.IGNORECASE):
            matches.append(skill)

    return matches


def calculate_skill_score(
    matched: list[str],
    required: list[str]
) -> float:
    if not required:
        return 100.0

    return round(
        len(matched) / len(required) * 100,
        2
    )


def extract_experience_years(resume: str) -> float | None:
    """
    Extract explicitly stated years of experience.
    Does not infer years from employment dates.
    """

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+of\s+experience",
        r"experience\s*[:\-]\s*(\d+(?:\.\d+)?)\s*\+?\s*years?",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+(?:in|with)\s+\w+"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            resume,
            re.IGNORECASE
        )

        if match:
            return float(match.group(1))

    return None


def calculate_experience_score(
    actual_years: float | None,
    required_years: float
) -> float | None:

    if required_years <= 0:
        return 100.0

    if actual_years is None:
        return None

    return round(
        min(actual_years / required_years, 1.0) * 100,
        2
    )


def normalize_semantic_score(
    distance: float | None
) -> float | None:
    """
    Converts cosine distance to similarity percentage.

    Only valid if Chroma collection uses cosine distance.
    """

    if distance is None:
        return None

    similarity = 1 - distance

    return round(
        max(0, min(similarity, 1)) * 100,
        2
    )


def score_candidate(
    candidate: dict[str, Any],
    requirements: dict[str, Any]
) -> dict[str, Any]:

    resume = candidate.get("resume", "")

    must_have = requirements.get("must_have", [])
    nice_to_have = requirements.get("nice_to_have", [])

    matched_must = skill_matches(resume, must_have)
    matched_nice = skill_matches(resume, nice_to_have)

    mandatory_score = calculate_skill_score(
        matched_must,
        must_have
    )

    preferred_score = calculate_skill_score(
        matched_nice,
        nice_to_have
    )

    actual_years = extract_experience_years(resume)

    experience_score = calculate_experience_score(
        actual_years,
        requirements.get("min_experience", 0)
    )

    semantic_score = normalize_semantic_score(
        candidate.get("distance")
    )

    components = {
        "mandatory": mandatory_score,
        "experience": experience_score,
        "semantic": semantic_score,
        "preferred": preferred_score
    }

    available_weight = sum(
        WEIGHTS[key]
        for key, value in components.items()
        if value is not None
    )

    weighted_total = sum(
        value * WEIGHTS[key]
        for key, value in components.items()
        if value is not None
    )

    score = (
        weighted_total / available_weight
        if available_weight else 0.0
    )

    gaps = [
        skill for skill in must_have
        if skill not in matched_must
    ]

    return {
        **candidate,
        "score": round(score, 2),
        "score_breakdown": components,
        "strengths": matched_must + matched_nice,
        "gaps": gaps,
        "years_experience": actual_years,
        "experience_verified": actual_years is not None,
        "missing_evidence": [
            name
            for name, value in components.items()
            if value is None
        ]
    }


def rank_candidates(
    candidates: list[dict[str, Any]],
    requirements: dict[str, Any]
) -> list[dict[str, Any]]:

    ranked = [
        score_candidate(candidate, requirements)
        for candidate in candidates
    ]

    return sorted(
        ranked,
        key=lambda item: item["score"],
        reverse=True
    )
