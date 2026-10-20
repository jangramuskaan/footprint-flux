
from uuid import uuid4
from datetime import datetime, timezone

from app.models import Person, Snapshot
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)



def test_snapshot_diff_rejects_reverse_chronological_order(session):
    person = Person(
        display_name="Snapshot Order Test",
        created_at=datetime.now(timezone.utc),
    )
    session.add(person)
    session.flush()

    later_snapshot = Snapshot(
        person_id=person.id,
        captured_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
    )
    earlier_snapshot = Snapshot(
        person_id=person.id,
        captured_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
    )

    session.add_all([later_snapshot, earlier_snapshot])
    session.commit()

    response = client.get(
        "/snapshots/diff",
        params={
            "snapshot_before_id": str(later_snapshot.id),
            "snapshot_after_id": str(earlier_snapshot.id),
        },
    )

    assert response.status_code == 400


def test_snapshot_diff_rejects_snapshots_from_different_people(session):
    person_a = Person(
        display_name="Snapshot Diff Person A",
        created_at=datetime.now(timezone.utc),
    )
    person_b = Person(
        display_name="Snapshot Diff Person B",
        created_at=datetime.now(timezone.utc),
    )

    session.add_all([person_a, person_b])
    session.flush()

    before = Snapshot(
        person_id=person_a.id,
        captured_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
    )
    after = Snapshot(
        person_id=person_b.id,
        captured_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
    )

    session.add_all([before, after])
    session.commit()

    response = client.get(
        "/snapshots/diff",
        params={
            "snapshot_before_id": str(before.id),
            "snapshot_after_id": str(after.id),
        },
    )

    assert response.status_code == 400


def test_snapshot_diff_requires_snapshot_ids():
    response = client.get("/snapshots/diff")

    assert response.status_code == 422


def test_snapshot_diff_rejects_invalid_uuid():
    response = client.get(
        "/snapshots/diff",
        params={
            "snapshot_before_id": "invalid-uuid",
            "snapshot_after_id": "invalid-uuid",
        },
    )

    assert response.status_code == 422


def test_snapshot_diff_returns_not_found_for_missing_snapshots():
    response = client.get(
        "/snapshots/diff",
        params={
            "snapshot_before_id": str(uuid4()),
            "snapshot_after_id": str(uuid4()),
        },
    )

    assert response.status_code == 404