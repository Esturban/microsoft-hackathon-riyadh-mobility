from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "app" / "static" / "sample-data"


def validate_geojson(file_name: str) -> None:
    payload = json.loads((SAMPLE_DIR / file_name).read_text(encoding="utf-8"))
    if payload.get("type") != "FeatureCollection":
        raise ValueError(f"{file_name} is not a FeatureCollection")
    print(f"ok {file_name}: {len(payload.get('features', []))} features")


if __name__ == "__main__":
    validate_geojson("riyadh_metro_lines_sample.geojson")
    validate_geojson("riyadh_bus_routes_sample.geojson")
    validate_geojson("district_centers_sample.geojson")
