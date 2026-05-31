# Judging Demo Script

A short demo script for pitching the Riyadh Mobility Intelligence Dashboard to hackathon judges.

Target: 5–7 minutes. No slides required.

---

## Setup Before the Demo

1. Open the dashboard in a browser — local or deployed.
2. Have `/api/data-status` ready in a second tab.
3. If using the deployed app, confirm it loads and `/health` returns 200.
4. Know which district you will select (Riyadh North is a clear example with good coverage).

---

## Step 1 — Open the Dashboard (30 seconds)

Show the full dashboard view on load.

> "This is the Riyadh Mobility Intelligence Dashboard. It shows metro and bus coverage across Riyadh, calculates a district accessibility score, and runs on an Azure-backed architecture. We built it as a starter kit — a reusable scaffold that any hackathon team can adapt."

Point to:
- the Riyadh map centered on the city
- the metro and bus layer toggles
- the district selector panel

---

## Step 2 — Toggle the Map Layers (60 seconds)

Toggle metro off, then on. Toggle bus off, then on.

> "The map pulls metro and bus data from the RCRC open datasets — six metro lines and a hundred bus routes. In sample mode it runs entirely from bundled files. In cloud mode it reads from Azure Blob Storage or Cosmos DB."

> "Each layer is a GeoJSON FeatureCollection served by a FastAPI endpoint. Builders can replace or extend any layer just by changing the data pipeline."

---

## Step 3 — Select a District and Show the Score (90 seconds)

Select Riyadh North (or the district with the clearest score).

> "When a builder selects a district, the app calls `/api/score` with that district ID. The backend counts how many metro stops and bus routes fall within 1.5 km of the district center, then applies a live-event penalty for any nearby delays or incidents."

Point to the score panel:
- the district name and score number
- the formula breakdown (metro count × 3 + bus count − penalty)
- the Low / Medium / High rating

> "The formula is intentionally transparent. Teams can adjust the weights, the buffer radius, or the penalty logic to fit a different track — walkability, pollution access, heritage routing."

---

## Step 4 — Show the Fallback-Aware Architecture (60 seconds)

Open `/api/data-status` in the second tab.

> "This endpoint shows the active data source. In production it would say `cosmos`. Here it says `sample`, which means the app is running entirely from bundled data. This is the fallback-aware design: the demo never breaks because of a missing cloud credential."

> "The fallback chain is: Cosmos DB → Blob Storage → bundled sample files. The score, the map, and the panels all work at every level."

---

## Step 5 — Show the Azure Layer (60 seconds)

Describe the cloud-live path without switching screens.

> "When deployed to Azure, the same container runs on Azure Container Apps. Azure Maps provides the cloud tile layer. The processed RCRC data lives in Blob Storage. District and route records are in Cosmos DB. Application Insights tracks API health. All of it deploys with one command: `azd up`."

> "The infrastructure is defined in Bicep, so teams can spin up a clean environment in under five minutes and tear it down after the demo."

---

## Step 6 — Explain the Starter Kit Routes (60 seconds)

> "The most important thing about this scaffold is that it is not just a mobility dashboard. The same architecture supports four hackathon tracks."

| Track | Extension path |
|---|---|
| Transformational Technology | add congestion layers and live Event Hubs feeds |
| Prosperous People | evolve district scoring into a 15-minute city walkability score |
| Sustainable Solutions | overlay AQI, heat, or emissions data alongside route coverage |
| Culture | adapt the map for heritage sites, event routing, and visitor movement |

> "Any team can fork this starter kit, remove the mobility data, and replace it with data for their track — using the same FastAPI backend, the same Azure services, and the same scoring pattern."

---

## Closing (30 seconds)

> "To summarize: a Riyadh mobility intelligence dashboard that runs locally from open RCRC data, demonstrates a full Azure-backed cloud path, and serves as a reusable scaffold for all four hackathon tracks. The code is clean, the architecture is documented, and the demo never depends on a live cloud connection."

---

## Common Judge Questions

**Q: Is this real data?**
A: Yes — metro lines and bus routes are from the RCRC open datasets for Riyadh 2024. The sample files are normalized from that source. The live Cosmos path uses the same data.

**Q: How fast can a team adapt this?**
A: Local mode works in under five minutes. A team that wants to swap the data source or adjust the score formula can do it in a single afternoon.

**Q: What Azure services does this use?**
A: Container Apps, Azure Maps, Blob Storage, Cosmos DB, and Application Insights. All defined in Bicep and deployed with Azure Developer CLI.

**Q: Can it handle live streaming data?**
A: The architecture is ready for it — Event Hubs is listed as a stretch extension. The live-events endpoint and the delay penalty formula already exist. Connecting a real stream would be a one-day addition.
