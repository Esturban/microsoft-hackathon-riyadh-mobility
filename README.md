# Riyadh Mobility Intelligence Dashboard

## What this is

A beginner-friendly smart-city MVP for Riyadh hackathons. It shows metro and bus layers on a map, calculates a simple district accessibility score, and demonstrates how Azure Maps, Blob Storage, Cosmos DB, and Container Apps fit together.

## Rebuild guide

A polished walkthrough for reconstructing the app step by step is available here:

- `docs/rebuild_guide.md`
- `docs/rebuild_guide.docx`

## Architecture in 60 seconds

`RCRC or sample files -> FastAPI -> API + static frontend -> Azure Maps dashboard -> optional Blob/Cosmos live data path`

The repo runs locally from bundled sample files, then upgrades cleanly to Azure-backed mode after deployment.

## Prerequisites

- Python 3.11+
- Docker Desktop for the container smoke test
- Azure CLI and Azure Developer CLI for deployment

## Run locally in 5 minutes

```bash
git clone <repo-url>
cd riyadh-mobility-intelligence-dashboard
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Deploy to Azure with azd

```bash
az login
azd auth login
azd init
bash scripts/deploy_azure.sh
```

After deployment, copy the `WEB_APP_URL` from `azd` output and open it in your browser.

To delete the current azd environment's resource group when you are done testing:

```bash
bash scripts/destroy_resource_group.sh --yes
```

## Load real/sampled Riyadh data

- Sample mode: keep `DATA_MODE=sample`
- Blob mode: run `python3 scripts/fetch_rcrc_data.py`, `python3 scripts/normalize_to_geojson.py`, and `python3 scripts/upload_to_blob.py`
- Cosmos mode: run `python3 scripts/seed_cosmos.py`

## What Azure services are used

- Azure Container Apps for hosting
- Azure Maps for rendering Riyadh layers
- Azure Blob Storage for raw and processed datasets
- Azure Cosmos DB for route, district, and event documents
- Log Analytics and Application Insights for monitoring

## Troubleshooting

- If no Azure Maps key is set, the app falls back to an OpenStreetMap view for local exploration
- Check `/api/data-status` to confirm whether you are in `sample`, `blob`, or `cosmos` mode
- Run `python3 scripts/validate_data.py` if edited sample files stop loading
- Container health checks should target `/health`

## Extension ideas

- Add Event Hubs and Stream Analytics for a stretch live-feed demo
- Add more districts or points of interest
- Add a Power BI summary for judges
