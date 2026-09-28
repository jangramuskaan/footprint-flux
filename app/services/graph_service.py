import networkx as nx

from app.models.graph.node import Node
from app.models.graph.edge import Edge
from app.models.graph.relationship import Relationship


def create_node(
    node_type: str,
    label: str,
    value: str,
) -> Node:
    return Node(
        node_type=node_type,
        label=label,
        value=value,
    )


def create_relationship(
    source: Node,
    target: Node,
    relationship: Relationship,
) -> Edge:
    return Edge(
        source_node_id=source.id,
        target_node_id=target.id,
        relationship=relationship.value,
    )


def build_graph(
    nodes: list[Node],
    edges: list[Edge],
) -> nx.Graph:
    graph = nx.Graph()

    for node in nodes:
        graph.add_node(
            str(node.id),
            node_type=node.node_type,
            label=node.label,
            value=node.value,
        )

    for edge in edges:
        graph.add_edge(
            str(edge.source_node_id),
            str(edge.target_node_id),
            relationship=edge.relationship,
        )

    return graph