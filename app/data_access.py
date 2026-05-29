from __future__ import annotations

import json
import logging
from collections.abc import Iterable
from pathlib import Path

from .azure_clients import get_blob_service_client, get_cosmos_database_client
from .config import get_settings
from .scoring import compute_accessibility_score, compute_delay_penalty

logger = logging.getLogger(__name__)


def _prefers_mode(*allowed: str) -> bool:
    return get_settings().data_mode.lower() in allowed


def _read_json_file(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_sample_geojson(mode: str) -> tuple[dict, str]:
    settings = get_settings()
    file_map = {
        "metro": settings.sample_metro_file,
        "bus": settings.sample_bus_file,
        "districts": settings.sample_district_file,
    }
    return _read_json_file(file_map[mode]), "sample"


def _load_sample_events() -> tuple[list[dict], str]:
    settings = get_settings()
    return _read_json_file(settings.sample_events_file), "sample"


def _load_blob_json(blob_name: str):
    settings = get_settings()
    blob_service = get_blob_service_client()
    if blob_service is None:
        return None
    try:
        container = blob_service.get_container_client(
            settings.azure_storage_container_processed
        )
        full_name = f"{settings.blob_geojson_prefix}{blob_name}"
        payload = container.download_blob(full_name).readall()
        return json.loads(payload)
    except Exception as exc:  # pragma: no cover - network dependency
        logger.warning("Blob fallback triggered for %s: %s", blob_name, exc)
        return None


def _query_cosmos_items(container_name: str) -> list[dict] | None:
    db = get_cosmos_database_client()
    if db is None:
        return None
    try:
        container = db.get_container_client(container_name)
        items = list(container.query_items("SELECT * FROM c", enable_cross_partition_query=True))
        return items
    except Exception as exc:  # pragma: no cover - network dependency
        logger.warning("Cosmos fallback triggered for %s: %s", container_name, exc)
        return None


def _summarize_geojson(geojson: dict, mode: str) -> list[dict]:
    features = geojson.get("features", [])
    summaries = []
    seen = set()
    geometry_path_map = {
        "metro": "processed-data/metro_lines.geojson",
        "bus": "processed-data/bus_routes.geojson",
    }
    for feature in features:
        props = feature.get("properties", {})
        route_id = props.get("routeId") or props.get("id") or props.get("name")
        if route_id in seen:
            continue
        seen.add(route_id)
        summaries.append(
            {
                "id": route_id,
                "type": mode,
                "source": props.get("source", "sample"),
                "name": props.get("name", route_id),
                "mode": mode,
                "lineColor": props.get("lineColor", "#888888"),
                "featureCount": 1,
                "geometryBlobPath": geometry_path_map[mode],
                "lastUpdatedUtc": props.get("lastUpdatedUtc", "2026-05-24T00:00:00Z"),
            }
        )
    return summaries


def load_route_geojson(mode: str) -> tuple[dict, str]:
    settings = get_settings()
    blob_map = {
        "metro": settings.metro_blob_name,
        "bus": settings.bus_blob_name,
    }
    if _prefers_mode("blob", "auto", "cosmos"):
        blob_payload = _load_blob_json(blob_map[mode])
        if blob_payload:
            return blob_payload, "blob"
    return _load_sample_geojson(mode)


def load_route_summaries() -> tuple[list[dict], str]:
    settings = get_settings()
    if _prefers_mode("cosmos", "auto"):
        cosmos_items = _query_cosmos_items(settings.cosmos_routes_container)
        if cosmos_items:
            return cosmos_items, "cosmos"

    metro_geojson, metro_source = load_route_geojson("metro")
    bus_geojson, bus_source = load_route_geojson("bus")
    summaries = _summarize_geojson(metro_geojson, "metro") + _summarize_geojson(
        bus_geojson, "bus"
    )
    return summaries, "sample" if "sample" in {metro_source, bus_source} else "blob"


def _count_features_near_point(
    geojson: dict, center_lat: float, center_lon: float, buffer_km: float
) -> int:
    from .scoring import haversine_km

    count = 0
    for feature in geojson.get("features", []):
        for lon, lat in _iter_feature_points(feature):
            if haversine_km(center_lat, center_lon, lat, lon) <= buffer_km:
                count += 1
                break
    return count


def _iter_feature_points(feature: dict) -> Iterable[tuple[float, float]]:
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


def load_districts() -> tuple[list[dict], str]:
    settings = get_settings()
    if _prefers_mode("cosmos", "auto"):
        cosmos_items = _query_cosmos_items(settings.cosmos_districts_container)
        if cosmos_items:
            return cosmos_items, "cosmos"

    blob_payload = (
        _load_blob_json(settings.district_blob_name)
        if _prefers_mode("blob", "auto", "cosmos")
        else None
    )
    geojson, source = (blob_payload, "blob") if blob_payload else _load_sample_geojson(
        "districts"
    )

    metro_geojson, _ = load_route_geojson("metro")
    bus_geojson, _ = load_route_geojson("bus")
    events, _ = load_live_events()

    districts = []
    for feature in geojson.get("features", []):
        props = feature.get("properties", {})
        lon, lat = feature["geometry"]["coordinates"]
        metro_count = _count_features_near_point(
            metro_geojson, lat, lon, settings.access_buffer_km
        )
        bus_count = _count_features_near_point(
            bus_geojson, lat, lon, settings.access_buffer_km
        )
        delay_penalty = (
            compute_delay_penalty(lat, lon, events, settings.access_buffer_km)
            if settings.enable_live_events
            else 0
        )
        score_data = compute_accessibility_score(metro_count, bus_count, delay_penalty)
        doc = {
                "id": f"district-{props['districtId']}",
                "districtId": props["districtId"],
                "name": props["name"],
                "center": {"lat": lat, "lon": lon},
                "nearbyMetroCount": metro_count,
                "nearbyBusCount": bus_count,
                "accessibilityScore": score_data["score"],
                "accessibilityRating": score_data["rating"],
                "lastCalculatedUtc": "2026-05-24T00:00:00Z",
            }
        if props.get("nameAr"):
            doc["nameAr"] = props["nameAr"]
        if props.get("description"):
            doc["description"] = props["description"]
        districts.append(doc)
    return districts, source


def load_live_events() -> tuple[list[dict], str]:
    settings = get_settings()
    if _prefers_mode("cosmos", "auto"):
        cosmos_items = _query_cosmos_items(settings.cosmos_events_container)
        if cosmos_items:
            return cosmos_items, "cosmos"

    if _prefers_mode("blob", "auto", "cosmos"):
        blob_payload = _load_blob_json(settings.live_events_blob_name)
        if blob_payload:
            return blob_payload, "blob"
    return _load_sample_events()


def get_district_score(district_id: str) -> tuple[dict | None, str]:
    districts, source = load_districts()
    for district in districts:
        if district["districtId"] == district_id:
            events, _ = load_live_events()
            penalty = (
                compute_delay_penalty(
                    district["center"]["lat"],
                    district["center"]["lon"],
                    events,
                    get_settings().access_buffer_km,
                )
                if get_settings().enable_live_events
                else 0
            )
            score_data = compute_accessibility_score(
                district["nearbyMetroCount"], district["nearbyBusCount"], penalty
            )
            return {
                **district,
                "liveDelayPenalty": penalty,
                "formula": score_data["formula"],
                "disclaimer": (
                    "This score is a hackathon-friendly proxy. It is not a formal "
                    "transport-planning model. It is designed to show how public "
                    "mobility data, cloud storage, and simple analytics can support "
                    "district-level planning conversations."
                ),
            }, source
    return None, source


def get_data_status() -> dict:
    route_items, route_source = load_route_summaries()
    _, district_source = load_districts()
    events, events_source = load_live_events()
    settings = get_settings()
    return {
        "requestedMode": settings.data_mode,
        "routes": {"count": len(route_items), "source": route_source},
        "districts": {"source": district_source},
        "liveEvents": {
            "enabled": settings.enable_live_events,
            "source": events_source,
            "count": len(events),
        },
        "activeMode": (
            "cosmos"
            if "cosmos" in {route_source, district_source, events_source}
            else "blob"
            if "blob" in {route_source, district_source, events_source}
            else "sample"
        ),
        "fallbackMessage": (
            "Azure services are optional. The app falls back to bundled sample files "
            "when Blob Storage or Cosmos DB is unavailable."
        ),
    }
