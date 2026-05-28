<!-- /autoplan restore point: /Users/EVA/.gstack/projects/riyadh_ud/main-autoplan-restore-20260528-104919.md -->
# Riyadh Mobility Intelligence Dashboard — Agent Build Spec v2

## TL;DR

Build a new beginner-friendly, deployable hackathon starter repo called:

```text
riyadh-mobility-intelligence-dashboard
```

This repo should help hackathon attendees build a simple Riyadh mobility dashboard using real public Riyadh transit data where possible, with bundled sample data as a fallback. The app should be basic enough for beginners to understand, but should use a meaningful Azure stack so it feels like a real smart-city MVP rather than a static map.

The first version should prioritize speed, reliability, and clarity. It should not use Kubernetes, complex authentication, real CCTV, or production-grade ML. The target is a working MVP that can be cloned, run locally, deployed to Azure, and extended by students during a four-day hackathon.

### Mandatory v1 Azure stack

| Layer | Azure service | Required in v1? | Purpose |
|---|---|---:|---|
| Hosting | Azure Container Apps | Yes | Host the web app/API in one lightweight container |
| Mapping | Azure Maps | Yes | Display Riyadh metro, bus, districts, and overlays |
| Raw data storage | Azure Blob Storage | Yes | Store raw and processed mobility datasets |
| App state | Azure Cosmos DB for NoSQL | Yes | Store processed route metadata, district scores, and latest mock events |
| Monitoring | Application Insights / Log Analytics | Yes | Track app health, logs, and API failures |
| Deployment | Azure Developer CLI + Bicep | Yes | Deploy reproducibly into one Azure resource group |

### Optional v1.5 / stretch Azure stack

| Layer | Azure service | Required? | Purpose |
|---|---|---:|---|
| Event ingestion | Azure Event Hubs | Optional | Simulate live delay/congestion events |
| Stream processing | Azure Stream Analytics | Optional | Aggregate live mobility events by route/district |
| Executive dashboard | Power BI | Optional | Display summary KPIs for judges/stakeholders |
| Secrets | Azure Key Vault | Optional | Store secrets if the project expands beyond Container App secrets |
| AI explanation | Azure OpenAI | Optional | Explain mobility/accessibility results in plain English |

## 1. Why this project should be built first

The most practical first project is a **Mobility Intelligence Dashboard** because it can use real public Riyadh data and does not require hardware, cameras, private APIs, or advanced ML. It can start with RCRC metro and bus datasets, then add simulated live delay events to demonstrate how a smart-city stack works.

This project directly supports two hackathon tracks:

1. **Transformational Technology**: mobility dashboard, congestion proxy, transit layers, simulated route delay events, command center view.
2. **Prosperous People**: 15-minute city thinking, district access scoring, walkability/accessibility proxy, service gap analysis.

The project should also be reusable as a template for later tracks. The same architecture can later support environmental dashboards, waste operations, cultural visitor routing, and district digital twins.

## 2. Outcome to build

Build a working web app that lets users:

1. View Riyadh on an Azure Maps dashboard.
2. Toggle metro lines and bus routes.
3. Select a sample district or point of interest.
4. See a simple transit accessibility score.
5. See a basic route/district KPI panel.
6. Load data from sample files locally.
7. Load cloud-hosted data from Azure Blob Storage after deployment.
8. Store processed route and district summaries in Cosmos DB.
9. Optionally simulate live route delay events and show them on the map.
10. Deploy everything into one Azure resource group using `azd up`.

## 3. Project positioning

This is not a production transportation model. It is a hackathon starter kit.

The goal is to teach students how an urban intelligence app is assembled:

```text
Riyadh open data
  → ingestion script
  → raw files in Blob Storage
  → cleaned GeoJSON / JSON
  → processed summaries in Cosmos DB
  → API layer
  → Azure Maps dashboard
  → optional live event simulation
  → optional Power BI / AI explanation layer
```

Students should be able to explain the project in plain English:

> “We built a simple mobility intelligence dashboard for Riyadh. It loads public metro and bus data, stores it in Azure, displays it on Azure Maps, calculates simple district accessibility scores, and can simulate live mobility events such as route delays or congestion alerts.”

## 4. Source anchors

### Hackathon and program anchors

The Riyadh Urban Intelligence Lab proposal positions the hackathon around Microsoft Azure, smart-city MVPs, mobility, air quality, walkability, district service delivery, and pilot-ready solutions. The Transformational Technology track includes mobility dashboards, congestion forecasting, parking prediction, isochrone mapping, and command-center-style outputs. The Prosperous People track includes district intelligence, 15-minute city analytics, walkability scoring, and district digital twins.

### atomcamp Arabia positioning anchor

atomcamp Arabia already positions AI for City Management around urban data dashboards, traffic analysis, congestion prediction, monitoring public safety, waste management optimization, flood mapping, and generative AI tools for urban planners. This repo should become a practical training/demo asset that supports that positioning.

## 5. External resources the agent should review

The agent must review these sources before building. Do not blindly clone and paste. Extract only the minimal useful patterns.

| Resource | URL | Use |
|---|---|---|
| Azure Maps Code Samples | https://github.com/Azure-Samples/AzureMapsCodeSamples | Map patterns, GeoJSON layers, popups, controls |
| Azure Container Apps overview | https://learn.microsoft.com/en-us/azure/container-apps/overview | Hosting model for API/web container |
| Azure Blob Storage overview | https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction | Raw/processed data storage |
| Azure Cosmos DB overview | https://learn.microsoft.com/en-us/azure/cosmos-db/overview | App state, route summaries, district scores |
| Azure Event Hubs overview | https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about | Optional simulated live events |
| Azure Stream Analytics overview | https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-introduction | Optional stream aggregation |
| Azure Developer CLI | https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview | `azd up` deployment |
| Azure Bicep | https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview | Infrastructure-as-code |

## 6. Riyadh data sources

The app should use real Riyadh open data where available, but must work with bundled sample data even if public endpoints fail.

