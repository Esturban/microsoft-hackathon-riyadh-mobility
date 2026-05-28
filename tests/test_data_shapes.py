import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "app" / "static" / "sample-data"


def test_sample_geojson_shapes():
    for file_name in (
        "riyadh_metro_lines_sample.geojson",
        "riyadh_bus_routes_sample.geojson",
        "district_centers_sample.geojson",
    ):
        payload = json.loads((SAMPLE_DIR / file_name).read_text(encoding="utf-8"))
        assert payload["type"] == "FeatureCollection"
        assert len(payload["features"]) > 0
