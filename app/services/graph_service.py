from app.models.graph import Node, Edge, Relationship


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