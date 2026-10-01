from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_exposure_endpoint():
    response = client.get("/api/exposure")

    assert response.status_code == 200

    data = response.json()

    assert "score" in data
    assert isinstance(data["score"], int)
    assert 0 <= data["score"] <= 100