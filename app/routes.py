from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from .config import get_settings
from .data_access import (
    get_data_status,
    get_district_score,
    load_districts,
    load_live_events,
    load_route_geojson,
    load_route_summaries,
)

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/api/config")
def config():
    settings = get_settings()
    return {
        "appName": settings.app_name,
        "azureMapsEnabled": bool(settings.azure_maps_key),
        "azureMapsKey": settings.azure_maps_key,
        "azureMapsClientId": settings.azure_maps_client_id,
        "riyadhCenter": {"lat": 24.7136, "lon": 46.6753},
        "accessBufferKm": settings.access_buffer_km,
    }


@router.get("/api/routes")
def routes():
    items, source = load_route_summaries()
    return {"items": items, "source": source}


@router.get("/api/routes/geojson")
def routes_geojson(mode: str = Query(..., pattern="^(metro|bus)$")):
    geojson, source = load_route_geojson(mode)
    return {"source": source, "geojson": geojson}


@router.get("/api/districts")
def districts():
    items, source = load_districts()
    return {"items": items, "source": source}


@router.get("/api/score")
def score(districtId: str):
    item, source = get_district_score(districtId)
    if item is None:
        raise HTTPException(status_code=404, detail="District not found")
    return {"item": item, "source": source}


@router.get("/api/live-events")
def live_events():
    items, source = load_live_events()
    return {"items": items, "source": source}


@router.get("/api/data-status")
def data_status():
    return get_data_status()
