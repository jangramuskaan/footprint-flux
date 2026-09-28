from uuid import UUID

from sqlalchemy.orm import Session

from app.models.graph.edge import Edge
from app.models.graph.node import Node
from app.models.graph.relationship import Relationship
from app.repositories.graph.edge import save_edge
from app.repositories.graph.node import save_node


def create_node(
    session: Session,
    node_type: str,
    label: str,
    value: str,
) -> Node:
    node = Node(
        node_type=node_type,
        label=label,
        value=value,
    )

    return save_node(session, node)


def create_relationship(
    session: Session,
    source_node_id: UUID,
    target_node_id: UUID,
    relationship: Relationship,
) -> Edge:
    edge = Edge(
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        relationship=relationship.value,
    )

    return save_edge(session, edge)