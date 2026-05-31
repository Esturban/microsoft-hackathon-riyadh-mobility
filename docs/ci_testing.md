# CI and Testing Guide

Run the test suite, check what each test covers, and add new tests safely.

---

## Quick Run

```bash
# Activate the virtualenv first
source .venv/bin/activate

# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run a specific test file
python -m pytest tests/test_scoring.py -v

# Run with timing
python -m pytest -v --tb=short --durations=5
```

Or via npm:

```bash
npm test
```

---

## Test Suite Layout

```
tests/
├── conftest.py            shared fixtures (TestClient, sample data paths)
├── test_api_health.py     liveness, config, caching headers
├── test_api_routes.py     route, district, score, and geojson endpoints
├── test_data_shapes.py    sample GeoJSON structural contracts
└── test_scoring.py        scoring formula and delay penalty unit tests
```

---

## What Each File Covers

### `test_api_health.py` — System Contracts

| Test | What it verifies |
|---|---|
| `test_health` | `/health` returns 200 with `status: ok` |
| `test_data_status` | `/api/data-status` returns a recognized `activeMode` |
| `test_config_is_safe_for_frontend` | `/api/config` never leaks `azureMapsKey` |
| `test_frontend_assets_disable_caching` | HTML and JS assets carry `no-store` cache headers |

The caching test verifies that HTML and JS assets use `no-store` so the browser loads the latest code.

---

### `test_api_routes.py` — API Endpoints

| Test | What it verifies |
|---|---|
| `test_routes_returns_list` | `/api/routes` returns a JSON list |
| `test_metro_geojson_shape` | `/api/routes/geojson?mode=metro` is a valid FeatureCollection |
| `test_bus_geojson_shape` | `/api/routes/geojson?mode=bus` is a valid FeatureCollection |
| `test_districts_returns_list` | `/api/districts` returns non-empty list |
| `test_district_has_required_fields` | each district has `id`, `name`, `lat`, `lon` |
| `test_score_endpoint_returns_score` | `/api/score?districtId=...` returns score and rating |
| `test_score_rating_bands` | first three districts each return a valid rating band |
| `test_live_events_returns_list` | `/api/live-events` returns a list |

---

### `test_data_shapes.py` — Data Contracts

| Test | What it verifies |
|---|---|
| `test_sample_geojson_shapes` | all three sample GeoJSON files are valid FeatureCollections with at least one feature |

This test catches file corruption, missing files, or schema drift in the sample data.

---

### `test_scoring.py` — Business Logic

| Test | What it verifies |
|---|---|
| `test_accessibility_score_formula` | 2 metro + 6 bus − 1 penalty = score 11, rating High |
| `test_accessibility_score_low_medium_high_bands` | boundary conditions for Low / Medium / High |
| `test_delay_penalty_only_counts_medium_and_high_nearby` | low-severity events do not count; distant events do not count |

These are pure unit tests with no HTTP or file I/O.

---

## Response Time Baselines

Run with `--durations=5` to see the five slowest tests. Expected baselines on a cold venv:

| Endpoint | Expected p95 response (local, sample mode) |
|---|---|
| `GET /health` | < 20 ms |
| `GET /api/routes` | < 50 ms |
| `GET /api/routes/geojson?mode=metro` | < 100 ms |
| `GET /api/districts` | < 50 ms |
| `GET /api/score?districtId=...` | < 100 ms |
| `GET /api/live-events` | < 30 ms |

If any endpoint consistently exceeds 200 ms in sample mode, check for unintended disk reads or imports at request time.

---

## Manual Smoke Tests

Run these before each demo or deployment:

```bash
# 1. Local server
python -m uvicorn app.main:app --reload &
UVICORN_PID=$!
sleep 2

# 2. Health probe
curl -s http://localhost:8000/health | python3 -m json.tool

# 3. Data status
curl -s http://localhost:8000/api/data-status | python3 -m json.tool

# 4. Config (should NOT contain azureMapsKey)
curl -s http://localhost:8000/api/config | python3 -m json.tool

# 5. Metro GeoJSON (check featureCount)
curl -s "http://localhost:8000/api/routes/geojson?mode=metro" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(f'Metro features: {len(d[\"features\"])}')"

# 6. Districts (check count)
curl -s http://localhost:8000/api/districts | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(f'Districts: {len(d)}')"

# 7. Score (pick a district)
curl -s "http://localhost:8000/api/score?districtId=riyadh-north" | python3 -m json.tool

# Tear down
kill $UVICORN_PID
```

---

## Docker Smoke Test

```bash
docker build -t riyadh-mobility-dash .
docker run --rm -p 8001:8000 riyadh-mobility-dash &
sleep 3
curl -s http://localhost:8001/health
docker stop $(docker ps -q --filter ancestor=riyadh-mobility-dash)
```

Expected: `{"status":"ok","version":"..."}` within 3 seconds.

---

## Adding Tests

### Unit test pattern

```python
# tests/test_my_feature.py
from app.scoring import compute_accessibility_score

def test_my_case():
    result = compute_accessibility_score(nearby_metro_count=1, nearby_bus_count=3, live_delay_penalty=0)
    assert result["score"] == 6
    assert result["rating"] == "Medium"
```

### API test pattern

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_my_endpoint():
    response = client.get("/api/my-endpoint")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
```

### Data shape test pattern

```python
import json
from pathlib import Path

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "app" / "static" / "sample-data"

def test_my_sample_file():
    payload = json.loads((SAMPLE_DIR / "my_file.geojson").read_text())
    assert payload["type"] == "FeatureCollection"
    assert len(payload["features"]) > 0
    for feat in payload["features"]:
        assert "geometry" in feat
        assert "properties" in feat
```

---

## CI Integration

The test suite is framework-agnostic and can run in any CI pipeline that supports Python:

```yaml
# Example GitHub Actions step
- name: Run tests
  run: |
    pip install -r requirements.txt
    python -m pytest -v --tb=short
```

For Azure Pipelines, use the same `pip install` + `pytest` commands in a script step.

The full suite runs in under 2 seconds. There are no network calls in the test suite — all tests use the FastAPI TestClient and bundled sample data.
