# Premium Build Guide Design System

## Archetype

Use an executive field-guide style: polished enough for sponsors and judges, practical enough for builders. The document should feel like a technology report, not a raw README export.

## Palette

- Navy: `#08182F` for headers, footer bands, and high-authority callouts.
- Cyan: `#11ABE8` for rules, highlights, and report identity.
- Blue: `#007CBE` for runtime and app layers.
- Green: `#0FB280` for local success and data readiness.
- Orange: `#F57522` for deployment, warnings, and action.
- Purple: `#7E57FF` for adaptation, scoring, and strategy.
- Red: `#EB4444` only for risk, telemetry, or failure states.
- Background: near-white `#F5F9FC`.

## Typography

For generated plates at 2550 x 3300:

- Title: 88-96 px bold.
- Section heading: 50-56 px bold.
- Card heading: 32-42 px bold.
- Body: 29-34 px.
- Small labels: 22-27 px.
- Avoid body text under 24 px unless it is metadata.

For DOCX:

- Cover title: 34-40 pt.
- Body: about 11 pt.
- Heading 1: 22-26 pt.
- Heading 2: 15-17 pt.
- Code: readable monospace, about 9.5 pt.

## Plate Patterns

### Executive Brief

Use for the first body page after the guide navigation.

Include:

- One-sentence thesis.
- 3-4 metric cards.
- Two judgment cards: what it proves and what it does not claim.
- A build path ladder.
- A dark bottom callout with the guiding principle.

### Service Matrix

Group by job:

- Local app runtime.
- Map and cloud data.
- Deploy and observe.
- Infrastructure workflow.

Each card should include service/tool, role, and builder touchpoint. Do not turn this into a long vendor list.

### Architecture Blueprint

Show:

- Browser/dashboard to FastAPI to data access to map/score UX.
- Local-first path.
- Azure-backed path.
- Fallback chain.
- Score request flow.

End with the rule: Azure should enhance the app, not be required for first success.

### Product Story Plate

Use when the "what you are building" section looks like a plain README page or leaves a large blank area. The plate should make the starter-kit thesis visible without requiring a long paragraph.

Show:

- The core user experience.
- The starter-kit principle.
- The judge-facing proof.
- The build question or domain thesis.

Prefer this plate over a large screenshot plus duplicated explanatory prose.

### Track Mapping Plate

Use when a challenge/track section is mostly positioning text and would otherwise create a half-empty page.

Show:

- Primary track fit.
- Strong secondary fit.
- Extension paths.
- Azure emphasis.
- A positioning rule that prevents overclaiming.

Keep the later adaptation routes page if it adds concrete "keep / replace / add / services" guidance.

### Local Run Playbook

Use a command ladder:

- Clone.
- Environment.
- Install.
- Configure.
- Start.
- Verify.

Each step needs a command and an expected signal. Include the slow-load warning as a highlighted card.

### Local Verification Plate

Use when the local checklist creates a mostly blank page before the backend or API section.

Group checks by:

- UI readiness.
- API checks.
- Builder commands.

The plate should preserve the slow-load warning and the concrete success signal: dashboard visible, overlays present, selector populated, score panel updating, `/health` OK, and `/api/data-status` explaining active data source.

### API Contract Plate

Use when the backend endpoint table starts to dominate the page.

Group endpoints by journey:

- Bootstrap.
- Map layers.
- District scoring.
- Diagnostics.

Each group should include endpoint paths, the purpose, and what a builder or judge should look for. Keep the detailed endpoint table only if the guide is primarily an API reference.

### Cloud Deployment Blueprint

Show:

- Authenticate.
- Initialize.
- Deploy.
- Verify.
- Operate.
- Teardown.

Add resource cards for Container Apps, Registry, Maps, Blob, Cosmos, App Insights, and Log Analytics. Include after-deploy checks and a slow-load expectation.

### Track Adaptation Routes

Use four large cards:

- Transformational Technology.
- Prosperous People.
- Sustainable Solutions.
- Culture.

Each card should answer: what to reuse from the starter kit and what to add for the track.

## Readability Gates

Before finalizing:

- Render DOCX to PDF, then PDF to PNG.
- Inspect page 1, page 2, first body page, service page, architecture page, deployment page, adaptation page, and appendix pages.
- Fail the pass if a plate requires zooming to understand normal body text.
- Fail the pass if a designed page is followed by a duplicate plain table saying the same thing.
- Fail the pass if large blank pages appear after page breaks.
- Fail the pass if screenshots are too small to inspect.
