---
title: "Riyadh Mobility Intelligence Starter Kit"
subtitle: "Builder Companion for the Riyadh Urban Intelligence Lab"
author: "Prepared for atomcamp Arabia and the Riyadh Urban Development Hackathon in collaboration with Microsoft"
date: "2026-05-30"
lang: "en-US"
---

# Riyadh Mobility Intelligence Starter Kit

## Builder Companion for the Riyadh Urban Intelligence Lab

Prepared for atomcamp Arabia and the Riyadh Urban Development Hackathon in collaboration with Microsoft.

You have the code. This companion explains what the starter kit is, how it fits the hackathon tracks, how the app is built, and how teams can adapt it into their own mobility, district intelligence, sustainability, or visitor-experience prototypes.

This is a client-facing builder guide. It is not meant to document every internal line of code. It gives participants, mentors, and stakeholders a clear map of the product, the architecture, the Azure services, and the extension routes.

## Before You Start

This guide accompanies the `riyadh-mobility-intelligence-dashboard` codebase. It is written for hackathon builders who need to understand the app quickly, run it locally, explain it to mentors, and adapt it into a track-aligned MVP.

After following this guide, a builder should be able to:

- run the starter kit locally with bundled sample data
- explain the app as a mobility intelligence scaffold, not only a dashboard
- identify how FastAPI, Vanilla JavaScript, Azure Maps, Blob Storage, Cosmos DB, and Container Apps fit together
- connect the app to a cloud-live Azure path when ready
- adapt the scaffold for another Riyadh Urban Intelligence Lab track
- prepare a short judge-facing demo

What you need before starting:

- Python 3.11 or newer
- Git and a code editor
- terminal access
- optional Azure account for the cloud-live path
- optional Azure CLI and Azure Developer CLI for deployment

Companion references to keep nearby:

| Document | Use it for |
|---|---|
| `README.md` | student quickstart, local run, deploy, demo flow, and troubleshooting |
| `docs/README.md` | documentation map for supporting notes |
| `docs/rebuild_guide.md` | editable source for this companion |
| `docs/rebuild_guide.docx` | polished handout version |

[Icon placement: partner/program row]  
Add approved atomcamp Arabia, Microsoft, Riyadh Urban Intelligence Lab, and strategic partner marks here if brand assets are available.

# Section 0 — What You’re Building

This application is a **Mobility Intelligence Starter Kit** for Riyadh. It helps teams explore public transport access, route visibility, district scoring, and cloud-live data architecture through one approachable web app.

The starter kit shows:

- Riyadh metro lines and bus routes on a map
- district selection and district-level mobility scoring
- route and event overlays
- a fallback-aware data path using bundled sample files
- an Azure-backed live layer for deployment and data services
- a pattern that can be reused for other hackathon tracks

The important point is that this is not only a one-off mobility dashboard. It is a reusable scaffold for building urban intelligence applications during a four-day hackathon.

## Product Story

The app answers a simple question:

> If a user selects a district in Riyadh, can we show nearby mobility infrastructure, explain the available route coverage, and turn that into a clear starter score?

The current score is intentionally transparent:

```text
score = (nearby metro count x 3) + nearby bus count - live delay penalty
```

This is not an official transport model. It is a teachable proxy that lets teams understand how data, scoring, APIs, map layers, and Azure services connect.

## Services at a Glance

| Layer | What it does | Main files or services |
|---|---|---|
| Web app | Serves the API and frontend | FastAPI, `app/main.py`, `app/routes.py` |
| Frontend | Shows the map, panels, toggles, and score | Vanilla JavaScript under `app/static/src/` |
| Map layer | Displays Riyadh mobility layers | Azure Maps with local fallback |
| Data layer | Loads sample, Blob, or Cosmos-backed data | `app/data_access.py`, sample GeoJSON/JSON |
| Scoring layer | Calculates district mobility score | `app/scoring.py` |
| Cloud-live layer | Hosts and observes the deployed app | Container Apps, Blob Storage, Cosmos DB, App Insights |

Show the browser view with the map centered on Riyadh, metro and bus layers available, district selector visible, and the scoring panel open.

[Screenshot placeholder: dashboard loaded locally]  

# Section 1 — Hackathon Track Fit

The Riyadh Urban Intelligence Lab is structured around four thematic tracks aligned to Riyadh urban challenges and Expo 2030 themes. This starter kit is built primarily for mobility, but it intentionally overlaps with more than one track.

## Track Mapping

