![](docs/assets/rebuild-guide/premium-cover-page.png){width=7.3in}

\newpage

![](docs/assets/rebuild-guide/premium-how-to-page.png){width=7.3in}

\newpage

![](docs/assets/rebuild-guide/premium-executive-build-brief.png){width=7.3in}

\newpage

![](docs/assets/rebuild-guide/premium-product-story.png){width=7.3in}

\newpage

![](docs/assets/rebuild-guide/premium-track-mapping.png){width=7.3in}

\newpage

![](docs/assets/rebuild-guide/premium-services-tools-matrix.png){width=7.3in}

\newpage

![](docs/assets/rebuild-guide/premium-architecture-blueprint.png){width=7.3in}

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

![](docs/assets/rebuild-guide/premium-local-run-playbook.png){width=7.3in}

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

Use a designed verification plate when the checklist starts to create a half-empty page.

\newpage

![](docs/assets/rebuild-guide/premium-local-verification.png){width=7.3in}

\newpage

![](docs/assets/rebuild-guide/premium-api-contracts.png){width=7.3in}

\newpage

# 6. Backend Walkthrough

Group endpoints by journey: bootstrap, map layers, scoring, and diagnostics. Explain what each group proves.

\newpage

# 7. Frontend Walkthrough

Explain page boot, map layers, controls, score panel, and visible success signals. Use screenshots that show the decision moment.

\newpage

![](docs/assets/rebuild-guide/premium-cloud-deployment-blueprint.png){width=7.3in}

\newpage

# 8. Cloud Deployment

List prerequisites, deployment commands, resources created, smoke tests, optional cloud data steps, and teardown.

\newpage

![](docs/assets/rebuild-guide/premium-track-adaptation-routes.png){width=7.3in}

\newpage

# 9. Adaptation Routes

For each route, explain what to keep, what to replace, what to add, and likely cloud services.

\newpage

# 10. Demo Flow

Give a short judge-facing flow: open app, show layers, select record/context, explain score, inspect diagnostics, explain cloud path, explain adaptation path.

\newpage

# Appendix

Include common commands, debugging checklist, visual asset checklist, glossary, and reference links.
