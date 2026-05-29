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


def test_config_is_safe_for_frontend():
    response = client.get("/api/config")
    assert response.status_code == 200
    payload = response.json()
    assert "azureMapsKey" not in payload
    assert payload["dataMode"] in {"sample", "blob", "cosmos", "auto"}


def test_frontend_assets_disable_caching():
    root = client.get("/")
    script = client.get("/src/main.js")

    assert root.status_code == 200
    assert script.status_code == 200
    assert root.headers["cache-control"] == "no-store, max-age=0"
    assert script.headers["cache-control"] == "no-store, max-age=0"
