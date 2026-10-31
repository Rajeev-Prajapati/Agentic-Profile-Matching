from services.candidate_ranker import rank_candidates


def test_candidate_ranking():
    candidates = [
        {
            "candidate_id": "A",
            "resume": "React JavaScript TypeScript",
            "distance": 0.2,
            "years_experience": 4
        },
        {
            "candidate_id": "B",
            "resume": "Python Django",
            "distance": 1.2,
            "years_experience": 2
        }
    ]

    requirements = {
        "must_have": ["React", "JavaScript"],
        "nice_to_have": ["TypeScript"],
        "min_experience": 3
    }

    result = rank_candidates(
        candidates, requirements
    )

    assert len(result) == 2
    assert result[0]["candidate_id"] == "A"
    assert result[0]["score"] > result[1]["score"]