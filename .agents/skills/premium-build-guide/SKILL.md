---
name: premium-build-guide
description: Create, revise, and polish technical build guides into premium report-style Markdown, DOCX, and PDF deliverables. Use when a user asks for a beautiful build guide, workbook, deployment guide, implementation guide, hackathon guide, starter-kit guide, DOCX/PDF report polish, reusable documentation template, or Google/consulting-style technical report design.
---

# Premium Build Guide

## Core Workflow

Use this skill to turn a useful but plain technical guide into a polished report-style workbook.

1. Inspect the source guide, generated DOCX/PDF, and rendered page PNGs before editing.
2. Preserve Markdown as source of truth unless the repo states otherwise.
3. Identify pages that feel exported from Word: dense tables, long bullets, tiny screenshots, repeated section forms, weak transitions, and dead whitespace.
4. Add report plates where they improve comprehension: executive brief, service matrix, architecture blueprint, local run playbook, deployment blueprint, adaptation routes, demo flow.
5. Reduce duplicated plain tables when a designed plate now carries the same information.
6. Regenerate DOCX and PDF, render pages to PNG, inspect representative pages, then iterate.
7. Run project tests and documentation checks before committing.

## Design System

Read [references/report_design_system.md](references/report_design_system.md) before a major redesign. Use it for page archetypes, typography, color, plate structure, and readability gates.

Use the bundled plate generator for fast report pages:

```bash
python .agents/skills/premium-build-guide/scripts/generate_report_plate.py path/to/plate-spec.json --out docs/assets/rebuild-guide
```

If the guide needs custom layouts, copy or adapt the script instead of hand-writing one-off Pillow code in the shell.

## Page Strategy

Use designed visual pages for orientation, decisions, and synthesis. Keep detailed prose for implementation steps.

- Cover: first impression, title, purpose, repo/local/deployed links.
- Navigation: how to use the guide, quick access, local-first principle.
- Executive brief: what builders get, what judges see, metrics, build path.
- Service matrix: group services by responsibility, not vendor list order.
- Architecture blueprint: local path, cloud path, fallback path, score/request flow.
- Local run playbook: command ladder, expected signal, slow-load warning.
- Deployment blueprint: prerequisites, resource map, smoke tests, teardown warning.
- Adaptation routes: track cards with keep, replace, add, likely services.

## Readability Rules

- Treat rendered PDF pages as authoritative; DOCX XML and Markdown are not enough.
- Keep body text readable after DOCX scaling. If a generated plate looks good at full image size but too small in PDF, regenerate with fewer words and larger type.
- Prefer one strong designed page over a designed page followed by a duplicate plain table.
- Avoid large blank pages caused by page breaks after short sections.
- Keep screenshots large enough to inspect, but crop around the decision moment.
- Add captions only when they help; do not let captions dominate visual pages.
- Do not mention internal cost, process complaints, or design criticism in the deliverable.

## Verification

Use the repo's existing commands where available. For this project, the expected loop is:

```bash
pandoc docs/rebuild_guide.md --resource-path=. --from markdown+raw_tex --to docx -o docs/rebuild_guide.docx
soffice --headless --convert-to pdf --outdir /tmp/guide-pdf docs/rebuild_guide.docx
pdftoppm -png -r 144 docs/rebuild_guide.pdf /tmp/guide-pages/page
python3 scripts/validate_data.py
.venv/bin/python -m pytest
```

Inspect the rendered PNGs before declaring the guide done.
