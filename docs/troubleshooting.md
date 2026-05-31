# Troubleshooting

---

## Common Issues

### No map tiles appear

The Azure Maps key is missing or invalid. The app should fall back to an OpenStreetMap tile layer automatically. If nothing loads:

1. Open the browser developer console (`F12` → Console tab).
2. Look for network errors on tile or map requests.
3. Confirm `AZURE_MAPS_KEY` is empty in `.env` — if it is set to an invalid value, it can prevent the fallback from activating.

Fix: set `AZURE_MAPS_KEY=` (empty) in `.env` to force the OSM fallback.

---

### API returns sample data when Cosmos or Blob is expected

Check `/api/data-status` first:

```bash
curl -s http://localhost:8000/api/data-status | python3 -m json.tool
```

If `cosmosAvailable` is `false` when you expect it to be `true`:
- Confirm `COSMOS_ENDPOINT` and `COSMOS_KEY` are set in `.env`.
- Confirm the Cosmos account exists and the database and containers are seeded.
- Run `python3 scripts/seed_cosmos.py` from the project root with the correct env vars set.

---

### Sample data files fail to load

Run the data validator:

```bash
python3 scripts/validate_data.py
```

If a file is missing or malformed, the validator reports which one. Restore from git if needed:

```bash
git checkout -- app/static/sample-data/
```

---

### Docker container exits immediately

Check the build first:

```bash
docker build -t riyadh-mobility-dash .
```

Then run with logs attached:

```bash
docker run --rm -p 8001:8000 riyadh-mobility-dash
```

If the container exits, the error usually points to a missing module or a bad `requirements.txt`.

---

### `azd up` fails

1. Run `az login` and `azd auth login` to refresh credentials.
2. Run `azd env get-values` to confirm the target subscription, resource group, and location.
3. Try `azd deploy` (skip infrastructure) if the container needs to be rebuilt but infrastructure is already deployed.
4. Check App Insights or the Container App logs in the Azure portal for post-deploy errors.

---

### Deployed app loads but data is wrong

1. Open `/api/data-status` on the deployed URL.
2. If `activeMode` is `sample`, the Cosmos and Blob credentials were not injected into the Container App environment.
3. Set the secrets via `azd env set VAR_NAME value` then redeploy, or set them directly in the Container App environment variables in the Azure portal.

---

## Full Smoke Test Checklist

**Local**
- [ ] App starts with `python -m uvicorn app.main:app --reload`
- [ ] Dashboard loads at `http://localhost:8000`
- [ ] Map renders (tiles or OSM fallback)
- [ ] Metro layer toggles on and off
- [ ] Bus layer toggles on and off
- [ ] District selector shows 10 districts
- [ ] District selection updates the score panel
- [ ] `/health` returns 200
- [ ] `/api/data-status` returns `sample` mode
- [ ] `python -m pytest` passes all tests

**Docker**
- [ ] `docker build -t riyadh-mobility-dash .` succeeds
- [ ] Container starts and `/health` returns 200 on port 8001
- [ ] Dashboard loads inside the container

**Azure**
- [ ] `azd up` completes without error
- [ ] Deployed URL loads the dashboard
- [ ] `/health` on the deployed URL returns 200
- [ ] `/api/data-status` on the deployed URL shows the correct active mode
- [ ] App Insights shows traffic from the deployed app

---

## Debug Endpoints

| Endpoint | What it tells you |
|---|---|
| `/health` | app is alive |
| `/api/data-status` | active data source and fallback state |
| `/api/config` | runtime configuration sent to the frontend |
| `/api/districts` | district list — check count and IDs |
| `/api/routes` | route summary list — check count |
| `/api/live-events` | live event markers |

---

## Getting Help

If you need help:

1. Check this troubleshooting page first.
2. Run `python -m pytest -v` to confirm the backend is intact.
3. Check `/api/data-status` to isolate whether the issue is frontend, API, or data.
4. Ask a mentor with the specific endpoint URL and error message.