| Dataset | URL | Use | Mode |
|---|---|---|---|
| Metro Lines in Riyadh | https://opendata.rcrc.gov.sa/explore/dataset/metro-lines-in-riyadh-2024/information/ | Metro route geometry and metadata | Real + sample fallback |
| Bus Roads by Direction in Riyadh | https://opendata.rcrc.gov.sa/explore/dataset/bus-roads-by-direction-in-riyadh-2024/information/ | Bus route geometry and metadata | Real + sample fallback |
| Riyadh Municipality realtime data page | https://www.alriyadh.gov.sa/en/realtime-data | Discovery anchor for AQI, parking, cleaning, interactive map | Extension only |

### Expected RCRC API pattern

RCRC appears to use an Opendatasoft-style API. The agent should test these patterns and adjust if the schema differs:

```text
https://opendata.rcrc.gov.sa/api/explore/v2.1/catalog/datasets/metro-lines-in-riyadh-2024/records?limit=100
https://opendata.rcrc.gov.sa/api/explore/v2.1/catalog/datasets/bus-roads-by-direction-in-riyadh-2024/records?limit=100
```

The app must not depend on these endpoints at runtime. Fetch scripts should download and normalize data ahead of time. The deployed app should read from Blob Storage and/or Cosmos DB.

## 7. Repo name and structure

Create a brand-new repo.

```text
riyadh-mobility-intelligence-dashboard/
├── README.md
├── STUDENT_QUICKSTART.md
├── INSTRUCTOR_NOTES.md
├── AGENT_BUILD_NOTES.md
├── .env.example
├── azure.yaml
├── package.json
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routes.py
│   ├── azure_clients.py
│   ├── scoring.py
│   ├── data_access.py
│   └── static/
│       ├── index.html
│       ├── src/
│       │   ├── main.js
│       │   ├── map.js
│       │   ├── api.js
│       │   ├── layers.js
│       │   ├── scoringPanel.js
│       │   └── styles.css
│       └── sample-data/
│           ├── riyadh_metro_lines_sample.geojson
│           ├── riyadh_bus_routes_sample.geojson
│           ├── district_centers_sample.geojson
│           └── mock_live_events_sample.json
├── scripts/
│   ├── fetch_rcrc_data.py
│   ├── normalize_to_geojson.py
│   ├── upload_to_blob.py
│   ├── seed_cosmos.py
│   ├── generate_mock_events.py
│   └── validate_data.py
├── infra/
│   ├── main.bicep
│   ├── main.parameters.json
│   ├── modules/
│   │   ├── container-app.bicep
│   │   ├── storage.bicep
│   │   ├── cosmos.bicep
│   │   ├── maps.bicep
│   │   ├── monitoring.bicep
│   │   └── optional-eventhubs.bicep
│   └── outputs.md
├── streaming/
│   ├── event_schema.md
│   ├── stream_analytics_query.sql
│   └── eventhub_simulator_notes.md
├── docs/
│   ├── architecture.md
│   ├── data_sources.md
│   ├── local_setup.md
│   ├── azure_deployment.md
│   ├── troubleshooting.md
│   ├── extension_ideas.md
│   └── judging_demo_script.md
└── tests/
    ├── test_scoring.py
    ├── test_data_shapes.py
    └── test_api_health.py
```

## 8. Technology choices

Keep the app simple.

| Component | Recommended choice | Why |
|---|---|---|
| Backend | FastAPI | Beginner-readable, easy API, Python-friendly |
| Frontend | Vanilla JS + Azure Maps Web SDK | Avoid React complexity for v1 |
| Hosting | Azure Container Apps | One deployable container for backend + static frontend |
| Data files | GeoJSON + JSON | Easy to inspect and map |
| Raw storage | Azure Blob Storage | Simple file landing zone |
| App state | Cosmos DB for NoSQL | Route summaries, district scores, latest events |
| Infra | Bicep + Azure Developer CLI | Reproducible deployment |
| Local dev | Docker Compose optional | Easy local smoke test |

Avoid React unless the agent has a strong reason. Avoid AKS entirely.

## 9. Infrastructure architecture

### Local mode

Local mode must work without Azure, except for Azure Maps if the user wants real map tiles.

```text
Local browser
  → FastAPI app on localhost
  → static frontend files
  → bundled sample GeoJSON
  → local scoring logic/API
```

In local mode, the app should work with sample GeoJSON and show a clear message if no Azure Maps key is present.

### Cloud MVP mode

Cloud MVP mode is mandatory.

```text
Azure Resource Group
  ├── Azure Container Apps
  │     └── runs FastAPI + static frontend
  ├── Azure Maps account
  │     └── map rendering / geospatial UI
  ├── Azure Storage Account
  │     ├── raw-data container
  │     └── processed-data container
  ├── Azure Cosmos DB for NoSQL
  │     ├── routes container
  │     ├── districts container
  │     └── events container
  └── Log Analytics / Application Insights
        └── app logs, request telemetry, error tracking
```

### Optional streaming mode

Streaming mode is a stretch goal. It should be included in the spec and repo folders, but not required for the first smoke test.

```text
Mock event generator
  → Azure Event Hubs
  → Azure Stream Analytics
  → Cosmos DB events container
  → API /live-events
  → Azure Maps live overlay
```

## 10. Azure resources to provision

### Required resources

| Resource | Suggested name pattern | Required config |
|---|---|---|
| Resource group | `rg-riyadh-mobility-${env}` | Single deployment target |
| Container App Environment | `cae-riyadh-mobility-${env}` | Log Analytics connected |
| Container App | `ca-riyadh-mobility-api-${env}` | External ingress enabled |
| Azure Maps Account | `maps-riyadh-mobility-${env}` | Standard Gen2 if available |
| Storage Account | `striyadhmobility${unique}` | Standard LRS |
| Blob container | `raw-data` | Private |
| Blob container | `processed-data` | Private or read-only via API |
| Cosmos DB Account | `cosmos-riyadh-mobility-${env}` | NoSQL, serverless preferred |
| Cosmos DB database | `mobilitydb` | Required |
| Cosmos container | `routes` | partition key `/type` or `/source` |
| Cosmos container | `districts` | partition key `/districtId` |
| Cosmos container | `events` | partition key `/routeId` or `/districtId` |
| Log Analytics Workspace | `log-riyadh-mobility-${env}` | Required |
| Application Insights | `appi-riyadh-mobility-${env}` | Required |

