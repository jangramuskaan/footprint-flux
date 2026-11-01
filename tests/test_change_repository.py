from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Change, ChangeType, Person, Snapshot
from app.repositories.change import save_change, get_change


def test_save_and_get_change():
    person = Person(
        display_name="Test User",
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
            old_value="exampleuser",
            new_value="example_user",
            detected_at=datetime.now(timezone.utc),
        )

        saved = save_change(
            session=session,
            change=change,
        )

        assert saved.id is not None
        assert saved.change_type == ChangeType.MODIFIED
        assert saved.old_value == "exampleuser"
        assert saved.new_value == "example_user"

        retrieved = get_change(
            session=session,
            change_id=saved.id,
        )

        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.snapshot_before_id == snapshot_before.id
        assert retrieved.snapshot_after_id == snapshot_after.id



def test_save_change_prevents_duplicates():
    person = Person(
        display_name="Duplicate Test User",
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

        session.add_all([snapshot_before, snapshot_after])
        session.flush()

        change_one = Change(
            snapshot_before_id=snapshot_before.id,
            snapshot_after_id=snapshot_after.id,
            change_type=ChangeType.MODIFIED,
            old_value="old_username",
            new_value="new_username",
            detected_at=datetime.now(timezone.utc),
        )

        first_saved = save_change(session, change_one)

        change_two = Change(
            snapshot_before_id=snapshot_before.id,
            snapshot_after_id=snapshot_after.id,
            change_type=ChangeType.MODIFIED,
            old_value="old_username",
            new_value="new_username",
            detected_at=datetime.now(timezone.utc),
        )

        second_saved = save_change(session, change_two)

        assert first_saved.id == second_saved.id

        duplicates = session.execute(
            select(Change).where(
                Change.snapshot_before_id == snapshot_before.id,
                Change.snapshot_after_id == snapshot_after.id,
            )
        ).scalars().all()

        assert len(duplicates) == 1