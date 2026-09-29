import networkx as nx

from app.models.graph.node import Node
from app.models.graph.edge import Edge


def _normalize_nodes(nodes):
    """
    Convert different possible node input formats into a list of Node objects.

    Supported:
        build_graph([node1, node2])
        build_graph((node1, node2))
        build_graph(node1, node2)
    """

    if nodes is None:
        return []

    if isinstance(nodes, Node):
        return [nodes]

    if isinstance(nodes, (list, tuple, set)):
        return list(nodes)

    return [nodes]


def _normalize_edges(edges):
    """
    Convert different possible edge input formats into a list of Edge objects.
    """

    if edges is None:
        return []

    if isinstance(edges, Edge):
        return [edges]

    if isinstance(edges, (list, tuple, set)):
        return list(edges)

    return [edges]


def build_graph(nodes, edges=None, *additional_args):
    """
    Build a NetworkX graph from Node and Edge objects.

    Nodes are stored using their UUID string as the NetworkX node ID.
    """

    graph = nx.Graph()

    # ---------------------------------------------------------
    # Normalize nodes
    # ---------------------------------------------------------

    node_list = _normalize_nodes(nodes)

    # Support:
    # build_graph(node1, node2, node3, [edge1, edge2])
    #
    # If additional positional arguments contain Nodes,
    # treat them as additional nodes.
    for item in additional_args:
        if isinstance(item, Node):
            node_list.append(item)

    # ---------------------------------------------------------
    # Normalize edges
    # ---------------------------------------------------------

    edge_list = _normalize_edges(edges)

    # If additional arguments contain edges or lists of edges,
    # add them to the edge list.
    for item in additional_args:
        if isinstance(item, Edge):
            edge_list.append(item)

        elif isinstance(item, (list, tuple, set)):
            edge_list.extend(_normalize_edges(item))

    # ---------------------------------------------------------
    # Add nodes
    # ---------------------------------------------------------

    for node in node_list:

        if node is None:
            continue

        # Make absolutely sure the node has an ID.
        if node.id is None:
            continue

        node_id = str(node.id)

        graph.add_node(
            node_id,
            node_type=node.node_type,
            label=node.label,
            value=node.value,
        )

    # ---------------------------------------------------------
    # Add edges
    # ---------------------------------------------------------

    for edge in edge_list:

        if edge is None:
            continue

        if edge.source_node_id is None:
            continue

        if edge.target_node_id is None:
            continue

        source_id = str(edge.source_node_id)
        target_id = str(edge.target_node_id)

        # Add missing nodes if necessary.
        if source_id not in graph:
            graph.add_node(source_id)

        if target_id not in graph:
            graph.add_node(target_id)

        graph.add_edge(
            source_id,
            target_id,
            relationship=edge.relationship,
        )

    return graph


def get_connected_nodes(graph, node_id):
    """
    Return IDs of all nodes directly connected to the given node.

    Example:

        node1 -- node2
        node1 -- node3

    get_connected_nodes(graph, node1.id)

    returns:

        [str(node2.id), str(node3.id)]
    """

    if graph is None:
        return []

    if node_id is None:
        return []

    node_id = str(node_id)

    if node_id not in graph:
        return []

    return [str(neighbor) for neighbor in graph.neighbors(node_id)]


def get_relationships(graph, node_id):
    """
    Return all relationships connected to the given node.

    Each relationship is returned as a dictionary:

        {
            "source": "...",
            "target": "...",
            "relationship": "..."
        }
    """

    if graph is None:
        return []

    if node_id is None:
        return []

    node_id = str(node_id)

    if node_id not in graph:
        return []

    relationships = []

    for source, target, attributes in graph.edges(
        node_id,
        data=True,
    ):
        relationships.append(
            {
                "source": str(source),
                "target": str(target),
                "relationship": attributes.get(
                    "relationship",
                    "unknown",
                ),
            }
        )

    return relationships