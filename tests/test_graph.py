
import uuid

from matching_agent import agent


def test_complete_workflow():
    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    jd = """
    Hiring a React Developer with 3+ years
    of experience. React and JavaScript required.
    Docker preferred.
    """

    result = agent.invoke(
        {"user_query": jd},
        config=config
    )

    assert result["requirements"]
    assert "shortlist" in result
    assert "report" in result
    assert "Candidate Matching Report" in result["report"]

    snapshot = agent.get_state(config)

    assert snapshot.next == ("human_feedback",)