### Optional resources

| Resource | Suggested name pattern | Purpose |
|---|---|---|
| Event Hubs Namespace | `evhns-riyadh-mobility-${env}` | Streaming extension |
| Event Hub | `mobility-events` | Mock delay/congestion messages |
| Stream Analytics Job | `asa-riyadh-mobility-${env}` | Aggregate events |
| Power BI assets | `/powerbi` folder only | Manual import/export |
| Key Vault | `kv-riyadh-mobility-${env}` | Future secret management |

## 11. Data model

### Route document in Cosmos DB

```json
{
  "id": "metro-blue-line",
  "type": "metro",
  "source": "rcrc",
  "name": "Blue Line",
  "mode": "metro",
  "lineColor": "blue",
  "featureCount": 1,
  "geometryBlobPath": "processed-data/metro_lines.geojson",
  "lastUpdatedUtc": "2026-05-24T00:00:00Z"
}
```

### District document in Cosmos DB

```json
{
  "id": "district-central-riyadh",
  "districtId": "central-riyadh",
  "name": "Central Riyadh",
  "center": {
    "lat": 24.7136,
    "lon": 46.6753
  },
  "nearbyMetroCount": 2,
  "nearbyBusCount": 6,
  "accessibilityScore": 12,
  "accessibilityRating": "High",
  "lastCalculatedUtc": "2026-05-24T00:00:00Z"
}
```

### Mock live event document in Cosmos DB

```json
{
  "id": "event-20260524-0001",
  "routeId": "bus-route-12",
  "districtId": "central-riyadh",
  "eventType": "delay",
  "severity": "medium",
  "delayMinutes": 8,
  "lat": 24.7136,
  "lon": 46.6753,
  "timestampUtc": "2026-05-24T12:00:00Z",
  "source": "simulator"
}
```

## 12. API contract

The FastAPI app must expose these endpoints.

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Basic health check |
| `/api/config` | GET | Safe frontend config, no secrets |
| `/api/routes` | GET | Route summaries from Cosmos DB or sample fallback |
| `/api/routes/geojson?mode=metro` | GET | Metro GeoJSON |
| `/api/routes/geojson?mode=bus` | GET | Bus GeoJSON |
| `/api/districts` | GET | District center points and scores |
| `/api/score?districtId=...` | GET | Accessibility score for a district |
| `/api/live-events` | GET | Latest simulated mobility events |
| `/api/data-status` | GET | Shows source mode: sample/blob/cosmos/live |

### API behavior rules

1. Every endpoint must fail gracefully.
2. If Cosmos DB is unavailable, fallback to local sample files.
3. If Blob Storage is unavailable, fallback to local sample files.
4. The app should never crash because a public data source changed schema.
5. `/health` must return `200` if the app process is alive.
6. `/api/data-status` must clearly tell the user what mode is active.

## 13. Frontend requirements

The frontend must be simple and student-readable.

### Required UI sections

| UI section | Required behavior |
|---|---|
| Header | Project name and data status badge |
| Map | Azure Maps centered on Riyadh |
| Layer controls | Metro on/off, bus on/off, live events on/off |
| District selector | Dropdown of sample district centers |
| KPI cards | Metro routes, bus routes, selected district, score |
| Explanation panel | Plain-English explanation of selected district score |
| Debug panel | Shows whether data came from sample files, Blob, or Cosmos |

### Required map layers

| Layer | Source | Style |
|---|---|---|
| Metro lines | GeoJSON | Thick line |
| Bus routes | GeoJSON | Thin line |
| District centers | GeoJSON | Circle markers |
| Live events | Cosmos/sample JSON | Warning markers |
| Access buffer | Client-side generated circle | Semi-transparent polygon |

### Map behavior

1. App loads centered on Riyadh.
2. Metro and bus layers load automatically.
3. User can toggle layers.
4. User can click a route and see a popup.
5. User can select a district and zoom to it.
6. User can see a simple 1.5 km access buffer around the selected district.
7. User can see score explanation.

## 14. Scoring logic

Keep scoring intentionally simple.

### Required scoring formula

```text
score = (nearbyMetroCount * 3) + (nearbyBusCount * 1) - liveDelayPenalty
```

Rating:

```text
0–2   = Low
3–6   = Medium
7+    = High
```

Delay penalty:

```text
liveDelayPenalty = number of medium/high delay events within 1.5 km
```

If live events are not enabled, set penalty to `0`.

### Required scoring disclaimer

The UI must include this note:

> This score is a hackathon-friendly proxy. It is not a formal transport-planning model. It is designed to show how public mobility data, cloud storage, and simple analytics can support district-level planning conversations.

## 15. Data pipeline requirements

### Local sample pipeline

```text
app/static/sample-data/*.geojson
  → FastAPI reads files
  → frontend renders map
  → scoring runs locally or via API
```

### Cloud data pipeline

```text
scripts/fetch_rcrc_data.py
  → downloads raw API JSON
  → saves to local data/raw
  → uploads raw files to Azure Blob Storage /raw-data
  → normalize_to_geojson.py creates GeoJSON
  → uploads processed files to Blob Storage /processed-data
  → seed_cosmos.py writes route and district summaries to Cosmos DB
```

### Optional streaming pipeline

```text
scripts/generate_mock_events.py
  → sends delay/congestion events to Event Hubs
  → Stream Analytics aggregates by route/district
  → outputs latest events to Cosmos DB
  → frontend fetches /api/live-events
```

## 16. Scripts specification

### `scripts/fetch_rcrc_data.py`

Must:

1. Fetch metro dataset.
2. Fetch bus dataset.
3. Save raw responses into `data/raw`.
4. Write clear logs.
5. Fail gracefully.
6. Never block the app from running.

### `scripts/normalize_to_geojson.py`

Must:

1. Read raw downloaded JSON.
2. Detect geometry fields.
3. Convert records to valid GeoJSON FeatureCollections.
4. Save outputs into `app/static/sample-data` and `data/processed`.
5. Validate that each output has `type: FeatureCollection`.

### `scripts/upload_to_blob.py`

Must:

1. Upload raw files into `raw-data` container.
2. Upload processed GeoJSON into `processed-data` container.
3. Use Azure identity or connection string from environment.
4. Print uploaded blob paths.

