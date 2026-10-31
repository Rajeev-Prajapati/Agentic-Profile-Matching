import pandas as pd
import streamlit as st
import uuid

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

from matching_agent import agent, run_matching


st.set_page_config(
    page_title="Agentic Profile Matching",
    page_icon="🔎",
    layout="wide"
)


# Persist the LangGraph thread across Streamlit reruns.
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def get_agent_state():
    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id
        }
    }

    snapshot = agent.get_state(config)
    return snapshot.values or {}


def send_message(message: str):
    st.session_state.chat_history.append({
        "role": "user",
        "content": message
    })

    try:
        result = run_matching(
            message,
            st.session_state.thread_id
        )

        response = result.get(
            "report",
            "No response generated."
        )

    except Exception as error:
        response = f"Error: {error}"

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })


# Sidebar
with st.sidebar:
    st.title("🔎 Profile Matching")
    st.caption("LangGraph + Groq + ChromaDB")

    if st.button("New Conversation"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.rerun()

    st.divider()

    state = get_agent_state()
    requirements = state.get("requirements", {})

    st.subheader("Current Requirements")

    if requirements:
        st.write("**Role:**", requirements.get("role", "N/A"))
        st.write(
            "**Must-have:**",
            ", ".join(requirements.get("must_have", []))
        )
        st.write(
            "**Nice-to-have:**",
            ", ".join(requirements.get("nice_to_have", []))
        )
        st.write(
            "**Experience:**",
            f"{requirements.get('min_experience', 0)}+ years"
        )
    else:
        st.info("Enter a job description to begin.")

    st.divider()

    approval = state.get("approval_status", "pending")
    st.write("**Approval status:**", approval)


# Main area
st.title("Agentic Profile Matching Assistant")
st.caption(
    "Search, rank, compare, and review candidates "
    "using natural language."
)

state = get_agent_state()
shortlist = state.get("shortlist", [])

col1, col2, col3 = st.columns(3)

col1.metric(
    "Retrieved Candidates",
    len(state.get("retrieved_candidates", []))
)
col2.metric("Shortlisted", len(shortlist))
col3.metric(
    "Screening Round",
    state.get("screening_round", 0)
)

tab1, tab2, tab3 = st.tabs([
    "💬 Agent Chat",
    "📊 Candidate Shortlist",
    "📋 Screening Dashboard"
])

with tab1:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Enter a job description or ask about candidates..."
    )

    if prompt:
        with st.spinner("Agent is processing..."):
            send_message(prompt)
        st.rerun()

with tab2:
    if shortlist:
        rows = []

        
        for index, candidate in enumerate(shortlist, 1):
            breakdown = candidate.get("score_breakdown", {})

            rows.append({
                "Rank": index,
                "Candidate ID": candidate["candidate_id"],
                "Overall Score": candidate.get("score"),
                "Mandatory Skills": breakdown.get("mandatory"),
                "Experience": breakdown.get("experience"),
                "Semantic Similarity": breakdown.get("semantic"),
                "Preferred Skills": breakdown.get("preferred"),
                "Matched Skills": ", ".join(
                    candidate.get("strengths", [])
                ),
                "Missing Evidence": ", ".join(
                    candidate.get("missing_evidence", [])
                )
            })


        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Candidate Actions")

        candidate_ids = [
            candidate["candidate_id"]
            for candidate in shortlist
        ]

        selected_candidate = st.selectbox(
            "Select a candidate",
            candidate_ids
        )

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("Generate Interview Questions"):
                send_message(
                    "Generate 5 technical interview questions "
                    f"for {selected_candidate}"
                )
                st.rerun()

        with col_b:
            if st.button("Explain Candidate Ranking"):
                send_message(
                    f"Explain the ranking of {selected_candidate}"
                )
                st.rerun()

        st.divider()
        
        st.subheader("Human Review")

        review_notes = st.text_area(
            "Review notes",
            placeholder=(
                "Example: Verify candidate's "
                "production Docker experience."
            ),
            key="review_notes_input"
        )

        if st.button("Request Additional Review"):
            if not review_notes.strip():
                st.warning(
                    "Please enter review notes."
                )
            else:
                message = (
                    f"Request additional review for "
                    f"{selected_candidate}. "
                    f"Review notes: {review_notes}"
                )

                send_message(message)
                st.rerun()

        review_status = state.get(
            "feedback_status",
            "pending"
        )

        if review_status == "review_requested":
            st.warning(
                "Additional candidate review requested."
            )

            st.write(
                "**Candidates:**",
                ", ".join(
                    state.get(
                        "review_candidate_ids",
                        []
                    )
                )
            )

            st.write(
                "**Notes:**",
                state.get("review_notes", "")
            )


        if state.get("approval_status") == "approved":
            st.success("Shortlist approved for screening.")
        elif st.button(
            "Approve Shortlist",
            type="primary"
        ):
            send_message("Approve the shortlist")
            st.rerun()

    else:
        st.info(
            "No candidates shortlisted yet. "
            "Start by entering a job description."
        )