| Hackathon track | How this starter kit fits | Builder route |
|---|---|---|
| Transformational Technology | Mobility dashboard, route overlays, congestion proxy, parking or delay extensions | turn the map into a live mobility command view |
| Prosperous People | 15-minute city thinking, access scoring, district intelligence, walkability proxy | extend district scoring into service access and walkability |
| Sustainable Solutions | mobility and pollution overlay, heat-stress routing, clean corridor recommendations | combine route data with AQI, heat, or emissions layers |
| Culture | visitor movement, crowd routing, heritage access, event mobility planning | adapt the map for cultural routes and visitor experience |

## Best Primary Fit

The strongest primary fit is **Transformational Technology** because the app already focuses on public transport visibility, route layers, and mobility intelligence.

The strongest secondary fit is **Prosperous People** because the district scoring pattern can become a 15-minute city or walkability-access score.

Sustainable Solutions and Culture are extension routes. They are not the first build path, but the same scaffold can support them once the core mobility app works.

## Track-Aligned Pitch

Use this pitch when presenting the starter kit:

```text
This starter kit helps teams build a Riyadh mobility intelligence prototype using public route data, district scoring, Azure Maps, and an Azure-backed live layer. It supports the Transformational Technology track directly and can be extended into Prosperous People, Sustainable Solutions, or Culture use cases.
```

Add one small icon for each track: mobility/technology, people/districts, sustainability/environment, culture/visitor experience.

[Icon placement: four hackathon tracks]  

# Section 2 — Architecture at a Glance

The app is designed to work locally first and then graduate into a cloud-live Azure path.

## Local-First Path

Local mode is the first build milestone. It should work even when the builder has no Azure credentials.

```text
Browser
  -> FastAPI on localhost
    -> static frontend
    -> bundled sample GeoJSON and JSON
    -> scoring logic
```

Key design principle: the app should always be explainable from local sample data. If cloud services are unavailable, the product story should still work.

## Azure-Backed Live Path

The cloud-live path keeps the same app shape but connects it to deployable Azure services.

```text
Browser
  -> Azure Container App
    -> FastAPI + static frontend
    -> Azure Maps
    -> Blob Storage
    -> Cosmos DB
    -> Application Insights / Log Analytics
```

This is not meant to become an enterprise platform during the hackathon. It is a credible deployment-ready starter kit that shows how a city app could move from local demo to pilot conversation.

Show a simple layer diagram with Browser, Container Apps, FastAPI, Azure Maps, Blob Storage, Cosmos DB, and App Insights.

[Screenshot placeholder: Azure service layer diagram]  

# Section 3 — Project Structure

The project is intentionally small. Builders should be able to find the app shell, API, frontend, sample data, and deployment path quickly.

```text
riyadh-mobility-intelligence-dashboard/
├── app/
│   ├── main.py                  # FastAPI app shell and static serving
│   ├── routes.py                # API endpoints
│   ├── data_access.py           # sample, Blob, Cosmos data loading
│   ├── scoring.py               # district mobility score
│   ├── azure_clients.py         # Azure SDK client setup
│   └── static/
│       ├── index.html           # single-page dashboard shell
│       ├── src/                 # frontend JavaScript and CSS
│       └── sample-data/         # always-on sample files
├── scripts/                     # fetch, normalize, upload, seed, validate
├── infra/                       # Bicep modules
├── docs/                        # polished rebuild guide
├── tests/                       # scoring, API, and data-shape checks
└── azure.yaml                   # Azure Developer CLI project
```

## File Map

| Area | Start here | Why it matters |
|---|---|---|
| Backend | `app/main.py`, `app/routes.py` | app shell and API contract |
| Data | `app/data_access.py`, `app/static/sample-data/` | fallback-aware data loading |
| Scoring | `app/scoring.py` | transparent district score |
| Frontend | `app/static/src/main.js`, `map.js`, `layers.js` | app boot, map, and overlays |
| Deployment | `azure.yaml`, `infra/main.bicep`, `scripts/deploy_azure.sh` | cloud-live path |
| Demo | `README.md` | short judge-facing narrative |

Use a five-icon row for Backend, Data, Map, Scoring, Cloud-Live.

[Icon placement: app layers]  

# Section 4 — Running It Locally

Local setup is deliberately simple. The first goal is to get a useful screen running before adding cloud services.

## Step 1: Create the Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Step 2: Start the App

