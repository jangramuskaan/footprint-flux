from uuid import uuid4

from app.models.graph.node import Node
from app.models.graph.edge import Edge
from app.services.graph_service import build_graph


def test_build_graph():
    node1 = Node(
        id=uuid4(),
        node_type="github",
        label="Muskaan",
        value="jangramuskaan",
    )

    node2 = Node(
        id=uuid4(),
        node_type="profile",
        label="Profile",
        value="jangramuskaan",
    )

    edge = Edge(
        source_node_id=node1.id,
        target_node_id=node2.id,
        relationship="same_username",
    )

    graph = build_graph([node1, node2], [edge])

    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() == 1


def test_graph_contains_relationship():
    node1 = Node(
        id=uuid4(),
        node_type="github",
        label="GitHub",
        value="jangramuskaan",
    )

    node2 = Node(
        id=uuid4(),
        node_type="profile",
        label="Other Profile",
        value="jangramuskaan",
    )

    edge = Edge(
        source_node_id=node1.id,
        target_node_id=node2.id,
        relationship="same_username",
    )

    graph = build_graph([node1, node2], [edge])

    assert graph.has_edge(
        str(node1.id),
        str(node2.id),
    )

    assert graph[
        str(node1.id)
    ][str(node2.id)]["relationship"] == "same_username"