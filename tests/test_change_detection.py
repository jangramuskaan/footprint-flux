from datetime import datetime, timezone

from app.models import (
    ChangeType,
    Observation,
    Person,
    Snapshot,
    Source,
)
from app.services.change_detection import detect_changes


def make_observation(
    session,
    source,
    category,
    key,
    value,
):
    observation = Observation(
        source_id=source.id,
        category=category,
        key=key,
        value=value,
        observed_at=datetime.now(timezone.utc),
    )

    session.add(observation)
    session.flush()

    return observation


def make_snapshot(
    session,
    person,
    observations,
):
    snapshot = Snapshot(
        person_id=person.id,
        captured_at=datetime.now(timezone.utc),
    )

    snapshot.observations = observations

    session.add(snapshot)
    session.flush()

    return snapshot


def setup_person_and_source(session):
    person = Person(
        display_name="Test Person",
        created_at=datetime.now(timezone.utc),
    )

    source = Source(
        platform="GitHub",
        url="https://github.com/test-user",
    )

    session.add_all([person, source])
    session.flush()

    return person, source


def test_detect_added_change(session):
    person, source = setup_person_and_source(session)

    before = make_snapshot(
        session,
        person,
        [],
    )

    observation = make_observation(
        session,
        source,
        "profile",
        "followers",
        "8",
    )

    after = make_snapshot(
        session,
        person,
        [observation],
    )

    changes = detect_changes(
        session=session,
        snapshot_before=before,
        snapshot_after=after,
    )

    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.ADDED
    assert changes[0].old_value is None
    assert changes[0].new_value == "8"


def test_detect_removed_change(session):
    person, source = setup_person_and_source(session)

    observation = make_observation(
        session,
        source,
        "profile",
        "bio",
        "Developer",
    )

    before = make_snapshot(
        session,
        person,
        [observation],
    )

    after = make_snapshot(
        session,
        person,
        [],
    )

    changes = detect_changes(
        session=session,
        snapshot_before=before,
        snapshot_after=after,
    )

    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.REMOVED
    assert changes[0].old_value == "Developer"
    assert changes[0].new_value is None


def test_detect_modified_change(session):
    person, source = setup_person_and_source(session)

    before_observation = make_observation(
        session,
        source,
        "profile",
        "followers",
        "7",
    )

    after_observation = make_observation(
        session,
        source,
        "profile",
        "followers",
        "8",
    )

    before = make_snapshot(
        session,
        person,
        [before_observation],
    )

    after = make_snapshot(
        session,
        person,
        [after_observation],
    )

    changes = detect_changes(
        session=session,
        snapshot_before=before,
        snapshot_after=after,
    )

    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.MODIFIED
    assert changes[0].old_value == "7"
    assert changes[0].new_value == "8"
