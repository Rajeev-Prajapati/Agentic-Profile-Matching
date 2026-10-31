
from services.deep_analyzer import (
    analyze_candidate,
    analyze_shortlist
)


REQUIREMENTS = {
    "must_have": [
        "Python",
        "Django",
        "PostgreSQL"
    ],
    "nice_to_have": [
        "Docker",
        "Redis"
    ],
    "min_experience": 4
}


def test_strong_match():
    candidate = {
        "candidate_id": "candidate_001",
        "resume": (
            "Python Django PostgreSQL Docker Redis. "
            "5 years of experience."
        ),
        "distance": 0.2
    }

    result = analyze_candidate(
        candidate,
        REQUIREMENTS
    )

    assert result["recommendation"] == "Strong Match"
    assert result["requires_human_review"] is True


def test_needs_review():
    candidate = {
        "candidate_id": "candidate_002",
        "resume": (
            "Python Django Docker. "
            "2 years of experience."
        ),
        "distance": 0.3
    }

    result = analyze_candidate(
        candidate,
        REQUIREMENTS
    )

    assert result["recommendation"] == "Needs Review"


def test_low_match():
    candidate = {
        "candidate_id": "candidate_003",
        "resume": (
            "Java Spring Boot developer. "
            "3 years of experience."
        ),
        "distance": 0.5
    }

    result = analyze_candidate(
        candidate,
        REQUIREMENTS
    )

    assert result["recommendation"] == "Low Match"


def test_analyze_shortlist():
    candidates = [
        {
            "candidate_id": "candidate_001",
            "resume": (
                "Python Django PostgreSQL Docker. "
                "5 years of experience."
            ),
            "distance": 0.2
        },
        {
            "candidate_id": "candidate_002",
            "resume": (
                "Python developer. "
                "2 years of experience."
            ),
            "distance": 0.4
        }
    ]

    results = analyze_shortlist(
        candidates,
        REQUIREMENTS
    )

    assert len(results) == 2
    assert results[0]["candidate_id"] == "candidate_001"
