# Spec Traceability

This repo is split to keep the build traceable against `spec.md`.

## Vertical slices

- App shell and docs: repo scaffold, quickstart, architecture, deployment notes
- Backend/API: FastAPI app, fallback-aware data access, scoring, required endpoints
- Frontend/UI: Azure Maps-ready dashboard, layer toggles, district scoring panel, debug view
- Data + infra: sample data, fetch/normalize/upload/seed scripts, tests, Docker, `azd`, Bicep, streaming placeholders

## Source of truth

- Scope and required behavior live in [spec.md](/Users/EVA/Desktop/eva/03_development/_dev/repos/00_apps/js-ts/riyadh_ud/spec.md)
- Commit history should map to the slices above
