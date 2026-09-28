from app.models.graph import Relationship
from app.services.graph_service import create_node, create_relationship


def test_create_node():
    node = create_node(
        node_type="github",
        label="GitHub Profile",
        value="jangramuskaan",
    )

    assert node.node_type == "github"
    assert node.label == "GitHub Profile"
    assert node.value == "jangramuskaan"


def test_create_relationship():
    source = create_node(
        node_type="github",
        label="GitHub Profile",
        value="jangramuskaan",
    )

    target = create_node(
        node_type="username",
        label="Username",
        value="jangramuskaan",
    )

    edge = create_relationship(
        source,
        target,
        Relationship.SAME_USERNAME,
    )

    assert edge.source_node_id == source.id
    assert edge.target_node_id == target.id
    assert edge.relationship == Relationship.SAME_USERNAME.value