### `scripts/seed_cosmos.py`

Must:

1. Read processed route and district files.
2. Create route summary documents.
3. Create sample district documents.
4. Upsert documents into Cosmos DB.
5. Be idempotent.

### `scripts/generate_mock_events.py`

Must:

1. Generate delay/congestion events.
2. Write sample events to local JSON.
3. If Event Hubs env vars exist, send events to Event Hubs.
4. If not, run in local-only mode.

### `scripts/validate_data.py`

Must:

1. Validate GeoJSON files.
2. Validate required properties.
3. Validate district sample file.
4. Exit with non-zero status on serious schema failure.

## 17. Infrastructure-as-code requirements

Use Bicep and Azure Developer CLI.

### `azure.yaml`

Must define:

```yaml
name: riyadh-mobility-intelligence-dashboard
metadata:
  template: riyadh-mobility-intelligence-dashboard@0.1.0
services:
  web:
    project: .
    language: py
    host: containerapp
infra:
  provider: bicep
  path: infra
```

### Bicep requirements

`infra/main.bicep` must deploy:

1. Container Apps Environment.
2. Container App.
3. Storage Account.
4. Blob containers: `raw-data`, `processed-data`.
5. Cosmos DB account, database, and containers.
6. Azure Maps account.
7. Log Analytics workspace.
8. Application Insights.
9. Managed identity for the Container App where practical.
10. Role assignments where practical.

### Outputs

The deployment must output:

```text
WEB_APP_URL
AZURE_MAPS_ACCOUNT_NAME
STORAGE_ACCOUNT_NAME
COSMOS_DATABASE_NAME
RESOURCE_GROUP_NAME
```

## 18. Environment variables

Create `.env.example`:

```bash
# Local app mode
APP_ENV=local
DATA_MODE=sample

# Azure Maps
AZURE_MAPS_KEY=replace_me

# Blob Storage
AZURE_STORAGE_ACCOUNT_NAME=replace_me
AZURE_STORAGE_CONTAINER_RAW=raw-data
AZURE_STORAGE_CONTAINER_PROCESSED=processed-data
AZURE_STORAGE_CONNECTION_STRING=replace_me_optional

# Cosmos DB
COSMOS_ENDPOINT=replace_me
COSMOS_KEY=replace_me_optional
COSMOS_DATABASE=mobilitydb
COSMOS_ROUTES_CONTAINER=routes
COSMOS_DISTRICTS_CONTAINER=districts
COSMOS_EVENTS_CONTAINER=events

# Optional Event Hubs
EVENT_HUB_CONNECTION_STRING=replace_me_optional
EVENT_HUB_NAME=mobility-events

# Optional Azure OpenAI
AZURE_OPENAI_ENDPOINT=replace_me_optional
AZURE_OPENAI_API_KEY=replace_me_optional
AZURE_OPENAI_DEPLOYMENT=replace_me_optional
```

The app should support local sample mode even if most values are blank.

## 19. README requirements

The README must be short and deployment-oriented. It should be the “I want to test it today” document.

### Required README outline

```text
# Riyadh Mobility Intelligence Dashboard

## What this is
## Architecture in 60 seconds
## Prerequisites
## Run locally in 5 minutes
## Deploy to Azure with azd
## Load real/sampled Riyadh data
## What Azure services are used
## Troubleshooting
## Extension ideas
```

### README quick start

Must include:

