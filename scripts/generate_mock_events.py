from __future__ import annotations

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
 
from azure.eventhub import EventData, EventHubProducerClient

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


def send_to_event_hub(events: list[dict]) -> None:
    connection_string = os.getenv("EVENT_HUB_CONNECTION_STRING")
    event_hub_name = os.getenv("EVENT_HUB_NAME", "mobility-events")
    if not connection_string:
        print("event hubs not configured; local-only mode")
        return

    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_string,
        eventhub_name=event_hub_name,
    )
    with producer:
        batch = producer.create_batch()
        for event in events:
            batch.add(EventData(json.dumps(event)))
        producer.send_batch(batch)
    print(f"published {len(events)} events to Event Hubs: {event_hub_name}")


if __name__ == "__main__":
    events = [make_event(index) for index in range(1, 6)]
    OUTPUT_FILE.write_text(json.dumps(events, indent=2), encoding="utf-8")
    print(f"generated {OUTPUT_FILE}")
    send_to_event_hub(events)
