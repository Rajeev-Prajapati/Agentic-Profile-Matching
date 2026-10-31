
import uuid

import pytest

from matching_agent import agent, run_matching


@pytest.mark.integration
def test_new_search_workflow():
    thread_id = str(uuid.uuid4())

    jd = """
    Hiring a Python Backend Developer.

    Minimum experience: 4 years.

    Mandatory skills:
    Python, Django, PostgreSQL.

    Preferred skills:
    Docker, Redis.
    """

    result = run_matching(jd, thread_id)

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = agent.get_state(config).values

    assert state.get("requirements")
    assert state.get("shortlist")
    assert state.get("deep_analyses")
    assert state.get("screening_report")
    assert state.get("screening_round") == 3

    assert len(state["shortlist"]) <= 10

    assert (
        "# Candidate Screening Report"
        in state["screening_report"]
    )


@pytest.mark.integration
def test_refinement_preserves_requirements():
    thread_id = str(uuid.uuid4())

    jd = """
    Hiring a Python Backend Developer
    with 4 years of experience.

    Mandatory: Python, Django, PostgreSQL.
    Preferred: Docker, Redis, AWS.
    """

    run_matching(jd, thread_id)

    run_matching(
        "Make Docker mandatory and remove AWS.",
        thread_id
    )

    state = agent.get_state({
        "configurable": {
            "thread_id": thread_id
        }
    }).values

    requirements = state["requirements"]

    must_have = {
        s.lower()
        for s in requirements["must_have"]
    }

    preferred = {
        s.lower()
        for s in requirements["nice_to_have"]
    }

    assert "python" in must_have
    assert "django" in must_have
    assert "docker" in must_have
    assert "aws" not in preferred

    assert state.get("deep_analyses")
    assert state.get("screening_report")
