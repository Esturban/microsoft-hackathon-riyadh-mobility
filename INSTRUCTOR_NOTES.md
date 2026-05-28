# Instructor Notes

## 20-minute demo flow

1. Start the app in sample mode.
2. Show the Riyadh map shell and explain why sample mode matters.
3. Toggle metro, bus, and live event layers.
4. Select a district and walk through the score formula.
5. Open `/api/data-status` and explain fallback-aware design.
6. Close by showing the Azure deployment files.

## 60-minute guided build option

1. Introduce the problem and architecture in 10 minutes.
2. Run the starter app locally in 10 minutes.
3. Edit one district or route sample in 10 minutes.
4. Explain the FastAPI endpoints in 10 minutes.
5. Walk through Blob/Cosmos scripts in 10 minutes.
6. End with `azd` deployment overview in 10 minutes.

## Common student errors

- Forgetting to activate the virtual environment
- Editing invalid GeoJSON syntax
- Expecting Azure mode to work without credentials
- Confusing sample files with Cosmos summary documents

## How to switch between sample and cloud modes

- `DATA_MODE=sample`: always use bundled files
- `DATA_MODE=blob`: prefer Blob Storage, then fall back
- `DATA_MODE=cosmos`: prefer Cosmos DB summaries, then fall back
- `DATA_MODE=auto`: try Azure-backed data first, then sample

## How to explain each Azure service

- Azure Maps: draws the city and transport overlays
- Blob Storage: keeps raw and cleaned files
- Cosmos DB: keeps app-ready summaries and events
- Container Apps: hosts the web app
- Log Analytics and App Insights: track health and failures

## Suggested stretch tasks for advanced students

- Add a points-of-interest layer
- Add more districts and compare scores
- Replace sample events with Event Hubs input
- Add a route filter or route search
- Add a judge-facing summary page

## Judging rubric

- Problem clarity: can the team explain the city use case?
- Technical fit: did they use Azure services for a real reason?
- Data clarity: can they explain sample vs cloud data paths?
- Product clarity: does the UI tell a clear story quickly?
- Extension thinking: do they know what they would build next?
