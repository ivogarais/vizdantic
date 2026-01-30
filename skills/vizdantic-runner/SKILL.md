---
name: vizdantic-runner
description: "Run Vizdantic visualization workflows in this repo: load user datasets (CSV/Parquet/JSON/Excel), draft and validate Vizdantic specs, and render Plotly charts. Use when the user asks to visualize data, generate charts from a file/DataFrame, or execute Python to validate/render Vizdantic schema outputs."
---

# Vizdantic Runner

## Overview
Turn user data and intent into a validated Vizdantic spec and a rendered Plotly figure using this repo's schema and plugins.

## Workflow
1. Confirm data source, file path, intended chart/insight, and whether a custom theme is desired.
2. Inspect data minimally (columns, dtypes, head) to choose the correct spec fields.
3. Build a Vizdantic spec dict and validate it with `vizdantic.validate`.
4. Render with `vizdantic.plugins.plotly.render`.
5. Write outputs (HTML/PNG) and summarize what was generated.

## Data loading rules
- Use pandas to read data.
- Supported formats: CSV, Parquet, JSON (including JSONL), Excel.
- Treat user data as read-only.
- For large files, avoid full loads when possible:
  - Check file size first.
  - Use `--inspect` with `--nrows` to view columns and a small sample.
  - Use `--usecols` to limit columns.
  - If the file is huge and limits are not supported (e.g., some JSON/Parquet cases), ask the user for a smaller sample or filtered extract.

## Theme handling
- If the user wants a custom theme, ask how they want to provide it:
  - A quick description (brand colors, fonts, template name)
  - A JSON snippet for Plotly layout
  - A JSON file path
- Apply themes via `fig.update_layout(...)` using the script flags.
- To remember a theme for future runs, save it with `--remember-theme` (stored at `artifacts/vizdantic/theme.json` by default).
- Use `references/theme-quickstart.json` as a starting point when a user wants a custom theme but hasn't provided one.

## Spec guidance
- Use `references/vizdantic-spec-quickref.md` for required fields and chart options.
- If the schema is needed, print it with a short Python snippet:

```bash
python - <<'PY'
from vizdantic import schema
import json
print(json.dumps(schema(), indent=2))
PY
```

## Automation script
Use the bundled script for repeatable runs:

```bash
python skills/vizdantic-runner/scripts/render_viz.py \
  --data /path/to/data.csv \
  --spec '{"kind":"cartesian","chart":"bar","x":"month","y":"revenue"}'
```

Apply a custom theme (layout JSON):

```bash
python skills/vizdantic-runner/scripts/render_viz.py \
  --data /path/to/data.csv \
  --spec '{"kind":"cartesian","chart":"bar","x":"month","y":"revenue"}' \
  --theme '{"template":"plotly_dark","colorway":["#1f2937","#0ea5e9"],"font":{"family":"Inter"}}'
```

Remember the theme for future runs:

```bash
python skills/vizdantic-runner/scripts/render_viz.py \
  --data /path/to/data.csv \
  --spec '{"kind":"cartesian","chart":"bar","x":"month","y":"revenue"}' \
  --theme-file /path/to/theme.json \
  --remember-theme
```

Use a built-in Plotly template name:

```bash
python skills/vizdantic-runner/scripts/render_viz.py \
  --data /path/to/data.csv \
  --spec '{"kind":"cartesian","chart":"bar","x":"month","y":"revenue"}' \
  --theme-template plotly_dark
```

Start from the bundled quickstart theme:

```bash
python skills/vizdantic-runner/scripts/render_viz.py \
  --data /path/to/data.csv \
  --spec '{"kind":"cartesian","chart":"bar","x":"month","y":"revenue"}' \
  --theme-file skills/vizdantic-runner/references/theme-quickstart.json
```

Inspect a large file safely (columns, dtypes, head):

```bash
python skills/vizdantic-runner/scripts/render_viz.py \
  --data /path/to/data.csv \
  --inspect --nrows 200
```

Limit columns and rows:

```bash
python skills/vizdantic-runner/scripts/render_viz.py \
  --data /path/to/data.parquet \
  --usecols month,revenue \
  --nrows 5000 \
  --spec '{"kind":"cartesian","chart":"line","x":"month","y":"revenue"}'
```

Write both HTML and PNG:

```bash
python skills/vizdantic-runner/scripts/render_viz.py \
  --data /path/to/data.csv \
  --spec-file /path/to/spec.json \
  --html --png \
  --output-dir artifacts/vizdantic
```

## Dependency guardrails
- If `plotly` or `pandas` is missing, ask before installing.
- Preferred install for this repo: `pip install -e '.[plotly]' pandas`.

## Output expectations
- Default output directory: `artifacts/vizdantic/`.
- Summarize: data source, spec used, output paths, and any validation fixes.