```bash
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Without `AZURE_MAPS_KEY`, the app should still run with the local map fallback and sample data.

## Step 3: Check the API

Open these endpoints:

```text
/health
/api/config
/api/routes
/api/districts
/api/data-status
```

The `/api/data-status` endpoint is especially useful because it tells builders which data source is active and whether the fallback path is working.

Show the dashboard loaded in the browser with metro, bus, district, and score UI visible.

[Screenshot placeholder: local dashboard]  

Show the JSON response that explains the active data source.

[Screenshot placeholder: `/api/data-status`]  

# Section 5 — How the Backend Works

The backend is a small FastAPI application. It serves both the API and the static frontend so the starter kit stays easy to run and deploy.

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | confirms the app is alive |
| `GET /api/config` | gives the frontend runtime configuration |
| `GET /api/routes` | returns route summaries and KPI data |
| `GET /api/routes/geojson?mode=metro-or-bus` | returns map-ready route geometry |
| `GET /api/districts` | returns district selector data |
| `GET /api/score?districtId=...` | returns district score and score components |
| `GET /api/live-events` | returns mock or configured event overlays |
| `GET /api/data-status` | explains active data source and fallback status |

## Fallback Chain

The running app should not depend on live external data endpoints. Data fetches happen through scripts. The app reads prepared local or Azure-backed data.

```text
Cosmos DB records
  -> Blob Storage files
    -> bundled sample files
```

Key design principle: if Azure data is unavailable, the app should fall back to sample files instead of failing during a workshop or judging demo.

## Scoring

The score is intentionally easy to explain:

```text
score = (nearby metro count x 3) + nearby bus count - live delay penalty
```

The score lives on the backend so it can be tested, reused, and explained as part of the API contract.

# Section 6 — How the Frontend Works

The frontend is a single-page application built with Vanilla JavaScript. This keeps the hackathon starter kit accessible to mixed-experience teams.

## App Boot

`main.js` coordinates the page. On startup, it fetches configuration, route summaries, GeoJSON, districts, live events, and data status.

```javascript
const [config, routes, metro, bus, districts, events, dataStatus] = await Promise.all([
  api.getConfig(),
  api.getRoutes(),
  api.getRouteGeojson("metro"),
  api.getRouteGeojson("bus"),
  api.getDistricts(),
  api.getLiveEvents(),
  api.getDataStatus(),
]);
```

## Map Layers

The map layer system should make the city data visible and explainable.

| Layer | What it shows |
|---|---|
| Metro lines | high-capacity mobility corridors |
| Bus routes | surface transit coverage |
| Districts | selectable district points |
| Live events | route delay or incident markers |
| Accessibility buffer | rough selected-district service area |

Show the map with route overlays, toggles, and selected district focus.

[Screenshot placeholder: map with metro and bus layers]  

## District Score Panel

The score panel translates raw counts into a judge-friendly story:

- selected district name
- score number
- metro and bus counts
- live-event penalty
- explanation of the formula
- active data source

Show a selected district with the score, formula components, and data source badge.

[Screenshot placeholder: district score panel]  

# Section 7 — Cloud-Live Path

The cloud-live path is the deployable version of the same starter kit. It shows how a hackathon prototype can become credible enough for pilot discussion.

## Azure Services

| Service | Role in the starter kit |
|---|---|
| Azure Container Apps | hosts FastAPI and the static frontend |
| Azure Container Registry | stores the built container image |
| Azure Maps | provides cloud-native map services |
| Blob Storage | stores raw and processed mobility files |
| Cosmos DB | stores app-shaped route, district, and event records |
| Application Insights | tracks app health and API failures |
| Log Analytics | supports logs and diagnostics |
| Azure Developer CLI | deploys the app and infrastructure |
| Bicep | defines the Azure resources in code |

## Deploy

```bash
az login
azd auth login
azd init
bash scripts/deploy_azure.sh
```

After deployment:

- open the deployed app URL
- check `/health`
- check `/api/data-status`
- upload or seed cloud data if using Blob or Cosmos
- inspect App Insights if the deployed app fails

Show the deployed app URL in a browser with route layers and score panel visible.

[Screenshot placeholder: deployed app running on Azure]  

# Section 8 — Starter Kit Routes

This codebase should be treated as a scaffold. Teams can reuse the same architecture for different urban intelligence ideas.

## Route 1: Mobility Command View

Best for Transformational Technology.

Keep:

- route layers
- event overlay
- district selector
- route KPIs

Add:

- congestion forecast API
- parking demand layer
- peak-load simulation
- route delay explanations

Starter-kit route: turn the current dashboard into a live mobility command view for mentors and judges.

## Route 2: District Intelligence

Best for Prosperous People.

Keep:

- district selector
- scoring panel
- map focus behavior
- Cosmos-backed district records

Add:

- 15-minute city compliance indicators
- walkability score
- service access layers
- district comparison panel

Starter-kit route: evolve the score from mobility access into district intelligence.

## Route 3: Sustainable Mobility Overlay

Best for Sustainable Solutions.

Keep:

- mobility layers
- selected district context
- route scoring pattern

Add:

- AQI or heat layer
- pollution hotspot markers
- clean corridor recommendations
- heat-stress routing notes

Starter-kit route: combine mobility with environmental conditions for cleaner route planning.

## Route 4: Culture and Visitor Movement

Best for Culture.

Keep:

- map layer structure
- event markers
- route overlays
- selected place or district panel

Add:

- heritage site markers
- crowd-sensitive route suggestions
- multilingual visitor notes
- event-day access planning

Starter-kit route: adapt the map into a visitor mobility and cultural access prototype.

# Section 9 — Single Page Now, Multi-Page Later

The current app works as a single-page application. That is the right starting point for a hackathon because it keeps the product easy to run, inspect, and present.

As the starter kit grows, it can become a multi-page application.

| Future page | Purpose | When to add it |
|---|---|---|
| `/dashboard` | main map and scoring view | when the app needs a cleaner landing route |
| `/data-status` | human-readable source and fallback view | when mentors need to inspect cloud-live state |
| `/demo` | judge-facing presentation mode | when preparing final pitches |
| `/admin` | data refresh or seeding controls | when scripts become too hidden for teams |
| `/extensions` | track-specific starter routes | when multiple teams reuse the scaffold |

Key design principle: keep the first useful version single-page. Add pages only when they clarify the builder or demo experience.

# Section 10 — Demo and Extension Ideas

## Judge-Facing Demo Flow

Use the demo script in `README.md` as the short presentation reference.

| Step | Show | Explain |
|---:|---|---|
| 1 | dashboard landing view | the app is a Riyadh mobility starter kit |
| 2 | metro and bus toggles | map layers show mobility infrastructure |
| 3 | district selector | district context drives scoring |
| 4 | score panel | score is transparent and easy to adjust |
| 5 | `/api/data-status` | app is fallback-aware and cloud-live ready |
| 6 | Azure layer diagram | services map cleanly to hosting, map, files, records, and monitoring |
| 7 | starter kit routes | the same scaffold supports multiple hackathon tracks |

## Safe Extensions

Good first extensions:

- add more districts or points of interest
- add a parking or congestion layer
- adjust score weights by track
- add event severity to the KPI panel
- add a Power BI export path
- add a demo presentation page

Stretch extensions:

- Event Hubs for live event ingestion
- Stream Analytics for live aggregation
- plain-English score explanations in the frontend or API
- Azure Digital Twins for district or event simulation
- Power Apps for field-service workflows

# Appendix — Quick Reference

## Common Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
pytest
bash scripts/deploy_azure.sh
```

