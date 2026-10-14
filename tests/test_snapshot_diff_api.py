from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_snapshot_diff_requires_snapshot_ids():
    response = client.get("/snapshots/diff")

    assert response.status_code == 422


def test_snapshot_diff_rejects_invalid_uuid():
    response = client.get(
        "/snapshots/diff",
        params={
            "snapshot_before_id": "invalid",
            "snapshot_after_id": str(uuid4()),
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

 
def test_snapshot_diff_missing_ids_returns_422():
    response = client.get("/snapshots/diff")

    assert response.status_code == 422
