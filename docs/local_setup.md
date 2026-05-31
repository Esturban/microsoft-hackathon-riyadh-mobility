# Local Setup

Get a working dashboard in under five minutes. No Azure credentials required.

---

## Prerequisites

- Python 3.11 or newer (`python3 --version`)
- Git
- A terminal

---

## Steps

### 1. Create and activate a virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your environment file

```bash
cp .env.example .env
```

The defaults in `.env.example` set `DATA_MODE=sample`. You do not need to fill in any Azure values to run locally.

### 4. Start the server

```bash
python -m uvicorn app.main:app --reload
```

### 5. Open the dashboard

```
http://localhost:8000
```

---

## Without `AZURE_MAPS_KEY`

The app falls back to an OpenStreetMap tile layer. The API, scoring, and panels all work identically. You only need an Azure Maps key to get the official Riyadh satellite and road tiles.

---

## Verification Checklist

After the server starts:

- [ ] Dashboard loads at `http://localhost:8000`
- [ ] Metro layer toggles on and off
- [ ] Bus layer toggles on and off
- [ ] District selector appears (10 Riyadh districts)
- [ ] Selecting a district shows a score and rating
- [ ] `http://localhost:8000/health` returns `{"status":"ok"}`
- [ ] `http://localhost:8000/api/data-status` returns `{"activeMode":"sample"}`

---

## npm Shortcuts

If you have Node.js installed, these npm scripts wrap the common commands:

```bash
npm test               # run the pytest suite
npm run validate:data  # validate sample data file shapes
npm run fetch:data     # fetch raw RCRC data (requires network)
npm run normalize:data # normalize raw data to GeoJSON
npm run deploy:azure   # deploy to Azure with azd
```

---

## Common Issues

**`ModuleNotFoundError`** — the virtualenv is not active. Run `source .venv/bin/activate`.

**Port 8000 already in use** — kill the process (`lsof -ti:8000 | xargs kill`) or run on a different port (`uvicorn app.main:app --reload --port 8001`).

**Map shows no tiles** — no Azure Maps key is set. The OpenStreetMap fallback should appear. If nothing loads, check the browser console for network errors.
