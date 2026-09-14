from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database import engine
from app.models import (
    Person,
    Source,
    Observation,
    Snapshot,
    Change,
    ChangeType,
    snapshot_observations,
)


def test_person_model():
    person = Person(
        display_name="Test User",
        created_at=datetime.now(timezone.utc),
    )

    with Session(engine) as session:
        session.add(person)
        session.flush()

        assert person.display_name == "Test User"
        assert person.id is not None


def test_source_model():
    source = Source(
        platform="GitHub",
        url="https://github.com/example",
    )

    assert source.platform == "GitHub"
    assert source.url == "https://github.com/example"


def test_observation_model():
    source = Source(
        platform="GitHub",
        url="https://github.com/example",
    )

    observation = Observation(
        source_id=source.id,
        category="profile",
        key="username",
        value="exampleuser",
        observed_at=datetime.now(timezone.utc),
    )

    assert observation.key == "username"
    assert observation.value == "exampleuser"


def test_snapshot_model():
    person = Person(
        display_name="Test User",
        created_at=datetime.now(timezone.utc),
    )

    snapshot = Snapshot(
        person_id=person.id,
        captured_at=datetime.now(timezone.utc),
    )

    assert snapshot.person_id == person.id
    assert snapshot.captured_at is not None
    assert snapshot_observations.name == "snapshot_observations"


def test_change_model():
    person = Person(
        display_name="Test User",
        created_at=datetime.now(timezone.utc),
    )

    snapshot_before = Snapshot(
        person_id=person.id,
        captured_at=datetime.now(timezone.utc),
    )

    snapshot_after = Snapshot(
        person_id=person.id,
        captured_at=datetime.now(timezone.utc),
    )

    change = Change(
        snapshot_before_id=snapshot_before.id,
        snapshot_after_id=snapshot_after.id,
        change_type=ChangeType.MODIFIED,
        old_value="exampleuser",
        new_value="example_user",
        detected_at=datetime.now(timezone.utc),
    )

    assert change.change_type == ChangeType.MODIFIED
    assert change.old_value == "exampleuser"
    assert change.new_value == "example_user"
    assert change.detected_at is not None