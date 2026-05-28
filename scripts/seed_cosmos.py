from __future__ import annotations

import json
import os
from pathlib import Path

from azure.cosmos import CosmosClient


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SAMPLE_DIR = BASE_DIR / "app" / "static" / "sample-data"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def get_database():
    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ["COSMOS_KEY"]
    database_name = os.getenv("COSMOS_DATABASE_NAME", "mobilitydb")
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
    for mode, file_name in (("metro", "metro_lines.geojson"), ("bus", "bus_routes.geojson")):
        payload = load_json(PROCESSED_DIR / file_name if (PROCESSED_DIR / file_name).exists() else SAMPLE_DIR / f"riyadh_{mode}_lines_sample.geojson")
        for feature in payload.get("features", []):
            props = feature.get("properties", {})
            docs.append(
                {
                    "id": props.get("routeId", props.get("id")),
                    "type": mode,
                    "source": "rcrc",
                    "name": props.get("name"),
                    "mode": mode,
                    "lineColor": props.get("lineColor", "#888888"),
                    "featureCount": 1,
                    "geometryBlobPath": f"processed-data/{file_name}",
                    "lastUpdatedUtc": "2026-05-24T00:00:00Z",
                }
            )
    return docs


def build_district_docs() -> list[dict]:
    payload = load_json(SAMPLE_DIR / "district_centers_sample.geojson")
    docs = []
    for feature in payload.get("features", []):
        props = feature["properties"]
        lon, lat = feature["geometry"]["coordinates"]
        docs.append(
            {
                "id": props["districtId"],
                "districtId": props["districtId"],
                "name": props["name"],
                "center": {"lat": lat, "lon": lon},
                "nearbyMetroCount": 0,
                "nearbyBusCount": 0,
                "accessibilityScore": 0,
                "accessibilityRating": "Low",
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