```bash
git clone <repo-url>
cd riyadh-mobility-intelligence-dashboard
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Then:

```text
Open http://127.0.0.1:8000
```

### Azure deploy quick start

Must include:

```bash
az login
azd auth login
azd init
azd up
```

Then include:

```text
After deployment, copy the WEB_APP_URL from azd output and open it in your browser.
```

## 20. Student-facing explanation requirements

Even though this spec focuses on the agent build, the repo should include a beginner-facing `STUDENT_QUICKSTART.md`.

It must explain:

1. What a mobility dashboard is.
2. What Azure Maps does.
3. What Blob Storage does.
4. What Cosmos DB does.
5. Why simulated live events are acceptable.
6. How to run the app locally.
7. How to modify one sample district.
8. How to add a new route layer.
9. How to explain the project to judges.

Use simple language. Avoid enterprise jargon.

## 21. Instructor notes requirements

`INSTRUCTOR_NOTES.md` must include:

1. 20-minute demo flow.
2. 60-minute guided build option.
3. Common student errors.
4. How to switch between sample and cloud modes.
5. How to explain each Azure service.
6. Suggested stretch tasks for advanced students.
7. Judging rubric.

## 22. Testing requirements

The repo must include basic tests.

| Test | Purpose |
|---|---|
| `test_api_health.py` | `/health` returns 200 |
| `test_data_shapes.py` | sample GeoJSON files are valid FeatureCollections |
| `test_scoring.py` | scoring produces Low/Medium/High correctly |

Also include a manual smoke test checklist:

```text
[ ] App starts locally
[ ] Map loads
[ ] Metro layer appears
[ ] Bus layer appears
[ ] District selector works
[ ] Score panel updates
[ ] /health returns 200
[ ] Docker build succeeds
[ ] azd deployment completes
[ ] Deployed app loads
```

## 23. Agent build phases

### Phase 0 — Confirm scope

Before coding, the agent must restate:

1. New repo name.
2. Required Azure services.
3. Local/sample fallback requirement.
4. No Kubernetes.
5. No production ML.

### Phase 1 — Research and extraction

Agent tasks:

1. Review Azure Maps Code Samples.
2. Identify minimal examples for GeoJSON line layers, symbols, popups, and controls.
3. Review Azure Container Apps deployment pattern.
4. Review Blob and Cosmos SDK usage in Python.
5. Do not copy unnecessary sample infrastructure.

Deliverable:

```text
AGENT_BUILD_NOTES.md
```

Include:

- Which sources were reviewed.
- Which patterns were reused.
- What was intentionally not included.

### Phase 2 — Local app scaffold

Agent tasks:

1. Create FastAPI app.
2. Serve static frontend from `/`.
3. Add `/health` endpoint.
4. Add sample GeoJSON files.
5. Add frontend map shell.
6. Add `.env.example`.
7. Add `requirements.txt`.

Acceptance:

```bash
uvicorn app.main:app --reload
```

Then browser opens locally.

### Phase 3 — Map and dashboard

Agent tasks:

1. Initialize Azure Maps.
2. Load metro GeoJSON.
3. Load bus GeoJSON.
4. Load district centers.
5. Add layer toggles.
6. Add simple score panel.
7. Add popups.
8. Add data status badge.

Acceptance:

- Map shows Riyadh.
- Metro and bus layers are visible.
- District selector updates the score.

### Phase 4 — Data API and scoring

Agent tasks:

1. Add `/api/routes`.
2. Add `/api/routes/geojson`.
3. Add `/api/districts`.
4. Add `/api/score`.
5. Add `/api/live-events`.
6. Implement fallback data logic.
7. Implement score logic.

Acceptance:

- API works with local sample files.
- App does not require Cosmos DB locally.

### Phase 5 — Azure Blob Storage integration

Agent tasks:

1. Add Blob client utility.
2. Add script to upload sample/processed files.
3. Add app setting `DATA_MODE=blob`.
4. Allow API to read processed GeoJSON from Blob.
5. Fall back to local files if Blob fails.

Acceptance:

- `DATA_MODE=sample` works.
- `DATA_MODE=blob` works when env vars are configured.
- Failure message is clear.

### Phase 6 — Cosmos DB integration

Agent tasks:

1. Add Cosmos client utility.
2. Add route summary model.
3. Add district score model.
4. Add events model.
5. Add `seed_cosmos.py`.
6. Make API use Cosmos when configured.
7. Fall back to sample data if Cosmos fails.

Acceptance:

- `/api/routes` can return route summaries from Cosmos.
- `/api/districts` can return district scores from Cosmos.
- Local mode still works without Cosmos.

### Phase 7 — Containerization

Agent tasks:

1. Write Dockerfile.
2. Ensure static files are served.
3. Expose correct port.
4. Add health check note.
5. Add docker-compose for local smoke test.

Acceptance:

```bash
docker build -t riyadh-mobility-dashboard .
docker run -p 8000:8000 riyadh-mobility-dashboard
```

Then browser opens locally.

### Phase 8 — Azure deployment

Agent tasks:

1. Create `azure.yaml`.
2. Create Bicep infra.
3. Deploy Container App.
4. Deploy Storage.
5. Deploy Cosmos DB.
6. Deploy Azure Maps.
7. Deploy Log Analytics/Application Insights.
8. Set Container App environment variables.
9. Output web URL.

Acceptance:

```bash
azd up
```

Deploys to one resource group.

### Phase 9 — Optional streaming module

Agent tasks:

1. Add Event Hub Bicep module.
2. Add `generate_mock_events.py`.
3. Add event schema docs.
4. Add Stream Analytics query file.
5. Add manual instructions for enabling streaming.

Acceptance:

- Local event simulation works without Azure.
- Event Hubs integration works only when configured.
- Main app does not depend on streaming.

### Phase 10 — Documentation pass

Agent tasks:

1. Write README.
2. Write student quickstart.
3. Write instructor notes.
4. Write architecture doc.
5. Write deployment doc.
6. Write troubleshooting doc.
7. Write judging demo script.

Acceptance:

A beginner can follow README to run locally. A technical operator can follow deployment docs to run `azd up`.

## 24. MVP acceptance criteria

The project is acceptable when:

1. The repo can be cloned and run locally.
2. The app works with bundled sample data.
3. The map loads and displays Riyadh.
4. Metro and bus layers can be toggled.
5. A district can be selected.
6. An accessibility score is displayed.
7. The API exposes health, routes, districts, scores, and live events endpoints.
8. Docker build works.
9. `azd up` deploys the app and required resources.
10. Blob Storage and Cosmos DB are provisioned.
11. The app can run even if Blob/Cosmos integration fails.
12. Documentation explains every Azure service used.

## 25. Explicit non-goals for v1

Do not build these in v1:

- AKS or Kubernetes.
- User login/authentication.
- Real CCTV ingestion.
- Real-time production traffic feeds.
- Full routing engine.
- True walkability model.
- Real isochrone calculation.
- Azure Digital Twins as mandatory scope.
- Azure ML as mandatory scope.
- Complex front-end framework unless needed.
- Multi-tenant architecture.
- Enterprise security architecture.

## 26. Stretch goals

Only after the MVP is deployed:

| Stretch | Description |
|---|---|
| Event Hubs | Stream mock route delay events |
| Stream Analytics | Aggregate live events by district |
| Power BI | Build executive dashboard |
| Azure OpenAI | Explain scores and suggest interventions |
| Digital Twins | Model districts/routes/stations as a graph |
| AQI overlay | Add Riyadh AQI or environmental layer |
| Parking overlay | Add Riyadh parking availability if accessible |
| True isochrones | Use proper routing/service-area logic |

## 27. Suggested judging demo script

Use this script for a two-minute demo.

```text
This is the Riyadh Mobility Intelligence Dashboard.

It uses public Riyadh metro and bus data to create a simple city mobility view. The app is deployed on Azure Container Apps, stores raw and processed data in Azure Blob Storage, stores route and district summaries in Cosmos DB, and displays everything through Azure Maps.

The dashboard allows us to toggle metro and bus layers, select a district, and calculate a simple accessibility score. This score is not a formal transport model, but it helps identify areas with stronger or weaker transit access.

The architecture is designed for extension. We can add simulated live congestion events through Event Hubs, process those events with Stream Analytics, and display them as alerts on the map. We can also extend this into parking prediction, pollution overlays, or 15-minute-city analysis.
```

## 28. Copy/paste prompt for the AI agent harness

```text
You are building a new Azure-ready hackathon starter repo called `riyadh-mobility-intelligence-dashboard`.

Goal:
Create a beginner-friendly but deployable smart-city MVP for the Riyadh Urban Intelligence Lab. The app must visualize Riyadh metro and bus data, calculate simple district accessibility scores, and deploy to Azure using Azure Container Apps, Azure Maps, Azure Blob Storage, Cosmos DB, and Application Insights. Event Hubs and Stream Analytics should be included only as optional stretch modules.

