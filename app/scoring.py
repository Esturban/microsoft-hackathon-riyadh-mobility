from __future__ import annotations

from math import asin, cos, radians, sin, sqrt


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    return 2 * radius_km * asin(sqrt(a))


def rate_score(score: int) -> str:
    if score <= 2:
        return "Low"
    if score <= 6:
        return "Medium"
    return "High"


def compute_delay_penalty(
    center_lat: float, center_lon: float, events: list[dict], buffer_km: float
) -> int:
    penalty = 0
    for event in events:
        if event.get("severity") not in {"medium", "high"}:
            continue
        lat = event.get("lat")
        lon = event.get("lon")
        if lat is None or lon is None:
            continue
        if haversine_km(center_lat, center_lon, float(lat), float(lon)) <= buffer_km:
            penalty += 1
    return penalty


def compute_accessibility_score(
    nearby_metro_count: int,
    nearby_bus_count: int,
    live_delay_penalty: int = 0,
) -> dict:
    score = (nearby_metro_count * 3) + nearby_bus_count - live_delay_penalty
    return {
        "score": score,
        "rating": rate_score(score),
        "formula": {
            "nearbyMetroCount": nearby_metro_count,
            "nearbyBusCount": nearby_bus_count,
            "liveDelayPenalty": live_delay_penalty,
        },
    }
