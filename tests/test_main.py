from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "Footprint Flux"


def test_graph_endpoint():
    response = client.get("/graph")

    assert response.status_code == 200

    data = response.json()

    assert "nodes" in data
    assert "links" in data