Hard constraints:
- Build a brand-new repo from scratch.
- Do not use Kubernetes or AKS.
- Do not require real CCTV, hardware, IoT devices, or private APIs.
- The app must run locally with bundled sample GeoJSON data.
- The app must deploy with `azd up` into one Azure resource group.
- The app must use Azure Blob Storage and Cosmos DB in cloud mode.
- The app must fall back gracefully if Blob Storage or Cosmos DB is unavailable.
- Keep the app beginner-friendly and heavily documented.

Required stack:
- FastAPI backend
- Vanilla JavaScript frontend
- Azure Maps Web SDK
- Azure Container Apps
- Azure Blob Storage
- Azure Cosmos DB for NoSQL
- Application Insights / Log Analytics
- Bicep + Azure Developer CLI

Data:
Use bundled sample GeoJSON by default. Add scripts that attempt to fetch and normalize real Riyadh data from:
- https://opendata.rcrc.gov.sa/explore/dataset/metro-lines-in-riyadh-2024/information/
- https://opendata.rcrc.gov.sa/explore/dataset/bus-roads-by-direction-in-riyadh-2024/information/

Build phases:
1. Create local FastAPI + static frontend app.
2. Add sample Riyadh metro, bus, and district GeoJSON files.
3. Build Azure Maps UI with layer toggles, popups, and district selector.
4. Add accessibility scoring logic.
5. Add API endpoints: /health, /api/routes, /api/routes/geojson, /api/districts, /api/score, /api/live-events, /api/data-status.
6. Add Blob Storage integration and upload scripts.
7. Add Cosmos DB integration and seed scripts.
8. Add Dockerfile.
9. Add azure.yaml and Bicep infrastructure.
10. Add optional Event Hubs and Stream Analytics files as stretch modules.
11. Write README.md, STUDENT_QUICKSTART.md, INSTRUCTOR_NOTES.md, and docs.
12. Add basic tests.

Acceptance criteria:
- `uvicorn app.main:app --reload` works locally.
- `docker build` and `docker run` work.
- `azd up` deploys required Azure services.
- App shows Riyadh map, metro layer, bus layer, district selector, and score panel.
- App works in sample mode without cloud dependencies.
- Documentation explains every Azure service used.
```

## 29. Final implementation guidance

Build the boring version first.

The winning v1 is not the most sophisticated version. The winning v1 is the one that deploys reliably, explains the Azure stack clearly, and gives students something they can modify in a few hours.

Recommended build order:

1. Local app with sample files.
2. Azure Maps rendering.
3. Scoring panel.
4. Docker container.
5. Azure Container Apps deployment.
6. Blob Storage integration.
7. Cosmos DB integration.
8. Event simulation.
9. Stream Analytics stretch.
10. Power BI / AI extensions later.

If anything breaks, preserve the local sample mode. The hackathon experience depends on the app being runnable even when cloud setup fails.

## 30. /autoplan Review Addendum

### Review context

- Restore point: `/Users/EVA/.gstack/projects/riyadh_ud/main-autoplan-restore-20260528-104919.md`
- Review mode: `HOLD SCOPE`
- Premise confirmed by user: treat this as a **deployable reference app** for hackathon students, not only a teaching scaffold
- UI scope detected: yes
- DX scope detected: yes
- Design doc on branch: none

### Phase 1 — CEO review

#### Premise challenge

The core problem is valid: a Riyadh mobility dashboard is a better first repo than cameras, traffic ML, or private APIs because it can demonstrate a real Azure stack with public data and sample fallbacks.

The main strategic risk is not the idea but the packaging. The current spec mixes three products:

1. A student starter template
2. A deployable Azure reference application
3. A stretch-ready smart-city platform shell

That is survivable only if v1 is staged aggressively. Since the user explicitly chose "deployable reference app," the reviewed plan should still keep sample-mode success as the first success path, but Blob, Cosmos, Container Apps, Maps, and `azd up` remain true v1 deliverables.

#### What already exists

- Existing implementation: none; this repo is effectively a spec-only seed
- Existing leverage inside the spec:
  - clear mandatory Azure service list
  - clear local fallback rule
  - clear backend/frontend stack choice
  - clear phase order that already puts local mode before cloud integrations

#### Dream state delta

```text
CURRENT STATE                  THIS PLAN                          12-MONTH IDEAL
spec-only repo        --->     deployable reference MVP   --->   reusable smart-city template family
                               with sample fallback              with optional streaming, extra overlays,
                               and real Azure path              and track-specific extensions
