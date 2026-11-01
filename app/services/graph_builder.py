from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.graph import Node, Relationship
from app.models.graph.edge import Edge


def build_relationship(
    observation_type: str,
    source_value: str,
    target_value: str,
):
    relationship_map = {
        "username": Relationship.SAME_USERNAME,
        "url": Relationship.SAME_URL,
        "email": Relationship.SAME_EMAIL,
    }

    relationship = relationship_map.get(observation_type)

    if relationship is None:
        return None

    source = Node(
        id=uuid4(),
        node_type="profile",
        label="Source Profile",
        value=source_value,
    )

    target = Node(
        id=uuid4(),
        node_type=observation_type,
        label=observation_type.capitalize(),
        value=target_value,
    )

    return Edge(
        id=uuid4(),
        source_node_id=source.id,
        target_node_id=target.id,
        relationship=relationship.value,
    )



def save_relationship(
    session: Session,
    observation_type: str,
    source_value: str,
    target_value: str,
):
    relationship_map = {
        "username": Relationship.SAME_USERNAME,
        "url": Relationship.SAME_URL,
        "email": Relationship.SAME_EMAIL,
    }

    relationship = relationship_map.get(observation_type)

    if relationship is None:
        return None

    source_statement = select(Node).where(
        Node.node_type == "profile",
        Node.value == source_value,
    )
    source = session.execute(source_statement).scalar_one_or_none()

    if source is None:
        source = Node(
            node_type="profile",
            label="Source Profile",
            value=source_value,
        )
        session.add(source)
        session.flush()

    target_statement = select(Node).where(
        Node.node_type == observation_type,
        Node.value == target_value,
    )
    target = session.execute(target_statement).scalar_one_or_none()

    if target is None:
        target = Node(
            node_type=observation_type,
            label=observation_type.capitalize(),
            value=target_value,
        )
        session.add(target)
        session.flush()

    edge = Edge(
        source_node_id=source.id,
        target_node_id=target.id,
        relationship=relationship.value,
    )

    session.add(edge)
    session.commit()
    session.refresh(edge)

    return edge