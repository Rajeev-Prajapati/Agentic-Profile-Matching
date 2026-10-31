
from services.advanced_ranker import (
    skill_matches,
    extract_experience_years,
    score_candidate
)


def test_skill_matching():
    resume = """
    Experienced Python developer with Django,
    PostgreSQL, Docker and Redis.
    """

    matches = skill_matches(
        resume,
        ["Python", "Django", "Docker", "AWS"]
    )

    assert matches == [
        "Python", "Django", "Docker"
    ]


def test_experience_extraction():
    resume = """
    Backend engineer with 5+ years of experience.
    """

    years = extract_experience_years(resume)

    assert years == 5.0


def test_missing_experience():
    resume = """
    Python developer with Django and PostgreSQL.
    """

    assert extract_experience_years(resume) is None


def test_candidate_scoring():
    candidate = {
        "candidate_id": "candidate_001",
        "resume": """
        Python developer with 5 years of experience.
        Skills: Python, Django, PostgreSQL, Docker.
        """,
        "distance": 0.20
    }

    requirements = {
        "must_have": [
            "Python", "Django", "PostgreSQL"
        ],
        "nice_to_have": [
            "Docker", "AWS"
        ],
        "min_experience": 4
    }

    result = score_candidate(
        candidate, requirements
    )

    assert result["score_breakdown"]["mandatory"] == 100
    assert result["score_breakdown"]["experience"] == 100
    assert result["score_breakdown"]["semantic"] == 80
    assert result["score_breakdown"]["preferred"] == 50

    assert result["score"] == 88.5
    assert result["experience_verified"] is True
