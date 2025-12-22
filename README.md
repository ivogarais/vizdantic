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

<pre class="overflow-visible! px-0!" data-start="1585" data-end="1794"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="@w-xl/main:top-9 sticky top-[calc(--spacing(9)+var(--header-height))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> vizdantic </span><span>import</span><span> validate

llm_output = {
    </span><span>"kind"</span><span>: </span><span>"cartesian"</span><span>,
    </span><span>"chart"</span><span>: </span><span>"bar"</span><span>,
    </span><span>"x"</span><span>: </span><span>"category"</span><span>,
    </span><span>"y"</span><span>: </span><span>"value"</span><span>,
    </span><span>"title"</span><span>: </span><span>"Sales by Category"</span><span>,
}

spec = validate(llm_output)
</span></span></code></div></div></pre>

### Render with Plotly Example

<pre class="overflow-visible! px-0!" data-start="1820" data-end="2016"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="@w-xl/main:top-9 sticky top-[calc(--spacing(9)+var(--header-height))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> vizdantic.plugins.plotly </span><span>import</span><span> render
</span><span>import</span><span> pandas </span><span>as</span><span> pd

df = pd.DataFrame({
    </span><span>"category"</span><span>: [</span><span>"A"</span><span>, </span><span>"B"</span><span>, </span><span>"C"</span><span>],
    </span><span>"value"</span><span>: [</span><span>10</span><span>, </span><span>20</span><span>, </span><span>15</span><span>],
})

fig = render(spec, df)
fig.show()
</span></span></code></div></div></pre>

---

## Using Vizdantic with LLMs

Vizdantic works with **any LLM** and supports  **two common integration patterns** .

| Prompt-based (Universal)                                               | Tool / Function Calling (Structured)                                            |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Use when your LLM does**not** support tools or function calling. | Use when your LLM**supports JSON schema tools**(OpenAI, Anthropic, etc.). |
| You embed the schema directly in the prompt.                           | You pass the schema as a tool input contract.                                   |

### Prompt-based integration

<pre class="overflow-visible! px-0!" data-start="2549" data-end="2837"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="@w-xl/main:top-9 sticky top-[calc(--spacing(9)+var(--header-height))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-text"><span><span>You are an assistant that creates visualization specifications.

Return JSON that strictly conforms to the following schema:

<SCHEMA>
{{ vizdantic.schema() }}
</SCHEMA>

Rules:
- Return JSON only
- Choose the most appropriate chart type
- Use column names exactly as provided
</span></span></code></div></div></pre>

Example model output:

<pre class="overflow-visible! px-0!" data-start="2862" data-end="2984"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="@w-xl/main:top-9 sticky top-[calc(--spacing(9)+var(--header-height))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>{</span><span>
  </span><span>"kind"</span><span>:</span><span></span><span>"cartesian"</span><span>,</span><span>
  </span><span>"chart"</span><span>:</span><span></span><span>"bar"</span><span>,</span><span>
  </span><span>"x"</span><span>:</span><span></span><span>"category"</span><span>,</span><span>
  </span><span>"y"</span><span>:</span><span></span><span>"value"</span><span>,</span><span>
  </span><span>"title"</span><span>:</span><span></span><span>"Sales by Category"</span><span>
</span><span>}</span><span>
</span></span></code></div></div></pre>

---

### Tool / function calling integration

<pre class="overflow-visible! px-0!" data-start="3032" data-end="3191"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="@w-xl/main:top-9 sticky top-[calc(--spacing(9)+var(--header-height))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>tool = {
    </span><span>"name"</span><span>: </span><span>"create_visualization"</span><span>,
    </span><span>"description"</span><span>: </span><span>"Create a visualization specification"</span><span>,
    </span><span>"input_schema"</span><span>: vizdantic.schema(),
}
</span></span></code></div></div></pre>

The LLM is now constrained to  **valid Vizdantic output only** .

---

## Validate and Render

Once the LLM returns JSON, the workflow is the same:

<pre class="overflow-visible! px-0!" data-start="3340" data-end="3491"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="@w-xl/main:top-9 sticky top-[calc(--spacing(9)+var(--header-height))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> vizdantic </span><span>import</span><span> validate
</span><span>from</span><span> vizdantic.plugins.plotly </span><span>import</span><span> render

spec = validate(llm_output)
fig = render(spec, df)
fig.show()
</span></span></code></div></div></pre>

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
