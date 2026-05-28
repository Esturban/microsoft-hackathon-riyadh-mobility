# Troubleshooting

- If the map does not render, confirm `AZURE_MAPS_KEY` is set.
- If Azure calls fail, the API should fall back to sample mode; check `/api/data-status`.
- If RCRC endpoints change, rerun fetch and normalization after inspecting the raw schema in `data/raw`.
