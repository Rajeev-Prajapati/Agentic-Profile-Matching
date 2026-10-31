
from agents.state import AgentState
from langchain_core.messages import HumanMessage


def test_agent_state_structure():
    state: AgentState = {
        "messages": [
            HumanMessage(
                content="Find React developers"
            )
        ],
        "user_query": "Find React developers",
        "intent": "search",
        "job_description": "React developer with 3 years",
        "requirements": {
            "must_have": ["React"],
            "min_experience": 3
        },
        "retrieved_candidates": [],
        "shortlist": [],
        "ranking_reasoning": {},
        "previous_ranking": [],
        "screening_round": 1,
        "report": "",
        "feedback": "",
        "feedback_status": "pending"
    }

    assert state["intent"] == "search"
    assert state["screening_round"] == 1
    assert state["requirements"]["must_have"] == ["React"]
    assert len(state["messages"]) == 1

""" Run:

```powershell
python -m pytest tests/test_agent_state.py -v
```

Expected output:

```text
tests/test_agent_state.py::test_agent_state_structure PASSED

1 passed
```

## 6.5 Test conversation memory with a small LangGraph

This second test verifies that `add_messages` works inside a real graph.

Create:

```text
tests/test_agent_memory.py
```

Add:

<CodeBlock language="python" editable> """

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, AIMessage

from agents.state import AgentState


def chat_node(state: AgentState):
    return {
        "messages": [
            AIMessage(content="Request received")
        ]
    }


def test_conversation_memory():
    builder = StateGraph(AgentState)

    builder.add_node("chat", chat_node)
    builder.add_edge(START, "chat")
    builder.add_edge("chat", END)

    graph = builder.compile(
        checkpointer=InMemorySaver()
    )

    config = {
        "configurable": {
            "thread_id": "test-session-001"
        }
    }

    graph.invoke(
        {
            "messages": [
                HumanMessage(content="Find React developers")
            ]
        },
        config=config
    )

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="Compare top 3")
            ]
        },
        config=config
    )

    assert len(result["messages"]) == 4

    assert result["messages"][0].content == (
        "Find React developers"
    )

    assert result["messages"][2].content == (
        "Compare top 3"
    )

""" Run:

```powershell
python -m pytest tests/test_agent_memory.py -v
```

Expected:

```text
tests/test_agent_memory.py::test_conversation_memory PASSED

1 passed
```

This verifies that LangGraph retains previous messages when using the same `thread_id` and the same checkpointer instance.

**Note:** `InMemorySaver` stores checkpoints only while the Python process is running. We'll use a persistent checkpointer later if conversations need to survive application restarts.

## 6.6 Run both tests

```powershell
python -m pytest tests/test_agent_state.py tests/test_agent_memory.py -v
```

Expected:

```text
2 passed
```

## Current project progress

| Step | Status |
|---|---|
| 1. Environment setup | <icon name="check-circle" color="success" inline/> Completed |
| 2. Project structure | <icon name="check-circle" color="success" inline/> Completed |
| 3. Resume ingestion | <icon name="check-circle" color="success" inline/> Completed |
| 4. RAG search | <icon name="check-circle" color="success" inline/> Completed |
| 5. Agent tools | <icon name="check-circle" color="success" inline/> Completed |
| 6. LangGraph state | Ready to test |
| 7. LangGraph workflow | Next |

### Next: Step 7 — Building the LangGraph Workflow

Once both tests pass, we will create `agents/nodes.py`, `agents/graph.py`, and `matching_agent.py` to implement:

**START → Parse JD → Extract Requirements → Search Resumes → Rank Candidates → Generate Report → Human Feedback → END**

We will test the graph node by node before adding conditional routing and conversational refinement. """