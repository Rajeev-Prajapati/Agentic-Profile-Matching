
import uuid

from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_core.messages import HumanMessage
from agents.graph import build_graph


agent = build_graph()


def run_matching(query: str, thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = agent.invoke(
        {
            "user_query": query,
            "messages": [
                HumanMessage(content=query)
            ]
        },
        config=config
    )

    return result


def main():
    thread_id = str(uuid.uuid4())

    print("=" * 55)
    print("AGENTIC PROFILE MATCHING ASSISTANT")
    print("=" * 55)
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not query:
            continue

        try:
            result = run_matching(
                query,
                thread_id
            )

            print("\nAgent:")
            print(result.get(
                "report",
                "No response generated."
            ))
            print()

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()
