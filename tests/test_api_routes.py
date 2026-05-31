from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_routes_returns_envelope():
    response = client.get("/api/routes")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "source" in data
    assert isinstance(data["items"], list)


def test_metro_geojson_shape():
    response = client.get("/api/routes/geojson?mode=metro")
    assert response.status_code == 200
    data = response.json()
    assert "geojson" in data
    geojson = data["geojson"]
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) > 0


def test_bus_geojson_shape():
    response = client.get("/api/routes/geojson?mode=bus")
    assert response.status_code == 200
    data = response.json()
    assert "geojson" in data
    geojson = data["geojson"]
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) > 0


def test_districts_returns_envelope():
    response = client.get("/api/districts")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "source" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


def test_district_has_required_fields():
    response = client.get("/api/districts")
    assert response.status_code == 200
    for district in response.json()["items"]:
        assert "name" in district
        assert "center" in district
        assert "lat" in district["center"]
        assert "lon" in district["center"]


def test_score_endpoint_returns_score():
    districts = client.get("/api/districts").json()["items"]
    district_id = districts[0]["districtId"]
    response = client.get(f"/api/score?districtId={district_id}")
    assert response.status_code == 200
    data = response.json()
    assert "item" in data
    item = data["item"]
    assert "accessibilityScore" in item
    assert "accessibilityRating" in item
    assert item["accessibilityRating"] in {"Low", "Medium", "High"}
    assert isinstance(item["accessibilityScore"], (int, float))


def test_score_rating_bands():
    districts = client.get("/api/districts").json()["items"]
    for district in districts[:3]:
        response = client.get(f"/api/score?districtId={district['districtId']}")
        assert response.status_code == 200
        item = response.json()["item"]
        assert item["accessibilityRating"] in {"Low", "Medium", "High"}


def test_live_events_returns_envelope():
    response = client.get("/api/live-events")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