# ============================================
# TAB 3 — SCREENING DASHBOARD
# ============================================

with tab3:
    st.header("Candidate Screening Dashboard")

    # Read screening data from LangGraph state
    state = get_agent_state()

    analyses = state.get("deep_analyses", [])
    screening_report = state.get(
        "screening_report", ""
    )

    approval_status = state.get(
        "approval_status", "pending"
    )

    review_ids = state.get(
        "review_candidate_ids", []
    )

    if not analyses:
        st.info(
            "No screening results available. "
            "Submit a job description in Agent Chat."
        )

    else:
        # ------------------------------------
        # 1. Screening summary
        # ------------------------------------

        total = len(analyses)

        strong = sum(
            a.get("recommendation") == "Strong Match"
            for a in analyses
        )

        needs_review = sum(
            a.get("recommendation") == "Needs Review"
            for a in analyses
        )

        low_match = sum(
            a.get("recommendation") == "Low Match"
            for a in analyses
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Analyzed", total)
        col2.metric("Strong Match", strong)
        col3.metric("Needs Review", needs_review)
        col4.metric("Low Match", low_match)

        st.divider()

        # ------------------------------------
        # 2. Candidate screening table
        # ------------------------------------

        st.subheader("Screening Results")

        rows = []

        for index, candidate in enumerate(
            analyses, start=1
        ):
            breakdown = candidate.get(
                "score_breakdown", {}
            )

            rows.append({
                "Rank": index,
                "Candidate ID": candidate["candidate_id"],
                "Overall Score": candidate.get(
                    "overall_score"
                ),
                "Mandatory Skills": breakdown.get(
                    "mandatory"
                ),
                "Experience": breakdown.get(
                    "experience"
                ),
                "Semantic Similarity": breakdown.get(
                    "semantic"
                ),
                "Preferred Skills": breakdown.get(
                    "preferred"
                ),
                "Recommendation": candidate.get(
                    "recommendation"
                ),
                "Review Status": (
                    "Review Requested"
                    if candidate["candidate_id"] in review_ids
                    else "Not Flagged"
                )
            })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ------------------------------------
        # 3. Detailed candidate analysis
        # ------------------------------------

        st.subheader("Candidate Details")

        candidate_ids = [
            a["candidate_id"]
            for a in analyses
        ]

        selected_id = st.selectbox(
            "Select candidate to inspect",
            candidate_ids,
            key="screening_candidate_select"
        )

        selected = next(
            a for a in analyses
            if a["candidate_id"] == selected_id
        )

        st.write(
            "**Recommendation:**",
            selected.get("recommendation")
        )

        st.write(
            "**Overall Score:**",
            selected.get("overall_score")
        )

        years = selected.get("years_experience")

        st.write(
            "**Stated Experience:**",
            f"{years} years"
            if years is not None
            else "Not established"
        )

        st.write(
            "**Matched Skills:**",
            ", ".join(
                selected.get("matched_skills", [])
            ) or "None recorded"
        )

        st.write(
            "**Missing Mandatory Skill Evidence:**",
            ", ".join(
                selected.get(
                    "missing_skill_evidence", []
                )
            ) or "None recorded"
        )

        st.write(
            "**Unavailable Evidence:**",
            ", ".join(
                selected.get("missing_evidence", [])
            ) or "None recorded"
        )

        # ------------------------------------
        # 4. Human review status
        # ------------------------------------

        st.divider()
        st.subheader("Human Review")

        st.write(
            "**Approval Status:**",
            approval_status
        )

        if review_ids:
            st.warning(
                "Additional review requested for: "
                + ", ".join(review_ids)
            )

            st.write(
                "**Review Notes:**",
                state.get("review_notes", "")
            )

        if approval_status == "approved":
            st.success(
                "Shortlist approved for interview screening."
            )

        else:
            st.info(
                "Screening results are pending human approval."
            )

        # ------------------------------------
        # 5. Screening report download
        # ------------------------------------

        st.divider()
        st.subheader("Screening Report")

        if screening_report:
            with st.expander(
                "Preview Screening Report"
            ):
                st.markdown(screening_report)

            st.download_button(
                label="Download Screening Report",
                data=screening_report,
                file_name="candidate_screening_report.md",
                mime="text/markdown"
            )

        else:
            st.warning(
                "Screening report has not been generated."
            )
