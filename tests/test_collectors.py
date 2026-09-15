from uuid import UUID

from app.collectors.manual import create_observation


def test_create_observation():
    source_id = UUID("12345678-1234-5678-1234-567812345678")

    observation = create_observation(
        source_id=source_id,
        category="profile",
        key="username",
        value="example_user",
    )

    assert observation.category == "profile"
    assert observation.key == "username"
    assert observation.value == "example_user"