from datetime import datetime, timedelta, timezone
from unittest import result

from app.models import Person, Source, Observation, Snapshot
from app.api.snapshot_diff import compare_snapshots


def test_snapshot_diff_detects_added_removed_and_modified(
    session,
):
    person = Person(display_name="Snapshot Diff Test")
    session.add(person)
    session.flush()

    source = Source(
        platform="github",
        url="https://github.com/example",
    )
    session.add(source)
    session.flush()

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    before = Snapshot(
        person_id=person.id,
        captured_at=now,
    )
    after = Snapshot(
        person_id=person.id,
        captured_at=now + timedelta(minutes=1),
    )

    old_username = Observation(
        source_id=source.id,
        category="profile",
        key="username",
        value="old_user",
        observed_at=now,
    )
    removed_bio = Observation(
        source_id=source.id,
        category="profile",
        key="bio",
        value="Old bio",
        observed_at=now,
    )
    new_repo = Observation(
        source_id=source.id,
        category="repository",
        key="repo",
        value="project-one",
        observed_at=now + timedelta(minutes=1),
    )
    new_username = Observation(
        source_id=source.id,
        category="profile",
        key="username",
        value="new_user",
        observed_at=now + timedelta(minutes=1),
    )

    before.observations = [old_username, removed_bio]
    after.observations = [new_username, new_repo]

    session.add_all([before, after])
    session.commit()

    result = compare_snapshots(
        snapshot_before_id=before.id,
        snapshot_after_id=after.id,
    )

    assert "error" not in result
    assert result["total_changes"] == 3

    change_types = {
        (change["change_type"], change["key"])
        for change in result["changes"]
    }

    assert ("added", "repo") in change_types
    assert ("removed", "bio") in change_types
    assert ("modified", "username") in change_types
    assert result["summary"]["added"] == 1
    assert result["summary"]["removed"] == 1
    assert result["summary"]["modified"] == 1