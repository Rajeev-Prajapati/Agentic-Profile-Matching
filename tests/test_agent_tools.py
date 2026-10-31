
from tools.requirement_tool import extract_requirements
from tools.comparison_tool import compare_candidates
from tools.interview_tool import generate_interview_questions
from tools.rag_tool import collection


def test_extract_requirements():
    jd = """
    React Developer with 3+ years experience.
    React and JavaScript are mandatory.
    Docker and AWS are preferred.
    """

    result = extract_requirements(jd)

    assert result["min_experience"] >= 3
    assert result["must_have"]

    print("Requirement extraction passed")


def test_compare_candidates():
    ids = collection.get(limit=3)["ids"]

    assert len(ids) >= 2, "Need at least 2 resumes"

    result = compare_candidates(ids[:2])

    assert len(result) == 2
    assert all(
        "candidate_id" in c for c in result
    )

    print("Candidate comparison passed")


def test_generate_interview_questions():
    ids = collection.get(limit=1)["ids"]

    assert ids, "No indexed candidates found"

    result = generate_interview_questions(ids[0])

    assert len(result["questions"]) == 5
    assert all(result["questions"])

    print("Interview question generation passed")
