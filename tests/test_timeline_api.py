from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy.orm import Session

from app.api import timeline
from app.database import engine
from app.models import Person, Snapshot
from app.api.timeline import timeline_for_person
from uuid import UUID, uuid4



client = TestClient(app)

def test_timeline_stats_endpoint_returns_success():
    from uuid import uuid4

    person_id = uuid4()
    response = client.get(f"/timeline/{person_id}/stats")

    assert response.status_code == 200

    data = response.json()
    assert data["total_snapshots"] == 0
    assert data["total_changes"] == 0
    assert "change_rate" in data
    assert "activity_status" in data



def test_timeline_stats_rejects_invalid_uuid():
    response = client.get("/timeline/not-a-valid-uuid/stats")

    assert response.status_code == 422



def test_timeline_for_person():
    person = Person(
        display_name="API Timeline Test User",
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

        timeline = timeline_for_person(
            session=session,
            person_id=person.id,
        )

        assert len(timeline) == 2
        assert timeline[0]["type"] == "snapshot"
        assert timeline[1]["type"] == "snapshot" 
        assert timeline[0]["snapshot_id"] == str(snapshot_1.id)
        assert timeline[1]["snapshot_id"] == str(snapshot_2.id)


def test_timeline_rejects_zero_limit():
    response = client.get(
        f"/timeline/{uuid4()}",
        params={"limit": 0},
    )
    assert response.status_code == 422


def test_timeline_rejects_negative_offset():
    response = client.get(
        f"/timeline/{uuid4()}",
        params={"offset": -1},
    )
    assert response.status_code == 422


def test_timeline_rejects_excessive_limit():
    response = client.get(
        f"/timeline/{uuid4()}",
        params={"limit": 501},
    )
    assert response.status_code == 422



def test_timeline_pagination_returns_limited_events():
    person = Person(
        display_name="Pagination Test User",
        created_at=datetime.now(timezone.utc),
    )

    with Session(engine) as session:
        session.add(person)
        session.flush()

        snapshots = [
            Snapshot(
                person_id=person.id,
                captured_at=datetime(2026, 9, day, tzinfo=timezone.utc),
            )
            for day in (20, 21, 22)
        ]
        session.add_all(snapshots)
        session.commit()

        person_id = person.id

    response = client.get(
        f"/timeline/{person_id}",
        params={"limit": 2, "offset": 0},
    )

    assert response.status_code == 200
    events = response.json()
    assert len(events) == 2
    assert all(event["type"] == "snapshot" for event in events)
