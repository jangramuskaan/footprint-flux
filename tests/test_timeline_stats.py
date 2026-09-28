from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database import engine
from app.models import Person, Snapshot
from app.services.timeline_stats import get_timeline_stats


def test_get_timeline_stats():
    person = Person(
        display_name="Stats Test User",
        created_at=datetime.now(timezone.utc),
    )

    with Session(engine) as session:
        session.add(person)
        session.flush()

        snapshot_1 = Snapshot(
            person_id=person.id,
            captured_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        )

        snapshot_2 = Snapshot(
            person_id=person.id,
            captured_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
        )

        session.add_all([snapshot_1, snapshot_2])
        session.commit()

        stats = get_timeline_stats(
            session=session,
            person_id=person.id,
        )

        assert stats["total_snapshots"] == 2
        assert stats["total_changes"] == 0
        assert stats["first_snapshot"] == snapshot_1.captured_at
        assert stats["latest_snapshot"] == snapshot_2.captured_at