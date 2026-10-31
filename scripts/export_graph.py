from pathlib import Path
from matching_agent import agent

output = Path("docs")
output.mkdir(exist_ok=True)

mermaid = agent.get_graph().draw_mermaid()

(output / "state_diagram.md").write_text(
    "```mermaid\n" + mermaid + "\n```\n",
    encoding="utf-8"
)

print("Diagram saved to docs/state_diagram.md")