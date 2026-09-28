from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.graph.node import Node


def save_node(
    session: Session,
    node: Node,
) -> Node:
    session.add(node)
    session.commit()
    session.refresh(node)

    return node


def get_node(
    session: Session,
    node_id: UUID,
) -> Node | None:
    statement = select(Node).where(Node.id == node_id)

    return session.execute(statement).scalar_one_or_none()


def get_nodes(
    session: Session,
) -> list[Node]:
    statement = select(Node)

    return list(session.execute(statement).scalars().all())