```

#### Implementation alternatives

**Approach A: teaching-first starter kit**
- Summary: fully optimize for local success, with Azure mostly scaffolded after the core UI and API work
- Effort: M
- Risk: Low
- Pros: fastest student success, lowest setup friction, easiest to teach
- Cons: weaker proof that the cloud architecture is genuinely operational
- Reuses: almost all current spec structure

**Approach B: staged deployable reference app**
- Summary: keep local-first sequencing, but require working Blob, Cosmos, Maps, Container Apps, and `azd up` in v1
- Effort: L
- Risk: Medium
- Pros: matches the user's premise choice, preserves credibility, still allows sample fallback
- Cons: higher implementation and docs burden; more failure modes across local and cloud paths
- Reuses: current mandatory Azure stack and existing phase ordering

**Approach C: judge-demo shell**
- Summary: optimize for demo smoothness and visual impact first, with infra depth partly implied rather than proven
- Effort: M
- Risk: Medium
- Pros: strong first impression in a short demo
- Cons: poor fit for a reference repo; students inherit more hidden debt
- Reuses: UI-heavy portions of the current spec

**Reviewed recommendation:** Approach B. The user selected the more deployable interpretation, so the plan should harden that path rather than quietly downgrade to a pure teaching template.

#### Scope decisions

- Keep in v1:
  - FastAPI + vanilla JS + Azure Maps
  - sample-data local mode
  - Blob-backed processed data path
  - Cosmos-backed summaries path
  - Docker build
  - `azd` + Bicep deployment of required services
- Reframe inside v1:
  - Event Hubs and Stream Analytics stay present in repo structure but as non-blocking stretch scaffolds
  - docs set should exist, but the first pass should prioritize runbook quality over volume
- Not in scope:
  - Power BI integration
  - Azure OpenAI explanation layer
  - Key Vault unless secrets handling actually expands
  - any additional track templates

#### Error & rescue registry

| Method/Codepath | What Can Go Wrong | Rescue Action | User Sees |
|---|---|---|---|
| `fetch_rcrc_data.py` | RCRC schema drift or endpoint failure | log clearly, save nothing, keep app runnable | data refresh failed, sample mode still works |
| Blob read path | storage auth or missing blob | fallback to local sample files | status badge shows `sample` |
| Cosmos read path | endpoint unavailable or container missing | fallback to sample route/district summaries | status badge shows `sample` or partial cloud mode |
| Azure Maps init | missing key | show clear no-key message and non-map fallback text | app loads, map area explains missing key |
| `azd up` | one Azure resource fails | document preflight and post-deploy checks | operator sees explicit deploy failure and rerun path |

#### Failure modes registry

| Codepath | Failure Mode | Rescued? | Test? | User Sees? | Logged? |
|---|---|---:|---:|---|---:|
| local app boot | missing cloud env vars | Y | Y | app still runs in sample mode | Y |
| blob ingestion | blob container missing | Y | N | processed data unavailable, sample fallback | Y |
| cosmos summary reads | container or auth failure | Y | N | sample summaries returned | Y |
| maps frontend | missing map key | Y | N | clear banner instead of broken map | Y |
| streaming stretch | event hub unset | Y | N | local-only mock events path | Y |

Critical gaps before implementation:
- explicit tests for Blob fallback behavior
- explicit tests for Cosmos fallback behavior
- explicit spec text for missing Azure Maps key UX

#### CEO findings by section

**Architecture:** Strong single-container MVP shape. Risk is repo sprawl, not topology. Keep one deployable container and do not split services in v1.

**Security:** No auth is fine for v1 only if the app is clearly demo/reference scope and write paths stay limited to ingestion scripts and operator workflows. The spec should keep frontend config secret-free and avoid exposing raw storage directly.

**Performance:** Good enough for a starter app. Avoid premature streaming or geo-computation complexity; preprocessed GeoJSON and simple district summaries are the correct move.

**Observability:** Application Insights is listed but the spec should require a minimal operator story: health endpoint, request/error logging, data mode status, and one post-deploy smoke checklist.

**Deployment:** The biggest implementation risk is pretending `azd up` is easy without specifying the smallest happy path. The reviewed plan should target one resource group, one container app, one storage account, one Cosmos database, and explicit output variables only.

**Long-term trajectory:** Strong if this becomes the "mobility" base template rather than a pseudo-platform. Weak if v1 tries to pre-bake too many future tracks.

### Phase 2 — Design review

#### Initial design read

Design completeness is roughly **7/10**. The spec already names the required UI regions, map behavior, and key interactions. The gaps are not styling but decision edges that usually get punted to implementation.

#### Design findings

- Information hierarchy is mostly right:
  - first: map + status
  - second: district selection + score
  - third: debug and explanatory context
- Missing states still need to be explicit:
  - loading state for map/data
  - empty state when district data is unavailable
  - partial-cloud state when some cloud services fail
  - no-map-key state
- Responsive behavior is underspecified. This matters because student demos may happen on laptops, but students often inspect on mobile too.
- Accessibility is mentioned only implicitly. Keyboard access, visible labels, sufficient contrast, and a usable district selector should be called out as acceptance requirements.

#### Required user flow

```text
Load app
  -> see status badge + map shell
  -> metro/bus layers load
  -> choose district
  -> map zooms + buffer appears
  -> score panel + explanation update
  -> optional live events overlay updates status
```

#### Design not in scope

- bespoke visual identity system
- advanced animation or cinematic control-room UI
- multi-screen command-center layout

### Phase 3 — Engineering review

#### Architecture diagram

```text
Browser
  -> FastAPI app
      -> static frontend
      -> sample file reader
      -> Blob reader (optional cloud path)
      -> Cosmos reader (optional cloud path)
      -> scoring module
  -> Azure Maps SDK

Scripts
  -> RCRC fetch
  -> normalize to GeoJSON
  -> Blob upload
  -> Cosmos seed

Infra
  -> azd
      -> Bicep
          -> Container Apps
          -> Storage
          -> Cosmos DB
          -> Azure Maps
          -> App Insights / Log Analytics
```

#### Engineering findings

- The spec should define a strict data-source precedence so implementers do not improvise. Recommended precedence:
  - summaries: Cosmos if configured and healthy, else local sample summaries
  - GeoJSON: Blob if configured and healthy, else local sample GeoJSON
  - live events: Cosmos latest events if configured, else local mock JSON
- The spec should treat "cloud partial failure" as a first-class state, not just a fallback implementation detail.
- The spec should avoid promising too much dynamic fetching from public sources. Runtime dependence on RCRC should remain forbidden.
- The repo structure is fine, but the first build should not block on all docs and stretch files being perfect. Implementation order matters more than directory completeness.

#### Test diagram

```text
Flow 1: app boot in sample mode
  -> test health endpoint
  -> test data-status returns sample
  -> manual check local page loads

Flow 2: district selection and score update
  -> test scoring formula
  -> test district payload shape
  -> manual UI smoke for score panel update

Flow 3: cloud fallback behavior
  -> test blob failure falls back to sample GeoJSON
  -> test cosmos failure falls back to sample summaries
  -> test no Azure Maps key shows clear UX state

Flow 4: deployment path
  -> test Docker build
  -> test `azd up` happy path
  -> manual deployed smoke test
