
from services.recommendation_service import (
    generate_recommendation_report
)


def test_generate_recommendation_report():

    requirements = {
        "role": "Python Backend Developer",
        "must_have": ["Python", "Django", "PostgreSQL"],
        "nice_to_have": ["Docker", "Redis"],
        "min_experience": 4
    }

    analyses = [
        {
            "candidate_id": "candidate_001",
            "overall_score": 91.5,
            "score_breakdown": {
                "mandatory": 100,
                "experience": 100,
                "semantic": 82.5,
                "preferred": 100
            },
            "matched_skills": [
                "Python", "Django", "PostgreSQL", "Docker"
            ],
            "missing_skill_evidence": [],
            "years_experience": 5,
            "missing_evidence": [],
            "recommendation": "Strong Match"
        },
        {
            "candidate_id": "candidate_002",
            "overall_score": 68.0,
            "score_breakdown": {
                "mandatory": 66.67,
                "experience": 75,
                "semantic": 80,
                "preferred": 50
            },
            "matched_skills": ["Python", "Django"],
            "missing_skill_evidence": ["PostgreSQL"],
            "years_experience": 3,
            "missing_evidence": [],
            "recommendation": "Low Match"
        }
    ]

    report = generate_recommendation_report(
        analyses,
        requirements
    )

    assert "# Candidate Screening Report" in report
    assert "Python Backend Developer" in report
    assert "candidate_001" in report
    assert "candidate_002" in report
    assert "Strong Match: 1" in report
    assert "Low Match: 1" in report
    assert "## Human Review" in report
