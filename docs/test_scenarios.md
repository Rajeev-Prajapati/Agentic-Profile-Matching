
# End-to-End Test Scenarios

## Scenario 1 — New Job Description

Input:
Submit a Python Backend Developer job description.

Expected:
Requirements extracted, resumes retrieved, top 10 shortlisted, screening report generated.

## Scenario 2 — Requirement Refinement

Input:
Make Docker mandatory and remove AWS.

Expected:
Existing requirements preserved, changes applied, ranking recalculated.

## Scenario 3 — Candidate Comparison

Input:
Compare the top 3 candidates.

Expected:
Candidate IDs, scores, strengths, and missing evidence displayed.

## Scenario 4 — Human Review

Input:
Request additional review for candidate_002.

Expected:
Review request recorded and approval status set to pending.

## Scenario 5 — Shortlist Approval

Input:
Approve the shortlist for interview screening.

Expected:
Approval status updated to approved.

## Execution Results

| Scenario | Status | Notes |
|---|---|---|
| New JD | Not recorded | |
| Refinement | Not recorded | |
| Comparison | Not recorded | |
| Human review | Not recorded | |
| Approval | Not recorded | |

Update the status and notes after running each test.

## Validation Notes

Passing functional tests does not establish candidate matching accuracy.

Before real-world deployment, evaluate retrieval quality, scoring reliability, evidence completeness, fairness, privacy, and human-review controls.
```
