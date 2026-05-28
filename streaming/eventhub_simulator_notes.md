# Event Hub Simulator Notes

Stretch path:

1. Run `python scripts/generate_mock_events.py`
2. Publish JSON messages to `mobility-events`
3. Let Stream Analytics aggregate route and district alerts
4. Upsert latest events into Cosmos DB for `/api/live-events`
