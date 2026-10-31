
from agents.graph import build_graph


def test_screening_graph_compiles():
    graph = build_graph()

    assert graph is not None


def test_screening_nodes_registered():
    graph = build_graph()

    nodes = graph.get_graph().nodes

    assert "deep_analysis" in nodes
    assert "screening_report" in nodes



def test_screening_edges():
    graph = build_graph()

    graph_data = graph.get_graph(xray=True)

    print("\n--- Graph Nodes ---")
    for node in graph_data.nodes:
        print(node)

    print("\n--- Graph Edges ---")
    for edge in graph_data.edges:
        print(
            edge.source,
            "->",
            edge.target,
            "conditional:",
            edge.conditional
        )

    edge_pairs = {
        (edge.source, edge.target)
        for edge in graph_data.edges
    }

    expected_edges = {
        ("rank_candidates", "deep_analysis"),
        ("deep_analysis", "screening_report"),
        ("screening_report", "__end__")
    }

    missing_edges = expected_edges - edge_pairs

    assert not missing_edges, (
        f"Missing graph edges: {missing_edges}"
    )

