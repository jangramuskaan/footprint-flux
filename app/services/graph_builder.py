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
        node_type="profile",
        label="Source Profile",
        value=source_value,
    )

    target = Node(
        node_type=observation_type,
        label=observation_type.capitalize(),
        value=target_value,
    )

    return Edge(
        source_node_id=source.id,
        target_node_id=target.id,
        relationship=relationship.value,
    )