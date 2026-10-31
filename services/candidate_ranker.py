import re


def has_skill(text: str, skill: str) -> bool:
    pattern = (
        r"(?<!\w)" +
        re.escape(skill) +
        r"(?!\w)"
    )
    return bool(re.search(pattern, text, re.I))


def score_skills(text: str, skills: list[str]):
    if not skills:
        return 100.0, []

    matched = [
        skill for skill in skills
        if has_skill(text, skill)
    ]

    missing = [
        skill for skill in skills
        if skill not in matched
    ]

    return 100 * len(matched) / len(skills), missing


def rank_candidates(candidates, requirements):
    must_have = requirements.get("must_have", [])
    nice_to_have = requirements.get("nice_to_have", [])

    ranked = []

    for candidate in candidates:
        text = candidate["resume"]

        must_score, missing = score_skills(
            text, must_have
        )

        nice_score, _ = score_skills(
            text, nice_to_have
        )

        # Chroma default L2 distance is not a percentage.
        # This is a provisional normalized retrieval score.
        distance = candidate.get("distance", 2.0)
        semantic_score = max(
            0, min(100, 100 * (1 - distance / 2))
        )

        # Unknown experience receives no points until
        # verified structured experience is available.
        years = candidate.get("years_experience")
        required = requirements.get("min_experience", 0)

        if required <= 0:
            experience_score = 100
        elif years is None:
            experience_score = 0
        else:
            experience_score = min(
                100, 100 * years / required
            )

        score = (
            0.45 * must_score
            + 0.25 * experience_score
            + 0.20 * semantic_score
            + 0.10 * nice_score
        )

        ranked.append({
            **candidate,
            "score": round(score, 2),
            "strengths": [
                skill for skill in must_have
                if skill not in missing
            ],
            "gaps": missing,
            "experience_verified": years is not None
        })

    return sorted(
        ranked,
        key=lambda c: c["score"],
        reverse=True
    )