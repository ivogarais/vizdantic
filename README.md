# Vizdantic

<img width="300" height="300" alt="ChatGPT Image Jan 27, 2026, 05_16_35 PM" src="https://github.com/user-attachments/assets/dc955536-c9f5-4e0e-890a-ed11030d51b0" />


![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-experimental-orange)
![License](https://img.shields.io/badge/license-MIT-green)

**Stop LLMs from hallucinating plotting APIs. Let them describe what to visualize instead.**

Vizdantic separates the data layer (what LLMs produce) from the view layer (what your code renders).

---

## The Problem

You want an LLM to create charts from data. You have two bad options:

1. **Let the LLM write plotting code** → It hallucinates APIs, mixes incompatible parameters, breaks on library updates
2. **Hardcode every chart type** → Rigid, doesn't scale, defeats the purpose of using an LLM

**The actual problem:** LLMs are great at understanding intent but terrible at remembering exact function signatures.

---

## The Solution

Vizdantic gives LLMs a stable contract: describe *what* to visualize, not *how* to plot it.

```python
# LLM outputs this (validated against schema):
{
  "kind": "cartesian",
  "chart": "bar",
  "x": "month",
  "y": "revenue"
}

# Your code renders it however you want:
fig = render(spec, df)
fig = apply_company_theme(fig)
fig.show()
```

**You get:**
- Validated LLM output (no hallucinated APIs)
- Full control over rendering (swap Plotly for Matplotlib anytime)
- Type-safe specs (a "flow" chart can't claim `chart="bar"`)

---

## Is This For You?

**Yes, if you:**
- Build LLM apps that generate charts
- Want LLMs to pick chart types, not write plotting code
- Need to enforce brand guidelines on LLM-generated visualizations
- Want a stable interface between LLM output and rendering logic

**No, if you:**
- Just need a plotting library (use Plotly/Matplotlib directly)
- Don't use LLMs for visualization
- Want the LLM to control colors/fonts/styling

---

## Quick Start

```bash
pip install vizdantic
```

```python
from vizdantic import validate
from vizdantic.plugins.plotly import render
import pandas as pd

# 1. LLM produces this JSON
llm_output = {
    "kind": "cartesian",
    "chart": "bar",
    "x": "month",
    "y": "revenue"
}

# 2. Validate it
spec = validate(llm_output)  # Raises ValidationError if invalid

# 3. Render it
df = pd.DataFrame({"month": ["Jan", "Feb", "Mar"], "revenue": [100, 150, 120]})
fig = render(spec, df)
fig.show()
```

That's it. The LLM never touches plotting code.

---

## Codex Skill (Optional)

This repo includes a Codex skill for running Vizdantic visualizations locally.

```bash
vizdantic install-codex-skill
```

Or with uv:

```bash
uv run vizdantic install-codex-skill
```

Restart Codex after installing. The skill will appear as `vizdantic-runner`.

---

## What Charts Are Supported?

Vizdantic supports **14 chart type categories** covering ~90% of common use cases:

| Category | Chart Types | Example Use Case |
|----------|-------------|------------------|
| **Cartesian** | bar, line, area, scatter | Time series, comparisons |
| **Distribution** | histogram, box, violin, strip | Statistical analysis |
| **Parts** | pie | Proportions, market share |
| **Geo** | choropleth, scatter_geo, mapbox | Geographic data |
| **Hierarchy** | treemap, sunburst, icicle | Organizational charts |
| **Flow** | sankey | Process flows, migrations |
| **Polar** | scatter_polar, line_polar, bar_polar | Directional data, wind roses |
| **Ternary** | scatter_ternary, line_ternary | 3-component compositions |
| **3D** | scatter_3d, line_3d | Spatial data |
| **Financial** | funnel, funnel_area | Sales funnels, conversions |
| **Parallel** | parallel_coordinates, parallel_categories | Multi-dimensional data |
| **Timeline** | timeline | Gantt charts, schedules |
| **Matrix** | heatmap, imshow | Correlation matrices |
| **Points** | scatter | Basic scatter plots |

Each category has strongly-typed chart options. The LLM can't create invalid combinations.

---

## How to Use With LLMs

Vizdantic works with any LLM. Two common patterns:

### Option 1: Prompt-Based (Universal)

Embed the schema in your prompt:

```python
from vizdantic import schema

prompt = f"""
You are a data visualization assistant.
Return JSON matching this schema:

{schema()}

User data columns: {df.columns.tolist()}
User request: "Show me revenue by month as a bar chart"
"""
```

The LLM returns JSON. You validate and render it.

### Option 2: Tool/Function Calling (Structured)

For LLMs that support tools (OpenAI, Anthropic, etc.):

```python
tool = {
    "name": "create_chart",
    "description": "Create a data visualization",
    "input_schema": schema()
}
```

The LLM is now constrained to valid output only.

---

## Styling: You're In Control

Vizdantic doesn't touch colors, fonts, or themes. That's intentional.

```python
def company_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        colorway=["#ff0000", "#000000"],
        font=dict(family="Inter")
    )
    return fig

fig = render(spec, df)
fig = company_theme(fig)  # Apply your branding
fig.show()
```

The LLM picks the chart type. You control everything else.

This is why Vizdantic works in production: it never fights your design system.

---

## Plugins

**Currently supported:**
- Plotly (`vizdantic.plugins.plotly`)

**Planned:**
- Matplotlib
- Altair
- Vega-Lite

Each plugin exposes one function: `render(spec, data) → figure`

Want a custom plugin? Implement that function. The spec is just a Pydantic model.

---

## Status

- **Version:** 0.2.2
- **Stability:** Experimental (breaking changes possible until 1.0)
- **Python:** 3.10+
- **License:** MIT

Feedback welcome. This is a real project solving a real problem, not a demo.