```

#### Eng not in scope

- distributed background processing
- real-time event pipelines as a required path
- complicated caching layers
- any second service or worker in v1

### Phase 3.5 — DX review

#### Target developer persona

```text
Who:       hackathon student or early-career builder using the repo as a base
Context:   cloning the repo to get a smart-city MVP running fast, then modifying it
Tolerance: 10-20 minutes to first visible success; much less patience for Azure errors
Expects:   copy-paste local setup, obvious cloud toggle points, simple folder layout
```

#### Developer empathy narrative

I clone the repo because I want something real, not another toy map. The first thing I need is visible proof that it works locally. If local mode needs five Azure services before I see anything, I’m gone. If local mode works but the cloud story is fake, I’ll feel tricked later when I try to deploy. The README has to tell me exactly what success looks like in sample mode, then exactly what changes when I switch to Blob and Cosmos. When something fails, I need the app and docs to tell me which layer failed: map key, Blob, Cosmos, or deploy. I can handle cloud complexity if it is staged and named clearly. I will not enjoy guessing.

#### DX findings

- The current spec is ambitious enough that DX quality is a ship blocker, not a nice-to-have.
- Time to hello world target should be split:
  - local sample mode: under 5 minutes
  - first Azure deploy: under 30-45 minutes with prerequisites already installed
- The repo should explicitly separate:
  - "run locally now"
  - "load real-ish data into Azure"
  - "deploy to Azure"
- Student docs and operator docs should not be merged into one voice. Keep them distinct.

#### DX scorecard

| Dimension | Score | Notes |
|---|---:|---|
| Getting Started | 7/10 | strong outline, but local-vs-cloud path needs sharper separation |
| API/CLI/SDK | 8/10 | endpoint set is clear and modest |
| Error Messages | 5/10 | cloud failure UX and doc language need stronger specificity |
| Documentation | 7/10 | good coverage target, but currently too broad for first landing |
| Upgrade Path | 5/10 | not relevant yet, but versioning/deployment evolution is unspecified |
| Dev Environment | 7/10 | simple stack helps; Azure prerequisites remain the main drag |
| Community/Teaching | 8/10 | student/instructor split is a strong choice |
| DX Measurement | 6/10 | smoke checklist exists, but no explicit local/cloud success metrics |

**Overall DX:** 6.6/10  
**TTHW target:** local < 5 min; Azure deploy < 45 min  
**Competitive rank:** Competitive for hackathon starter repos if fallback behavior and docs are polished

#### DX implementation checklist

- [ ] local sample mode visible in under 5 minutes
- [ ] README separates local run, cloud data load, and Azure deploy
- [ ] every cloud dependency failure maps to problem + cause + fix
- [ ] sample mode requires no Blob or Cosmos
- [ ] `azd up` path names required Azure prerequisites explicitly
- [ ] student docs explain what each Azure service does in plain language
- [ ] instructor notes explain common failure modes and mode switching

### Cross-phase themes

- **Staging discipline**: the plan is good if it lands as a staged reference app; it becomes bad if all repo ambitions are treated as day-one blockers.
- **Fallback clarity**: sample/blob/cosmos mode transitions are central product behavior, not just technical plumbing.
- **Docs as product surface**: for this repo, docs quality directly determines whether the technical architecture is usable.

### Implementation tasks

- [ ] **T1 (P1, human: ~3h / CC: ~20min)** — Spec tightening — add explicit data-source precedence and partial-cloud behavior notes
- [ ] **T2 (P1, human: ~2h / CC: ~15min)** — DX staging — split local, cloud-data, and Azure-deploy success paths in the implementation plan and docs
- [ ] **T3 (P1, human: ~2h / CC: ~15min)** — Failure UX — specify no-map-key, Blob-failure, and Cosmos-failure user-facing states
- [ ] **T4 (P2, human: ~90min / CC: ~10min)** — Testing scope — add fallback tests for Blob/Cosmos and manual smoke expectations for partial-cloud mode
- [ ] **T5 (P2, human: ~60min / CC: ~10min)** — Scope hygiene — keep Event Hubs and Stream Analytics as stretch scaffolds only

## 31. Decision Audit Trail

| # | Phase | Decision | Classification | Principle | Rationale | Rejected |
|---|---|---|---|---|---|---|
| 1 | Intake | Skip `/office-hours` prerequisite and review the spec directly | Mechanical | Bias toward action | The spec is already detailed enough to review usefully | running a separate ideation pass first |
| 2 | CEO | Treat this as a deployable reference app | User choice | User override | The user selected the more cloud-operational interpretation at the premise gate | teaching-first default |
| 3 | CEO | Use `HOLD SCOPE` review posture | Mechanical | Choose completeness | The spec is already broad; review should harden, not expand | selective expansion |
| 4 | CEO | Keep Blob + Cosmos as true v1 deliverables | Mechanical | Completeness | Removing them would break the user's confirmed premise | deferring cloud persistence to v1.5 |
| 5 | CEO | Keep streaming as stretch-only scaffolding | Mechanical | Explicit over clever | It preserves extension value without making v1 fragile | full streaming implementation in v1 |
| 6 | Design | Require explicit missing/partial states | Mechanical | Completeness | The UI otherwise looks specified but still leaves core behavior ambiguous | leaving states to implementation taste |
| 7 | Eng | Require source-precedence rules | Mechanical | Explicit over clever | Fallback behavior is core system behavior | letting the implementation infer precedence |
| 8 | DX | Split local success from Azure success | Mechanical | Pragmatic | Students need a short first win and a separate cloud path | one blended onboarding path |

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | `/autoplan` | Scope & strategy | 1 | issues_open | deployable-reference premise confirmed; scope staging and fallback clarity need tightening |
| Codex Review | `codex exec` | Independent 2nd opinion | 1 | issues_open | outside voice reinforced overscope risk and need to stage v1 hard |
| Eng Review | `/autoplan` | Architecture & tests (required) | 1 | issues_open | source precedence, fallback tests, and partial-cloud behavior need to be explicit |
| Design Review | `/autoplan` | UI/UX gaps | 1 | issues_open | loading/empty/error/partial states and responsive intent need to be specified |
| DX Review | `/autoplan` | Developer experience gaps | 1 | issues_open | local-vs-cloud onboarding split and clearer error guidance required |

- **CODEX:** independent review agreed the spec is viable, but only if v1 is treated as a staged reference app instead of a platform shell.
- **CROSS-MODEL:** highest overlap was on staging discipline, fallback clarity, and doc quality as core product behavior.
- **UNRESOLVED:** no blocking premise ambiguity remains, but several implementation-spec ambiguities still need acceptance.
- **VERDICT:** strategy is usable; implementation should proceed only from the reviewed addendum, not the raw spec alone.