## Reference Index

| Need | Open |
|---|---|
| student quickstart | `README.md` |
| run, test, deploy, troubleshoot | `README.md` |
| demo script | `README.md` |
| documentation index | `docs/README.md` |
| builder companion source | `docs/rebuild_guide.md` |
| polished builder companion | `docs/rebuild_guide.docx` |

## Visual Asset Checklist

| Asset slot | Recommended visual |
|---|---|
| partner/program row | approved atomcamp Arabia, Microsoft, Riyadh Urban Intelligence Lab, and partner marks |
| dashboard loaded locally | browser screenshot with map, layers, district selector, and score panel |
| four hackathon tracks | compact icon row for technology, people, sustainability, and culture |
| Azure service layer diagram | simple diagram from browser to Container Apps, FastAPI, Azure Maps, Blob, Cosmos, and App Insights |
| app layers | icon row for Backend, Data, Map, Scoring, and Cloud-Live |
| `/api/data-status` | JSON screenshot showing active data source and fallback status |
| deployed app | browser screenshot of the Azure-hosted app |

## Glossary

**Azure-backed live layer**  
The deployable path where the starter kit uses Azure services for maps, hosting, files, records, and monitoring.

**Blob Storage**  
Azure file storage for raw and processed mobility datasets.

**Cosmos DB**  
Azure document database for route summaries, district records, and event records.

**FastAPI**  
Python web framework used to serve the API and static frontend.

**GeoJSON**  
JSON format for map features such as points, lines, and polygons.

**Mobility Intelligence Starter Kit**  
The reusable scaffold that teams can adapt into mobility, district, sustainability, or culture prototypes.

**Sample fallback**  
The local files that keep the app useful even when cloud services or remote data are unavailable.

**Single-page application**  
The current frontend shape: one main web page that loads data and updates panels dynamically.

# Closing Note

The starter kit is strongest when it stays practical: one useful local screen, clear route layers, transparent scoring, and a cloud-live path that is credible without becoming heavy. Build the smallest version that can be explained well, then extend it toward the hackathon track that matters most.
