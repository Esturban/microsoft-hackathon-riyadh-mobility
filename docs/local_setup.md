# Local Setup

1. Create a virtualenv.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. `python -m uvicorn app.main:app --reload`
5. Open `http://localhost:8000`

Without `AZURE_MAPS_KEY`, the app uses an OpenStreetMap fallback and still exposes the full API and scoring flow.
