from __future__ import annotations

import json
import os
from pathlib import Path

from azure.cosmos import CosmosClient
from app.scoring import compute_accessibility_score, compute_delay_penalty, haversine_km


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SAMPLE_DIR = BASE_DIR / "app" / "static" / "sample-data"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def get_database():
    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ["COSMOS_KEY"]
    database_name = os.getenv("COSMOS_DATABASE", os.getenv("COSMOS_DATABASE_NAME", "mobilitydb"))
    client = CosmosClient(endpoint, credential=key)
    return client.create_database_if_not_exists(id=database_name)


def upsert_documents(container_name: str, partition_key: str, documents: list[dict]) -> None:
    db = get_database()
    container = db.create_container_if_not_exists(id=container_name, partition_key={"paths": [partition_key], "kind": "Hash"})
    for document in documents:
        container.upsert_item(document)
        print(f"upserted {container_name}/{document['id']}")


def build_route_docs() -> list[dict]:
    docs = []
    sample_file_map = {
        "metro": SAMPLE_DIR / "riyadh_metro_lines_sample.geojson",
        "bus": SAMPLE_DIR / "riyadh_bus_routes_sample.geojson",
    }
    for mode, file_name in (("metro", "metro_lines.geojson"), ("bus", "bus_routes.geojson")):
        processed_path = PROCESSED_DIR / file_name
        payload = load_json(processed_path if processed_path.exists() else sample_file_map[mode])
        source = "rcrc" if processed_path.exists() else "sample"
        for feature in payload.get("features", []):
            props = feature.get("properties", {})
            docs.append(
                {
                    "id": props.get("routeId", props.get("id")),
                    "type": mode,
                    "source": source,
                    "name": props.get("name"),
                    "mode": mode,
                    "lineColor": props.get("lineColor", "#888888"),
                    "featureCount": 1,
                    "geometryBlobPath": f"processed-data/{file_name}",
                    "lastUpdatedUtc": "2026-05-24T00:00:00Z",
                }
            )
    return docs


def iter_feature_points(feature: dict):
    geometry = feature.get("geometry", {})
    coordinates = geometry.get("coordinates", [])
    geometry_type = geometry.get("type")
    if geometry_type == "Point":
        yield tuple(coordinates)
    elif geometry_type == "LineString":
        for point in coordinates:
            yield tuple(point)
    elif geometry_type == "MultiLineString":
        for line in coordinates:
            for point in line:
                yield tuple(point)


def count_nearby_features(geojson: dict, lat: float, lon: float, buffer_km: float) -> int:
    count = 0
    for feature in geojson.get("features", []):
        for point_lon, point_lat in iter_feature_points(feature):
            if haversine_km(lat, lon, point_lat, point_lon) <= buffer_km:
                count += 1
                break
    return count


def build_district_docs() -> list[dict]:
    metro = load_json(SAMPLE_DIR / "riyadh_metro_lines_sample.geojson")
    bus = load_json(SAMPLE_DIR / "riyadh_bus_routes_sample.geojson")
    events = load_json(SAMPLE_DIR / "mock_live_events_sample.json")
    payload = load_json(SAMPLE_DIR / "district_centers_sample.geojson")
    docs = []
    for feature in payload.get("features", []):
        props = feature["properties"]
        lon, lat = feature["geometry"]["coordinates"]
        metro_count = count_nearby_features(metro, lat, lon, 1.5)
        bus_count = count_nearby_features(bus, lat, lon, 1.5)
        live_delay_penalty = compute_delay_penalty(lat, lon, events, 1.5)
        score = compute_accessibility_score(metro_count, bus_count, live_delay_penalty)
        docs.append(
            {
                "id": f"district-{props['districtId']}",
                "districtId": props["districtId"],
                "name": props["name"],
                "center": {"lat": lat, "lon": lon},
                "nearbyMetroCount": metro_count,
                "nearbyBusCount": bus_count,
                "accessibilityScore": score["score"],
                "accessibilityRating": score["rating"],
                "lastCalculatedUtc": "2026-05-24T00:00:00Z",
            }
        )
    return docs


def build_event_docs() -> list[dict]:
    return load_json(SAMPLE_DIR / "mock_live_events_sample.json")


if __name__ == "__main__":
    upsert_documents("routes", "/type", build_route_docs())
    upsert_documents("districts", "/districtId", build_district_docs())
    upsert_documents("events", "/routeId", build_event_docs())
