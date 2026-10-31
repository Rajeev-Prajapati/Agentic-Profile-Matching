
from agents.nodes import request_review_node


def test_review_request():
    state = {
        "user_query": (
            "Verify Docker experience for candidate_002"
        ),
        "selected_candidate_ids": ["candidate_002"],
        "shortlist": [
            {"candidate_id": "candidate_002"}
        ]
    }

    result = request_review_node(state)

    assert result["feedback_status"] == "review_requested"
    assert result["approval_status"] == "pending"
    assert result["review_candidate_ids"] == [
        "candidate_002"
    ]


def test_unknown_candidate():
    state = {
        "user_query": "Review candidate_999",
        "selected_candidate_ids": ["candidate_999"],
        "shortlist": [
            {"candidate_id": "candidate_002"}
        ]
    }

    result = request_review_node(state)

    assert (
        result["feedback_status"]
        == "candidate_selection_required"
    )


def test_missing_candidate_selection():
    state = {
        "user_query": "Request additional review",
        "selected_candidate_ids": [],
        "shortlist": [
            {"candidate_id": "candidate_002"}
        ]
    }

    result = request_review_node(state)

    assert (
        result["feedback_status"]
        == "candidate_selection_required"
    )
