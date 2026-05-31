# Data Sources

---

## RCRC Open Datasets

The sample data in this starter kit is derived from the Riyadh Commission for Riyadh City (RCRC) open geospatial datasets published through the Saudi Open Data portal.

| Dataset | RCRC dataset name | What it contains |
|---|---|---|
| Metro lines | `metro-lines-in-riyadh-2024` | 6 metro lines with route geometry and color codes |
| Bus routes | `bus-roads-by-direction-in-riyadh-2024` | 100 bus routes with directional geometry |

---

## What is in the Sample Files

The bundled sample files live in `app/static/sample-data/` and are always available, even when Azure services are not configured.

| File | Contents | Records |
|---|---|---|
| `riyadh_metro_lines_sample.geojson` | Metro line features with name, color, and geometry | 6 features |
| `riyadh_bus_routes_sample.geojson` | Bus route features with route ID and direction | 100 features |
| `district_centers_sample.geojson` | District center points with name, nameAr, and description | 10 features |
| `mock_live_events_sample.json` | Sample live-event markers with severity and position | variable |

All files are GeoJSON FeatureCollections. District centers include both English and Arabic names (`name` and `nameAr`).

---

## District List

The 10 Riyadh districts included in the sample:

| ID | Name (EN) | Name (AR) |
|---|---|---|
| `riyadh-north` | Riyadh North | شمال الرياض |
| `riyadh-south` | Riyadh South | جنوب الرياض |
| `riyadh-east` | Riyadh East | شرق الرياض |
| `riyadh-west` | Riyadh West | غرب الرياض |
| `riyadh-center` | Riyadh Center | وسط الرياض |
| `al-malaz` | Al Malaz | الملز |
| `al-olaya` | Al Olaya | العليا |
| `al-sulimaniyah` | Al Sulimaniyah | السليمانية |
| `al-wurud` | Al Wurud | الورود |
| `al-naseem` | Al Naseem | النسيم |

---

## Fetching Fresh Data

To update the sample files from the RCRC sources:

```bash
python3 scripts/fetch_rcrc_data.py
python3 scripts/normalize_to_geojson.py
python3 scripts/validate_data.py
python3 scripts/upload_to_blob.py       # optional: upload to Blob Storage
PYTHONPATH=. python3 scripts/seed_cosmos.py  # optional: seed Cosmos DB
```

---

## Runtime Rule

The app must keep working from bundled sample data if remote sources or Azure services are unavailable.

Always keep the dashboard working from bundled sample data. If remote sources or Azure services fail, fall back to Cosmos DB, Blob Storage, or sample files in that order.

---

## Adding New Data

To add a new data layer (for example, AQI stations or parking lots):

1. Create a normalized GeoJSON file in `app/static/sample-data/`.
2. Add an API endpoint in `app/routes.py` that serves the file.
3. Add a rendering function in `app/static/src/layers.js`.
4. Add a toggle control in `app/static/index.html`.
5. Update the upload script if you want to store the data in Blob Storage.
6. Add a test in `tests/test_data_shapes.py` to validate the file shape.
