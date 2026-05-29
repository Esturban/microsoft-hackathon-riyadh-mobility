from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SAMPLE_DIR = BASE_DIR / "app" / "static" / "sample-data"


def detect_geometry(record: dict):
    for key in ("geo_shape", "geometry", "geoshape", "shape"):
        value = record.get(key)
        if isinstance(value, dict) and value.get("type") and value.get("coordinates"):
            return value
        if (
            isinstance(value, dict)
            and value.get("type") == "Feature"
            and isinstance(value.get("geometry"), dict)
            and value["geometry"].get("type")
            and value["geometry"].get("coordinates")
        ):
            return value["geometry"]
    return None


def canonical_properties(raw_name: str, record: dict) -> dict:
    if raw_name == "metro.json":
        line_code = str(record.get("metroline") or record.get("index") or "metro")
        line_name = record.get("metrolinename") or line_code
        return {
            "id": f"metro-{line_code.lower()}",
            "routeId": f"metro-{line_code.lower()}",
            "name": line_name,
            "lineColor": record.get("m_linecolorcode") or "#2563eb",
            "source": "rcrc",
        }

    route_code = str(record.get("busroutecode") or record.get("busroute") or record.get("index") or "bus")
    origin = record.get("origin")
    destination = record.get("destination")
    route_name = f"Bus {route_code}"
    if origin and destination and origin != "NA" and destination != "NA":
        route_name = f"Bus {route_code}: {origin} to {destination}"
    return {
        "id": f"bus-{route_code.lower()}",
        "routeId": f"bus-{route_code.lower()}",
        "name": route_name,
        "lineColor": "#f97316",
        "source": "rcrc",
    }


def normalize_file(raw_name: str, output_name: str) -> None:
    raw_path = RAW_DIR / raw_name
    if not raw_path.exists():
        print(f"skip missing {raw_path}")
        return

    payload = json.loads(raw_path.read_text(encoding="utf-8"))
    records = payload.get("results", payload.get("records", []))
    features = []
    for record in records:
        geometry = detect_geometry(record)
        if not geometry:
            continue
        properties = {k: v for k, v in record.items() if k not in {"geometry", "geo_shape", "geoshape", "shape"}}
        properties.update(canonical_properties(raw_name, record))
        features.append(
            {
                "type": "Feature",
                "properties": properties,
                "geometry": geometry,
            }
        )

    feature_collection = {"type": "FeatureCollection", "features": features}
    if feature_collection["type"] != "FeatureCollection":
        raise ValueError("invalid GeoJSON output")

    for target_dir in (PROCESSED_DIR, SAMPLE_DIR):
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / output_name).write_text(
            json.dumps(feature_collection, indent=2),
            encoding="utf-8",
        )
    print(f"normalized {raw_name} -> {output_name}")


def main() -> None:
    normalize_file("metro.json", "metro_lines.geojson")
    normalize_file("bus.json", "bus_routes.geojson")


if __name__ == "__main__":
    main()
