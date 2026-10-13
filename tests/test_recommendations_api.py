from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_recommendations_endpoint_returns_success():
    person_id = uuid4()

    response = client.get(
        f"/recommendations/{person_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["person_id"] == str(person_id)
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)


def test_recommendations_endpoint_rejects_invalid_uuid():
    response = client.get(
        "/recommendations/not-a-valid-uuid"
    )

    assert response.status_code == 422
