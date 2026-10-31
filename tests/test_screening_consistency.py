
from services.deep_analyzer import analyze_shortlist
from services.recommendation_service import (
    generate_recommendation_report
)


def test_screening_consistency():
    requirements = {
        "role": "Python Backend Developer",
        "must_have": ["Python", "Django"],
        "nice_to_have": ["Docker"],
        "min_experience": 3
    }

    candidates = [
        {
            "candidate_id": "candidate_001",
            "resume": (
                "Python Django Docker developer "
                "with 5 years of experience."
            ),
            "distance": 0.2
        },
        {
            "candidate_id": "candidate_002",
            "resume": (
                "Python developer with "
                "2 years of experience."
            ),
            "distance": 0.4
        }
    ]

    analyses = analyze_shortlist(
        candidates,
        requirements
    )

    report = generate_recommendation_report(
        analyses,
        requirements
    )

    assert len(analyses) == 2

    for analysis in analyses:
        assert analysis["candidate_id"] in report
        assert 0 <= analysis["overall_score"] <= 100
        assert analysis["requires_human_review"] is True

    assert (
        analyses[0]["overall_score"]
        >= analyses[1]["overall_score"]
    )

    assert "## Human Review" in report
