# Vizdantic

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-experimental-orange)
![License](https://img.shields.io/badge/license-MIT-green)

**Vizdantic** is a schema-first visualization layer for LLMs.

It allows language models to describe *what* to visualize using structured,
validated specifications, while developers remain in full control of *how*
charts are rendered.

---

## Why Vizdantic?

LLMs are good at describing intent, but unreliable at writing plotting code.

They often:

- hallucinate APIs
- mix incompatible chart parameters
- produce brittle, unvalidated code

Vizdantic solves this by separating responsibilities:

> **LLMs choose visualization intent.**
> **Developers choose the plotting library.**

---

## What Vizdantic Does

- Provides **Pydantic schemas** for common visualization types
- Validates LLM-generated visualization intent
- Is **library-agnostic** by design
- Renders charts via optional plugins (e.g. Plotly)

Vizdantic does **not** replace plotting libraries.
It sits between LLMs and visualization backends.

---

## Quick Start

### Install

```bash
pip install vizdantic
```

### Validate LLM output

```python
from vizdantic import validate

llm_output = {
    "kind": "cartesian",
    "chart": "bar",
    "x": "category",
    "y": "value",
    "title": "Sales by Category",
}

spec = validate(llm_output)
```

### Render with Plotly Example

```python
from vizdantic.plugins.plotly import render
import pandas as pd

df = pd.DataFrame({
    "category": ["A", "B", "C"],
    "value": [10, 20, 15],
})

fig = render(spec, df)
fig.show()
```

---

## Using Vizdantic with LLMs

Vizdantic works with **any LLM** and supports  **two common integration patterns** .

| Prompt-based (Universal)                                               | Tool / Function Calling (Structured)                                            |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Use when your LLM does**not** support tools or function calling. | Use when your LLM**supports JSON schema tools**(OpenAI, Anthropic, etc.). |
| You embed the schema directly in the prompt.                           | You pass the schema as a tool input contract.                                   |

### Prompt-based integration

```yaml
You are an assistant that creates visualization specifications.

Return JSON that strictly conforms to the following schema:


{{ vizdantic.schema() }}


Rules:
- Return JSON only
- Choose the most appropriate chart type
- Use column names exactly as provided
```

Example model output:

```json
{
  "kind":"cartesian",
  "chart":"bar",
  "x":"category",
  "y":"value",
  "title":"Sales by Category"
}
```

---

### Tool / function calling integration

```json
tool = {
    "name": "create_visualization",
    "description": "Create a visualization specification",
    "input_schema": vizdantic.schema(),
}
```

The LLM is now constrained to  **valid Vizdantic output only** .

---

## Validate and Render

Once the LLM returns JSON, the workflow is the same:

```python
from vizdantic import validate
from vizdantic.plugins.plotly import render

spec = validate(llm_output)
fig = render(spec, df)
fig.show()
```

## Custom Styling and Branding

Vizdantic **does not control styling**.

It intentionally avoids:

- colors
- themes
- fonts
- layout decisions

Vizdantic only defines **visualization intent**.
All styling remains fully under **user control**.

This makes it safe to use in production environments with strict
brand or design requirements.

---

### Example: Company styling (Evil Corp)

```python
from vizdantic.plugins.plotly import render

def evil_corp_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        colorway=["#ff0000", "#000000"],
        font=dict(family="Inter"),
    )
    return fig

fig = render(spec, df)
fig = evil_corp_theme(fig)
fig.show()
```

The LLM decides what to visualize.
Your code decides how it looks.

Vizdantic never overrides user-defined styling.

## How It Works

1. An LLM produces structured visualization intent (JSON)
2. Vizdantic validates it using Pydantic
3. A plugin translates the spec into a concrete chart

The schema is stable and backend-agnostic.

Rendering is handled entirely by plugins.

---

## Plugins

Currently supported:

* **Plotly** (`vizdantic.plugins.plotly`)

Planned:

* Matplotlib
* Altair
* Vega-Lite

Each plugin exposes a simple:

<pre class="overflow-visible! px-0!" data-start="3915" data-end="3947"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="@w-xl/main:top-9 sticky top-[calc(--spacing(9)+var(--header-height))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>render(spec, data)
</span></span></code></div></div></pre>

function.

---

## Status

* **Version:** 0.1.0
* **Stability:** Experimental
* **Breaking changes:** Possible until 1.0

Vizdantic is under active development and feedback is welcome.
