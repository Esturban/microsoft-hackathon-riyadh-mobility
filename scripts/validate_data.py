from __future__ import annotations

import json
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "app" / "static" / "sample-data"


def validate_geojson(file_name: str) -> None:
    payload = json.loads((SAMPLE_DIR / file_name).read_text(encoding="utf-8"))
    if payload.get("type") != "FeatureCollection":
        raise ValueError(f"{file_name} is not a FeatureCollection")
    if not payload.get("features"):
        raise ValueError(f"{file_name} has no features")
    for feature in payload["features"]:
        if "geometry" not in feature or "properties" not in feature:
            raise ValueError(f"{file_name} has a feature missing geometry/properties")
    print(f"ok {file_name}: {len(payload.get('features', []))} features")


def validate_district_properties() -> None:
    payload = json.loads(
        (SAMPLE_DIR / "district_centers_sample.geojson").read_text(encoding="utf-8")
    )
    for feature in payload["features"]:
        props = feature["properties"]
        if "districtId" not in props or "name" not in props:
            raise ValueError("district sample file is missing districtId or name")
    print("ok district properties")


def validate_route_properties(file_name: str) -> None:
    payload = json.loads((SAMPLE_DIR / file_name).read_text(encoding="utf-8"))
    for feature in payload["features"]:
        props = feature["properties"]
        if "routeId" not in props and "id" not in props:
            raise ValueError(f"{file_name} is missing route id properties")
        if "name" not in props:
            raise ValueError(f"{file_name} is missing route name")
    print(f"ok route properties for {file_name}")


if __name__ == "__main__":
    try:
        validate_geojson("riyadh_metro_lines_sample.geojson")
        validate_geojson("riyadh_bus_routes_sample.geojson")
        validate_geojson("district_centers_sample.geojson")
        validate_route_properties("riyadh_metro_lines_sample.geojson")
        validate_route_properties("riyadh_bus_routes_sample.geojson")
        validate_district_properties()
    except Exception as exc:
        print(f"validation failed: {exc}")
        sys.exit(1)
