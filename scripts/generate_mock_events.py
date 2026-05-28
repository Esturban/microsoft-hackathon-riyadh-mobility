from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "app" / "static" / "sample-data" / "mock_live_events_sample.json"

ROUTES = ["bus-route-12", "bus-route-22", "metro-blue-line", "metro-red-line"]
DISTRICTS = [
    ("central-riyadh", 24.7136, 46.6753),
    ("olaya", 24.6950, 46.6750),
    ("malaz", 24.6660, 46.7230),
]


def make_event(index: int) -> dict:
    district_id, lat, lon = random.choice(DISTRICTS)
    severity = random.choice(["low", "medium", "high"])
    return {
        "id": f"event-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{index:04d}",
        "routeId": random.choice(ROUTES),
        "districtId": district_id,
        "eventType": random.choice(["delay", "congestion"]),
        "severity": severity,
        "delayMinutes": 0 if severity == "low" else random.randint(4, 15),
        "lat": lat,
        "lon": lon,
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "source": "simulator",
    }


if __name__ == "__main__":
    events = [make_event(index) for index in range(1, 6)]
    OUTPUT_FILE.write_text(json.dumps(events, indent=2), encoding="utf-8")
    print(f"generated {OUTPUT_FILE}")
