# Vizdantic


![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-experimental-orange)
![License](https://img.shields.io/badge/license-MIT-green)

**Vizdantic** is a schema-first visualization layer for LLMs.

It allows language models to describe *what* to visualize using structured,

validated specifications — while developers remain in full control of *how*

charts are rendered.

---

## Why Vizdantic?

LLMs are good at describing intent, but unreliable at writing plotting code.

They often:

* hallucinate APIs
* mix incompatible chart parameters
* produce brittle, unvalidated code

Vizdantic solves this by separating responsibilities:

> **LLMs choose visualization intent.**

> **Developers choose the plotting library.**

---

## What Vizdantic Does

* Provides **Pydantic schemas** for common visualization types
* Validates LLM-generated visualization intent
* Is **library-agnostic** by design
* Renders charts via optional plugins (e.g. Plotly)

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

### Render with Plotly

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

```python

render(spec, data)

```

function.

---

## Status

* **Version:** 0.1.0
* **Stability:** Experimental
* **Breaking changes:** Possible until 1.0

Vizdantic is under active development and feedback is welcome.
