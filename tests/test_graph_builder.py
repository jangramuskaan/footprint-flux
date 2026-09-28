from app.models.graph import Relationship
from app.services.graph_builder import build_relationship


def test_username_relationship():
    edge = build_relationship(
        "username",
        "github:jangramuskaan",
        "jangramuskaan",
    )

    assert edge is not None
    assert edge.relationship == Relationship.SAME_USERNAME.value


def test_url_relationship():
    edge = build_relationship(
        "url",
        "github:jangramuskaan",
        "https://example.com",
    )

    assert edge is not None
    assert edge.relationship == Relationship.SAME_URL.value


def test_email_relationship():
    edge = build_relationship(
        "email",
        "github:jangramuskaan",
        "example@example.com",
    )

    assert edge is not None
    assert edge.relationship == Relationship.SAME_EMAIL.value


def test_unknown_observation_returns_none():
    edge = build_relationship(
        "unknown",
        "source",
        "target",
    )

    assert edge is None