# Troubleshooting

- If the map does not render, confirm `AZURE_MAPS_KEY` is set.
- If Azure calls fail, the API should fall back to sample mode; check `/api/data-status`.
- If RCRC endpoints change, rerun fetch and normalization after inspecting the raw schema in `data/raw`.

## Manual smoke test checklist

- [ ] App starts locally
- [ ] Map loads
- [ ] Metro layer appears
- [ ] Bus layer appears
- [ ] District selector works
- [ ] Score panel updates
- [ ] `/health` returns 200
- [ ] Docker build succeeds
- [ ] `azd` deployment completes
- [ ] Deployed app loads
