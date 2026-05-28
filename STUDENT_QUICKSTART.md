# Student Quickstart

## What a mobility dashboard is

A mobility dashboard is a simple app that helps you see how people move through a city. In this repo, the dashboard shows Riyadh metro lines, bus routes, district centers, and simple delay events on one map.

## What Azure Maps does

Azure Maps draws the city map and the transport layers. It helps us show metro lines, bus routes, district markers, and the 1.5 km access buffer around a selected district.

## What Blob Storage does

Blob Storage is the project file shelf. We save raw data downloads there and can also save cleaned GeoJSON files there after processing.

## What Cosmos DB does

Cosmos DB is the project app-data store. It keeps route summaries, district scores, and the latest mock events so the API can return ready-to-use records.

## Why simulated live events are acceptable

This project is a hackathon starter, not a control-room system. Simulated delay and congestion events are enough to show how a city dashboard could react to live data later.

## How to run the app locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000`.

## How to modify one sample district

Open [district_centers_sample.geojson](/Users/EVA/Desktop/eva/03_development/_dev/repos/00_apps/js-ts/riyadh_ud/app/static/sample-data/district_centers_sample.geojson) and change one district name or coordinates. Reload the app and pick that district from the dropdown.

## How to add a new route layer

1. Add a new GeoJSON file under [app/static/sample-data](/Users/EVA/Desktop/eva/03_development/_dev/repos/00_apps/js-ts/riyadh_ud/app/static/sample-data).
2. Add a backend loader in [app/data_access.py](/Users/EVA/Desktop/eva/03_development/_dev/repos/00_apps/js-ts/riyadh_ud/app/data_access.py).
3. Add a frontend source and layer in [app/static/src/map.js](/Users/EVA/Desktop/eva/03_development/_dev/repos/00_apps/js-ts/riyadh_ud/app/static/src/map.js).
4. Add a toggle in [app/static/index.html](/Users/EVA/Desktop/eva/03_development/_dev/repos/00_apps/js-ts/riyadh_ud/app/static/index.html).

## How to explain the project to judges

Use plain language:

“We built a Riyadh mobility dashboard that loads public or sample transit data, stores files in Blob Storage, stores summaries in Cosmos DB, shows the results on Azure Maps, and calculates a simple district accessibility score.”
