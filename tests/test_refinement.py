
from services.requirement_refiner import update_requirements
from agents.nodes import ranking_changes


def test_add_mandatory_skill():
    current = {
        "must_have": ["React", "JavaScript"],
        "nice_to_have": ["Docker", "AWS"],
        "min_experience": 3
    }

    changes = {
        "add_must_have": ["Docker"],
        "remove_nice_to_have": ["AWS", "Docker"]
    }

    result = update_requirements(
        current, changes
    )

    assert "Docker" in result["must_have"]
    assert "Docker" not in result["nice_to_have"]
    assert "AWS" not in result["nice_to_have"]
    assert "React" in result["must_have"]
    assert result["min_experience"] == 3


def test_original_requirements_unchanged():
    original = {
        "must_have": ["React"],
        "nice_to_have": [],
        "min_experience": 3
    }

    update_requirements(
        original,
        {"add_must_have": ["Docker"]}
    )

    assert original["must_have"] == ["React"]


def test_ranking_changes():
    previous = [
        {"candidate_id": "A", "score": 90},
        {"candidate_id": "B", "score": 85}
    ]

    current = [
        {"candidate_id": "B", "score": 95},
        {"candidate_id": "A", "score": 88}
    ]

    changes = ranking_changes(previous, current)

    assert any("B: Moved up 1" in x for x in changes)
    assert any("A: Moved down 1" in x for x in changes)
