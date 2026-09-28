from app.models.graph import Node, Relationship
from app.services.graph_service import create_node, create_relationship


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

    source = create_node(
        node_type="profile",
        label="Source Profile",
        value=source_value,
    )

    target = create_node(
        node_type=observation_type,
        label=observation_type.capitalize(),
        value=target_value,
    )

    return create_relationship(
        source,
        target,
        relationship,
    )