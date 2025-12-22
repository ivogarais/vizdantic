from typing import Any

try:
    import plotly.express as px
except ImportError as e:
    raise ImportError(
        "Vizdantic Plotly plugin requires plotly.\n"
        "Install it with: pip install vizdantic[plotly]"
    ) from e

from viz import (
    CartesianSpec,
    PointsSpec,
    DistributionSpec,
    PartsSpec,
    MatrixSpec,
    FlowSpec,
    HierarchySpec,
    GeoSpec,
)


def render(spec: Any, data):
    """
    Render a Vizdantic visualization spec using Plotly.

    Parameters
    ----------
    spec
        A validated Vizdantic spec (output of vizdantic.validate).
    data
        User-provided dataset (DataFrame-like).

    Returns
    -------
    plotly.graph_objects.Figure
    """

    if isinstance(spec, (CartesianSpec, PointsSpec)):
        fig = getattr(px, spec.chart)(
            data,
            x=spec.x,
            y=spec.y,
            color=spec.series,
            title=spec.title,
        )

    elif isinstance(spec, DistributionSpec):
        fig = getattr(px, spec.chart)(
            data,
            x=spec.value,
            color=spec.category,
            title=spec.title,
        )

    elif isinstance(spec, PartsSpec):
        fig = px.pie(
            data,
            names=spec.label,
            values=spec.value,
            title=spec.title,
        )

    elif isinstance(spec, MatrixSpec):
        fig = px.density_heatmap(
            data,
            x=spec.x,
            y=spec.y,
            z=spec.value,
            title=spec.title,
        )

    elif isinstance(spec, FlowSpec):
        fig = px.sankey(
            data,
            source=spec.source,
            target=spec.target,
            value=spec.value,
            title=spec.title,
        )

    elif isinstance(spec, HierarchySpec):
        fig = getattr(px, spec.chart)(
            data,
            path=spec.path,
            values=spec.value,
            title=spec.title,
        )

    elif isinstance(spec, GeoSpec):
        fig = getattr(px, spec.chart)(
            data,
            locations=spec.location,
            lat=spec.lat,
            lon=spec.lon,
            color=spec.value,
            title=spec.title,
        )

    else:
        raise NotImplementedError(
            f"Plotly plugin does not support spec type: {type(spec).__name__}"
        )

    if spec.legend_title:
        fig.update_layout(legend_title_text=spec.legend_title)

    return fig
