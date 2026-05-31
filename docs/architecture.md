# Architecture

## System Overview

The app runs as a single-container web application with fallback-aware data loading and an optional Azure path.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  RIYADH MOBILITY INTELLIGENCE DASHBOARD                                     │
│  Microsoft Hackathon · atomcamp Arabia · Riyadh Urban Intelligence Lab      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Local-First Path (no Azure credentials needed)

```
Browser (http://localhost:8000)
│
▼
FastAPI  ──────────────────────────────────────┐
│                                              │
├── GET /                 serves index.html    │  app/
├── GET /src/main.js      serves JS modules    │  static/
├── GET /src/map.js                            │
├── GET /src/layers.js                         │
├── GET /src/scoringPanel.js                   │
│                                              │
├── GET /api/config       → runtime config     │  app/
├── GET /api/routes       → route summaries    │  routes.py
├── GET /api/routes/geojson?mode=metro|bus     │
├── GET /api/districts    → district list      │
├── GET /api/score        → district score     │
├── GET /api/live-events  → event markers      │
├── GET /api/data-status  → fallback state     │
└── GET /health           → liveness probe     │
                                               │
└── Sample Data (always-on fallback)           │  app/static/
    ├── riyadh_metro_lines_sample.geojson      │  sample-data/
    ├── riyadh_bus_routes_sample.geojson       │
    ├── district_centers_sample.geojson        │
    └── mock_live_events_sample.json           │
```

---

## Azure-Live Path (deployed)

```
Browser
│
▼
Azure Container Apps  (hosts FastAPI + static frontend)
│
├── Azure Maps API ──────────────────────── map tiles and layer rendering
│
├── Azure Blob Storage ──────────────────── processed GeoJSON/JSON files
│   ├── raw-data/           raw RCRC exports
│   └── processed-data/     normalized GeoJSON (metro, bus, districts)
│
├── Azure Cosmos DB ─────────────────────── app-shaped document store
│   ├── routes container    route summaries and KPI data
│   ├── districts container district records (name, nameAr, description)
│   └── events container    live-event overlays
│
└── Application Insights + Log Analytics ── telemetry and diagnostics
```

---

## Data Fallback Chain

```
Request for routes / districts / events
│
▼
Is DATA_MODE=cosmos AND Cosmos credentials present?
├── YES → read from Cosmos DB  ──────────────────────── live records
│
▼
Is DATA_MODE=blob AND Blob credentials present?
├── YES → read from Azure Blob Storage  ─────────────── processed files
│
▼
Fall back to bundled sample files  ──────────────────── always works
    app/static/sample-data/
```

Always keep the app working from sample data. If Azure services are unavailable, fall back to bundled files.

---

## Scoring Logic

```
Selected district (lat, lon)
│
├── FIND: metro stops within access_buffer_km (default 1.5 km)
│         → nearby_metro_count
│
├── FIND: bus routes within access_buffer_km
│         → nearby_bus_count
│
├── FIND: live events with severity ≥ medium within buffer
│         → live_delay_penalty
│
└── COMPUTE:
    score = (nearby_metro_count × 3) + nearby_bus_count − live_delay_penalty

    rating: score < 5  → Low
            score < 10 → Medium
            score ≥ 10 → High
```

---

## Container Shape

```
Dockerfile
│
├── FROM python:3.12-slim
├── COPY requirements.txt → pip install
├── COPY app/ → FastAPI app
│   ├── main.py      app shell + static serving
│   ├── routes.py    API contract
│   ├── data_access.py   fallback-aware data loading
│   ├── scoring.py   district score formula
│   ├── azure_clients.py Azure SDK setup
│   └── static/      frontend + sample data
└── CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## File Map

```
riyadh-mobility-intelligence-dashboard/
│
├── app/
│   ├── main.py                 FastAPI shell, static serving, CORS
│   ├── routes.py               all API endpoints
│   ├── data_access.py          Cosmos / Blob / sample loader
│   ├── scoring.py              district score and delay penalty
│   ├── azure_clients.py        Cosmos and Blob SDK clients
│   ├── config.py               pydantic-settings for env vars
│   └── static/
│       ├── index.html          single-page dashboard shell
│       ├── src/
│       │   ├── main.js         app boot, fetch orchestration
│       │   ├── map.js          Azure Maps init and map control
│       │   ├── layers.js       metro / bus / event layer rendering
│       │   ├── scoringPanel.js district score panel
│       │   ├── api.js          fetch wrappers for all endpoints
│       │   └── styles.css      dashboard styles
│       └── sample-data/
│           ├── riyadh_metro_lines_sample.geojson    6 metro lines
│           ├── riyadh_bus_routes_sample.geojson     100 bus routes
│           ├── district_centers_sample.geojson      10 districts
│           └── mock_live_events_sample.json         sample events
│
├── scripts/
│   ├── fetch_rcrc_data.py          fetch raw RCRC exports
│   ├── normalize_to_geojson.py     normalize to app-shaped GeoJSON
│   ├── upload_to_blob.py           upload processed files to Blob
│   ├── seed_cosmos.py              seed Cosmos with route + district records
│   ├── validate_data.py            smoke-test sample file shapes
│   ├── generate_mock_events.py     generate mock live-event JSON
│   ├── deploy_azure.sh             thin deploy helper wrapping azd up
│   └── destroy_resource_group.sh  delete current resource group (--yes required)
│
├── infra/                          Bicep infrastructure modules
├── tests/                          pytest suite
├── docs/                           documentation
├── Dockerfile                      container definition
├── azure.yaml                      Azure Developer CLI project file
├── requirements.txt                Python dependencies
├── .env.example                    environment variable template
└── package.json                    npm scripts for common tasks
```

---

## Azure Services Summary

| Service | Role | Required for |
|---|---|---|
| Container Apps | hosts FastAPI and frontend | deployment |
| Container Registry | stores the built image | deployment |
| Azure Maps | cloud map tiles and layer API | production map view |
| Blob Storage | raw and processed data files | blob and auto mode |
| Cosmos DB | route, district, event documents | cosmos and auto mode |
| Application Insights | API health and error tracking | deployed app monitoring |
| Log Analytics | log aggregation and diagnostics | deployed app monitoring |
| Azure Developer CLI | one-command deploy and teardown | deployment workflow |
| Bicep | infrastructure-as-code | reproducible environments |

---

## Sequence: Browser to Score

```
User selects district
│
▼
Frontend sends GET /api/score?districtId=riyadh-north
│
▼
FastAPI routes.py receives request
│
▼
data_access.py loads district record (Cosmos / Blob / sample)
│
▼
scoring.py computes:
  → loads live events (sample or live)
  → counts metro stops within 1.5 km of district center
  → counts bus routes within 1.5 km of district center
  → counts delay-severity events within 1.5 km
  → returns score, rating, formula breakdown
│
▼
JSON response → scoringPanel.js renders result
```
