from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database import engine
from app.models import Change, ChangeType, Person, Snapshot
from app.services.change_service import (
    save_change,
    get_change,
    get_changes_between_snapshots,
)


def test_change_service():
    person = Person(
        display_name="Change Service User",
        created_at=datetime.now(timezone.utc),
    )

    with Session(engine) as session:
        session.add(person)
        session.flush()

        snapshot_before = Snapshot(
            person_id=person.id,
            captured_at=datetime.now(timezone.utc),
        )

        snapshot_after = Snapshot(
            person_id=person.id,
            captured_at=datetime.now(timezone.utc),
        )

        session.add_all([
            snapshot_before,
            snapshot_after,
        ])
        session.flush()

        change = Change(
            snapshot_before_id=snapshot_before.id,
            snapshot_after_id=snapshot_after.id,
            change_type=ChangeType.MODIFIED,
            old_value="old_username",
            new_value="new_username",
            detected_at=datetime.now(timezone.utc),
        )

        saved = save_change(
            session=session,
            change=change,
        )

        assert saved.id is not None
        assert saved.change_type == ChangeType.MODIFIED
        assert saved.old_value == "old_username"
        assert saved.new_value == "new_username"

        retrieved = get_change(
            session=session,
            change_id=saved.id,
        )

        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.snapshot_before_id == snapshot_before.id
        assert retrieved.snapshot_after_id == snapshot_after.id

        changes = get_changes_between_snapshots(
            session=session,
            snapshot_before_id=snapshot_before.id,
            snapshot_after_id=snapshot_after.id,
        )

        assert len(changes) == 1
        assert changes[0].id == saved.id
        assert changes[0].new_value == "new_username"