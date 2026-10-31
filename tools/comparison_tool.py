
from tools.rag_tool import collection
from services.candidate_ranker import rank_candidates

def compare_candidates(
    candidate_ids: list[str],
    shortlist: list[dict]
):
    lookup = {
        c["candidate_id"]: c
        for c in shortlist
    }

    return [
        {
            "candidate_id": cid,
            "score": lookup[cid].get("score"),
            "strengths": lookup[cid].get(
                "strengths", []
            ),
            "gaps": lookup[cid].get(
                "gaps", []
            )
        }
        for cid in candidate_ids
        if cid in lookup
    ]