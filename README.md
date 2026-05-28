# Riyadh Mobility Intelligence Dashboard

Beginner-friendly smart-city MVP for Riyadh hackathons.

What it does:

- FastAPI backend with required MVP endpoints
- Vanilla JS frontend with Azure Maps support
- Sample GeoJSON/JSON fallback for local use
- Azure-ready Blob Storage, Cosmos DB, Container Apps, monitoring, and `azd` scaffolding

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000).

## Data flow

`RCRC data -> scripts -> Blob Storage -> Cosmos DB -> API -> Azure Maps dashboard`

## Required endpoints

- `/health`
- `/api/config`
- `/api/routes`
- `/api/routes/geojson?mode=metro`
- `/api/routes/geojson?mode=bus`
- `/api/districts`
- `/api/score?districtId=central-riyadh`
- `/api/live-events`
- `/api/data-status`
