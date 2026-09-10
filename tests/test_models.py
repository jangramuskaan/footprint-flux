from datetime import datetime, timezone

from app.models import (
    Person,
    Source,
    Observation,
    Snapshot,
    Change,
    ChangeType,
)


def test_person_model():
    person = Person(
        display_name="Test User",
        created_at="2026-09-09T13:00:00"
    )

    assert person.display_name == "Test User"
    assert person.id is not None


def test_source_model():
    source = Source(
        platform="GitHub",
        url="https://github.com/example"
    )

    assert source.platform == "GitHub"


def test_observation_model():
    source = Source(
        platform="GitHub",
        url="https://github.com/example"
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
        created_at="2026-09-09T13:00:00"
    )

    snapshot = Snapshot(
        person_id=person.id,
        captured_at=datetime.now(timezone.utc),
    )

    assert snapshot.person_id == person.id
    assert snapshot.observation_ids == []


def test_change_model():
    person = Person(
        display_name="Test User",
        created_at="2026-09-09T13:00:00"
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