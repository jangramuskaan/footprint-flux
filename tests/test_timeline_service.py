from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.api import timeline
from app.database import engine
from app.models import Person, Snapshot


def test_get_person_timeline():
    from app.services.timeline_service import get_person_timeline

    person = Person(
        display_name="Timeline Test User",
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

        timeline = get_person_timeline(
            session=session,
            person_id=person.id,
        )

        assert len(timeline) == 2
        assert timeline[0]["type"] == "snapshot"
        assert timeline[1]["type"] == "snapshot"    
        assert timeline[0]["snapshot_id"] == str(snapshot_1.id)
        assert timeline[1]["snapshot_id"] == str(snapshot_2.id)