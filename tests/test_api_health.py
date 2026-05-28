from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_data_status():
    response = client.get("/api/data-status")
    assert response.status_code == 200
    assert response.json()["activeMode"] in {"sample", "blob", "cosmos"}
