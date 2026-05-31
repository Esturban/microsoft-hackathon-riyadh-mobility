# Extension Ideas

Ideas for teams to extend the starter kit during the hackathon. Organized by effort level and hackathon track alignment.

---

## Safe First Extensions (hours, not days)

These are low-risk additions that fit inside the existing architecture.

| Extension | Description | Track |
|---|---|---|
| Add more districts | Extend `district_centers_sample.geojson` with more Riyadh neighborhoods | Any |
| Adjust score weights | Change the metro, bus, and penalty multipliers in `app/scoring.py` | Any |
| Add parking layer | Add a GeoJSON file for parking locations and render it as a new map layer | Transformational Technology |
| Event severity panel | Show a count of low / medium / high severity events alongside the score | Transformational Technology |
| District comparison | Let users select two districts side-by-side and compare scores | Prosperous People |
| Walkability proxy | Replace the mobility score with a walkability calculation using pedestrian route data | Prosperous People |
| Power BI export | Add a `/api/export` endpoint that returns score data in a flat format for Power BI | Any |
| Demo presentation page | Add a `/demo` route that shows a simplified view for judge-facing presentations | Any |

---

## Medium Extensions (one to two days)

These require adding a new service or a new data source.

| Extension | Description | Track |
|---|---|---|
| AQI overlay | Fetch air quality index data and overlay it on the map as a color-coded layer | Sustainable Solutions |
| Heat stress routing | Use temperature data to suggest cooler route alternatives | Sustainable Solutions |
| Heritage site markers | Add a GeoJSON layer for UNESCO or national heritage sites | Culture |
| Event-day mobility | Load a special event dataset (Expo 2030, sports events) and adjust route recommendations | Culture |
| Live congestion proxy | Use traffic delay data to update the scoring penalty in near-real-time | Transformational Technology |
| Multilingual panel | Add Arabic text to the score panel alongside English labels | Any |

---

## Stretch Extensions (Azure-powered)

These use additional Azure services and demonstrate a more complete cloud architecture.

| Extension | Description | Azure Service | Track |
|---|---|---|---|
| Live event ingestion | Ingest real-time delay or incident events into the map | Event Hubs + Stream Analytics | Transformational Technology |
| Plain-English summaries | Generate a natural-language explanation of the district score | Azure OpenAI | Any |
| District simulation | Model the effect of a new bus route or metro stop on the score | Azure Digital Twins | Transformational Technology |
| Field service app | Build a simple field worker interface for route inspection | Power Apps + Cosmos DB | Transformational Technology |
| Carbon footprint layer | Estimate emissions per route based on distance and vehicle type | Blob Storage + custom scoring | Sustainable Solutions |
| Crowd density routing | Use pedestrian density estimates to suggest less congested walking routes | Azure Maps + custom data | Culture |

---

## How to Add a New Layer

The fastest path to extending the map is adding a GeoJSON layer:

1. Create or fetch a GeoJSON file and add it to `app/static/sample-data/`.
2. Add an API endpoint in `app/routes.py`.
3. Add a rendering function in `app/static/src/layers.js`.
4. Add a toggle in `app/static/index.html`.
5. Add a test in `tests/test_data_shapes.py`.

---

## How to Adjust the Score Formula

The score formula lives in `app/scoring.py`:

```python
score = (nearby_metro_count * METRO_WEIGHT) + nearby_bus_count - live_delay_penalty
```

To add a new scoring factor — for example, a walkability bonus:

```python
score = (
    (nearby_metro_count * METRO_WEIGHT)
    + nearby_bus_count
    + walkability_bonus
    - live_delay_penalty
)
```

Add the new variable to the `compute_accessibility_score` function signature, compute it from your new data source, and update the tests in `tests/test_scoring.py`.
