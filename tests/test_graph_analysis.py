from uuid import uuid4

from app.models.graph.node import Node
from app.models.graph.edge import Edge

from app.services.graph_service import (
    build_graph,
    get_connected_nodes,
    get_relationships,
)


def create_test_graph():
    """
    Create a small test graph.

    Graph structure:

        GitHub -------- Other Profile
           |
           |
        Website

    node1 is connected to node2 and node3.
    """

    # ---------------------------------------------------------
    # Create nodes
    # ---------------------------------------------------------

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

    node3 = Node(
        id=uuid4(),
        node_type="website",
        label="Personal Website",
        value="jangramuskaan",
    )

    # ---------------------------------------------------------
    # Create relationships
    # ---------------------------------------------------------

    edge1 = Edge(
        source_node_id=node1.id,
        target_node_id=node2.id,
        relationship="same_username",
    )

    edge2 = Edge(
        source_node_id=node1.id,
        target_node_id=node3.id,
        relationship="related_profile",
    )

    # ---------------------------------------------------------
    # Build graph
    # ---------------------------------------------------------

    graph = build_graph(
        [node1, node2, node3],
        [edge1, edge2],
    )

    return graph, node1, node2, node3


def test_get_connected_nodes():
    """
    node1 should be connected to node2 and node3.
    """

    graph, node1, node2, node3 = create_test_graph()

    connected = get_connected_nodes(
        graph,
        str(node1.id),
    )

    # node1 should have exactly two connections
    assert len(connected) == 2

    # node2 should be connected
    assert str(node2.id) in connected

    # node3 should be connected
    assert str(node3.id) in connected


def test_get_relationships():
    """
    node1 should have two relationships.
    """

    graph, node1, node2, node3 = create_test_graph()

    relationships = get_relationships(
        graph,
        str(node1.id),
    )

    # node1 has two relationships
    assert len(relationships) == 2

    # Convert relationships to a set of relationship types
    relationship_types = {
        item["relationship"]
        for item in relationships
    }

    assert "same_username" in relationship_types
    assert "related_profile" in relationship_types


def test_unknown_node_returns_empty():
    """
    An unknown node ID should return empty results.
    """

    graph, node1, node2, node3 = create_test_graph()

    unknown_node_id = str(uuid4())

    connected = get_connected_nodes(
        graph,
        unknown_node_id,
    )

    relationships = get_relationships(
        graph,
        unknown_node_id,
    )

    assert connected == []
    assert relationships == []