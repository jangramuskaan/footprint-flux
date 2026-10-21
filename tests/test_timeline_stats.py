from datetime import datetime, timedelta, timezone
from uuid import uuid4
from app.models import Person, Snapshot
from app.services.timeline_stats import get_timeline_stats


def test_timeline_stats_change_rate_with_multiple_snapshots(session):
    person = Person(
        display_name="Change Rate Test",
        created_at=datetime.now(timezone.utc),
    )
    session.add(person)
    session.flush()

    first_time = datetime(2026, 9, 20)
    snapshots = [
        Snapshot(person_id=person.id, captured_at=first_time),
        Snapshot(
            person_id=person.id,
            captured_at=first_time + timedelta(days=1),
        ),
        Snapshot(
            person_id=person.id,
            captured_at=first_time + timedelta(days=2),
        ),
    ]

    session.add_all(snapshots)
    session.flush()

    stats = get_timeline_stats(session, person.id)

    assert stats["total_snapshots"] == 3
    assert stats["total_changes"] == 0
    assert stats["change_rate"] == 0
    assert stats["activity_status"] == "no_changes"
    assert stats["first_snapshot"] == snapshots[0].captured_at
    assert stats["latest_snapshot"] == snapshots[2].captured_at