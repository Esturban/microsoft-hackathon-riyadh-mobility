# Riyadh Mobility Intelligence Dashboard

A beginner-friendly Riyadh hackathon starter kit for mapping metro and bus routes, selecting districts, and calculating a simple mobility access score.

The app is intentionally small: FastAPI backend, vanilla JavaScript frontend, bundled sample data, and an Azure-backed live path for teams that want to deploy.

## What You Build

This starter kit helps a team show:

- Riyadh metro and bus layers on a map
- district selection and a simple access score
- mock live mobility events such as delays or congestion
- a fallback-aware data path that works without cloud credentials
- an Azure deployment path using Container Apps, Azure Maps, Blob Storage, Cosmos DB, Application Insights, `azd`, and Bicep

For the full build guide, use:

- `docs/rebuild_guide.md`
- `docs/rebuild_guide.docx`

More supporting notes live in `docs/README.md`.

## Quick Start

Requirements:

- Python 3.11 or newer
- Git
- optional Docker Desktop for container testing
- optional Azure CLI and Azure Developer CLI for deployment

Run locally:

```bash
git clone https://github.com/Esturban/microsoft-hackathon-riyadh-mobility.git
cd microsoft-hackathon-riyadh-mobility
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## What To Check

After the app starts:

- the dashboard loads at `http://127.0.0.1:8000`
- metro and bus layers toggle on and off
- the district selector appears
- selecting a district updates the score panel
- `/health` returns `{"status":"ok"}`
- `/api/data-status` shows the active data mode

Run tests:

```bash
python -m pytest
python scripts/validate_data.py
```

## How The App Works

```text
sample or RCRC data
  -> FastAPI API
  -> vanilla JS dashboard
  -> map layers and score panel
  -> optional Azure-backed live layer
```

Core files:

| Area | Start here |
|---|---|
| API | `app/main.py`, `app/routes.py` |
| Data loading | `app/data_access.py` |
| Score formula | `app/scoring.py` |
| Frontend | `app/static/index.html`, `app/static/src/` |
| Sample data | `app/static/sample-data/` |
| Data scripts | `scripts/` |
| Azure infrastructure | `azure.yaml`, `infra/main.bicep` |
| Tests | `tests/` |

The local default is `DATA_MODE=sample`, which means the app uses bundled files and does not need Azure credentials.

## Data Modes

| Mode | Meaning |
|---|---|
| `sample` | always use bundled sample files |
| `blob` | prefer Azure Blob Storage, then fall back to sample files |
| `cosmos` | prefer Cosmos DB, then fall back to sample files |
| `auto` | try Cosmos, then Blob, then sample files |

Check the current mode:

```bash
curl -s http://127.0.0.1:8000/api/data-status | python -m json.tool
```

## Update The Data

The app works from sample data by default. To fetch and normalize fresh RCRC data:

```bash
python scripts/fetch_rcrc_data.py
python scripts/normalize_to_geojson.py
python scripts/validate_data.py
```

Optional cloud steps:

```bash
python scripts/upload_to_blob.py
PYTHONPATH=. python scripts/seed_cosmos.py
```

## Deploy To Azure

Sign in once:

```bash
az login
azd auth login
azd init
```

Deploy:

```bash
bash scripts/deploy_azure.sh
```

Open the `WEB_APP_URL` from the `azd` output.

Delete the current Azure resource group when finished:

```bash
bash scripts/destroy_resource_group.sh --yes
```

## Demo Script

Use this 5-minute flow:

1. Open the dashboard and explain that it is a Riyadh mobility starter kit.
2. Toggle metro and bus layers to show public transport coverage.
3. Select a district and explain the score formula.
4. Open `/api/data-status` to show fallback-aware data loading.
5. Describe the Azure-backed live layer: Container Apps, Azure Maps, Blob Storage, Cosmos DB, and Application Insights.
6. Explain how a team could adapt the same scaffold for mobility, district intelligence, sustainability, or culture use cases.

## Extension Ideas

Safe first changes:

- add more Riyadh districts or points of interest
- adjust the score weights in `app/scoring.py`
- add a parking, congestion, AQI, or heritage map layer
- add a `/demo` page for judge-facing presentations

Stretch changes:

- publish mock events to Event Hubs
- add Stream Analytics for live aggregation
- export summary data to Power BI

## Troubleshooting

If the map is blank, clear `AZURE_MAPS_KEY` in `.env` and reload. The app should fall back to OpenStreetMap for local work.

If cloud data is not loading, check `/api/data-status` first. Missing credentials should fall back to sample data instead of breaking the dashboard.

If sample files stop loading, run:

```bash
python scripts/validate_data.py
```

If the container fails, test locally first with `python -m pytest`, then run:

```bash
docker build -t riyadh-mobility-dash .
docker run --rm -p 8001:8000 riyadh-mobility-dash
```
