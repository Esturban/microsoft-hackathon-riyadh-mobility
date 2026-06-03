![](docs/assets/rebuild-guide/premium-cover-page.png)

\newpage

![](docs/assets/rebuild-guide/premium-how-to-page.png)

\newpage

![](docs/assets/rebuild-guide/premium-executive-build-brief.png)

\newpage

# 1. What You Are Building

State the product in one paragraph. Explain the user action, the data visible on screen, the backend/API role, and the intended demo outcome.

Include:

- what the app shows
- who uses it
- what decisions it supports
- what is intentionally simple or replaceable
- what makes it credible as a starter kit

![Primary dashboard screenshot](docs/assets/rebuild-guide/local-dashboard-overview.png)

*Figure: primary dashboard with the core workflow visible.*

\newpage

# 2. Challenge or Track Mapping

Explain the primary track fit, strongest secondary fit, and extension routes. Keep this concise; use a designed track/adaptation plate for comparison.

![](docs/assets/rebuild-guide/premium-services-tools-matrix.png)

\newpage

![](docs/assets/rebuild-guide/premium-architecture-blueprint.png)

\newpage

# 3. Architecture and Build Path

Explain the local-first path, cloud-backed path, and fallback path. The key principle: the app must remain useful even without cloud credentials.

## Local-First Workflow

Describe how the browser, backend, static frontend, and bundled sample data work together.

## Cloud-Backed Workflow

Describe what changes when deployed and connected to cloud services.

## Data Fallback Chain

Describe the order of preferred cloud data and guaranteed sample fallback.

\newpage

# 4. Project Structure

Show where builders should edit first. Prefer a short repository map over a full tree in the main flow.

| Area | Start here | Why it matters |
|---|---|---|
| Backend | `app/main.py`, `app/routes.py` | API contract and static serving |
| Frontend | `app/static/` | UI shell and browser behavior |
| Data | `app/data_access.py`, sample files | fallback and cloud data loading |
| Infrastructure | `azure.yaml`, `infra/` | deployable cloud path |
| Tests | `tests/` | confidence checks |

\newpage

![](docs/assets/rebuild-guide/premium-local-run-playbook.png)

\newpage

# 5. Run Locally

Provide copy-paste setup commands and expected success signals. Mention slow initial load and what to wait for before judging failure.

## Play-by-Play

```bash
git clone <repo-url>
cd <repo-folder>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

## Verification

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/api/data-status | python -m json.tool
python -m pytest
```

\newpage

![](docs/assets/rebuild-guide/premium-api-contracts.png)

\newpage

# 6. Backend Walkthrough

Group endpoints by journey: bootstrap, map layers, scoring, and diagnostics. Explain what each group proves.

\newpage

# 7. Frontend Walkthrough

Explain page boot, map layers, controls, score panel, and visible success signals. Use screenshots that show the decision moment.

\newpage

![](docs/assets/rebuild-guide/premium-cloud-deployment-blueprint.png)

\newpage

# 8. Cloud Deployment

List prerequisites, deployment commands, resources created, smoke tests, optional cloud data steps, and teardown.

\newpage

![](docs/assets/rebuild-guide/premium-track-adaptation-routes.png)

\newpage

# 9. Adaptation Routes

For each route, explain what to keep, what to replace, what to add, and likely cloud services.

\newpage

# 10. Demo Flow

Give a short judge-facing flow: open app, show layers, select record/context, explain score, inspect diagnostics, explain cloud path, explain adaptation path.

\newpage

# Appendix

Include common commands, debugging checklist, visual asset checklist, glossary, and reference links.
