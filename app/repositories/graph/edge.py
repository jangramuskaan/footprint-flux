from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.graph.edge import Edge


def save_edge(
    session: Session,
    edge: Edge,
) -> Edge:
    session.add(edge)
    session.commit()
    session.refresh(edge)

    return edge


def get_edge(
    session: Session,
    edge_id: UUID,
) -> Edge | None:
    statement = select(Edge).where(Edge.id == edge_id)

    return session.execute(statement).scalar_one_or_none()


def get_edges(
    session: Session,
) -> list[Edge]:
    statement = select(Edge)

    return list(session.execute(statement).scalars().all())