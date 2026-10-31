
from datetime import datetime, timezone
from typing import Any


def format_score(value: Any) -> str:
    if value is None:
        return "Not available"
    return f"{value:.2f}/100"


def format_items(items: list[str]) -> str:
    if not items:
        return "None recorded"
    return ", ".join(items)


def generate_recommendation_report(
    analyses: list[dict[str, Any]],
    requirements: dict[str, Any]
) -> str:
    """
    Generate a screening recommendation report
    from analyzed candidates.
    """

    role = requirements.get("role", "Not specified")
    must_have = requirements.get("must_have", [])
    nice_to_have = requirements.get("nice_to_have", [])
    min_experience = requirements.get("min_experience", 0)

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    )

    lines = [
        "# Candidate Screening Report",
        "",
        f"**Generated:** {timestamp}",
        f"**Role:** {role}",
        f"**Minimum Experience:** {min_experience} years",
        "",
        "## Job Requirements",
        "",
        f"**Mandatory Skills:** {format_items(must_have)}",
        f"**Preferred Skills:** {format_items(nice_to_have)}",
        "",
        "## Screening Summary",
        "",
        f"**Candidates Analyzed:** {len(analyses)}",
        ""
    ]

    counts = {
        "Strong Match": 0,
        "Needs Review": 0,
        "Low Match": 0
    }

    for candidate in analyses:
        label = candidate.get(
            "recommendation",
            "Needs Review"
        )
        counts[label] = counts.get(label, 0) + 1

    lines.extend([
        f"- Strong Match: {counts['Strong Match']}",
        f"- Needs Review: {counts['Needs Review']}",
        f"- Low Match: {counts['Low Match']}",
        "",
        "## Candidate Ranking",
        "",
        "| Rank | Candidate | Score | Recommendation |",
        "|---|---|---:|---|"
    ])

    ranked = sorted(
        analyses,
        key=lambda c: c.get("overall_score", 0),
        reverse=True
    )

    for index, candidate in enumerate(ranked, 1):
        lines.append(
            f"| {index} | {candidate['candidate_id']} "
            f"| {candidate['overall_score']:.2f} "
            f"| {candidate['recommendation']} |"
        )

    lines.extend([
        "",
        "## Detailed Candidate Analysis",
        ""
    ])

    for index, candidate in enumerate(ranked, 1):
        breakdown = candidate.get(
            "score_breakdown",
            {}
        )

        years = candidate.get("years_experience")
        experience_text = (
            f"{years} years"
            if years is not None
            else "Not established"
        )

        lines.extend([
            f"### {index}. {candidate['candidate_id']}",
            "",
            f"**Overall Score:** {format_score(candidate.get('overall_score'))}",
            f"**Screening Recommendation:** {candidate.get('recommendation', 'Needs Review')}",
            f"**Stated Experience:** {experience_text}",
            "",
            "**Score Breakdown**",
            "",
            f"- Mandatory skills: {format_score(breakdown.get('mandatory'))}",
            f"- Experience: {format_score(breakdown.get('experience'))}",
            f"- Semantic similarity: {format_score(breakdown.get('semantic'))}",
            f"- Preferred skills: {format_score(breakdown.get('preferred'))}",
            "",
            f"**Matched Skills:** {format_items(candidate.get('matched_skills', []))}",
            f"**Missing Mandatory Skill Evidence:** {format_items(candidate.get('missing_skill_evidence', []))}",
            f"**Unavailable Evidence:** {format_items(candidate.get('missing_evidence', []))}",
            "",
            "---",
            ""
        ])

    lines.extend([
        "## Human Review",
        "",
        "All recommendations are preliminary screening indicators.",
        "Resume mentions and extracted experience require verification.",
        "No automated hire/no-hire decision is made.",
        "",
        "**Next Action:** Review evidence, request clarification where needed, and approve candidates for interviews."
    ])

    return "\n".join(lines)
