from typing import Any

try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError as e:
    raise ImportError(
        "Vizdantic Plotly plugin requires plotly.\n"
        "Install it with: pip install vizdantic[plotly]"
    ) from e

from ..spec import (
    VizSpec,
    CartesianSpec,
    PointsSpec,
    DistributionSpec,
    PartsSpec,
    MatrixSpec,
    FlowSpec,
    HierarchySpec,
    GeoSpec,
    PolarSpec,
    TernarySpec,
    ThreeDSpec,
    FinancialSpec,
    ParallelSpec,
    TimelineSpec,
)


def render(spec: VizSpec, data: Any) -> go.Figure:
    """
    Render a Vizdantic visualization specification using Plotly.

    Parameters
    ----------
    spec : VizSpec
        A validated Vizdantic visualization specification, typically
        produced by an LLM and validated via ``vizdantic.validate``.
    data : Any
        User-provided dataset. This is typically a pandas DataFrame,
        but any Plotly-compatible data structure is accepted.

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly figure corresponding to the visualization specification.

    Raises
    ------
    NotImplementedError
        If the provided spec type is not supported by the Plotly plugin.
    """

    # Cartesian & point-based charts
    if isinstance(spec, (CartesianSpec, PointsSpec)):
        fig = getattr(px, spec.chart)(
            data,
            x=spec.x,
            y=spec.y,
            color=spec.series,
            title=spec.title,
        )

    # Distribution charts
    elif isinstance(spec, DistributionSpec):
        fig = getattr(px, spec.chart)(
            data,
            x=spec.value,
            color=spec.category,
            title=spec.title,
        )

    # Part-to-whole charts
    elif isinstance(spec, PartsSpec):
        fig = px.pie(
            data,
            names=spec.label,
            values=spec.value,
            title=spec.title,
        )

    # Matrix / heatmap charts
    elif isinstance(spec, MatrixSpec):
        fig = px.density_heatmap(
            data,
            x=spec.x,
            y=spec.y,
            z=spec.value,
            title=spec.title,
        )

    # Flow charts (Sankey)
    elif isinstance(spec, FlowSpec):
        # Build unique node list
        nodes = list(dict.fromkeys(list(data[spec.source]) + list(data[spec.target])))
        node_index = {label: i for i, label in enumerate(nodes)}

        fig = go.Figure(
            go.Sankey(
                node=dict(label=nodes),
                link=dict(
                    source=[node_index[v] for v in data[spec.source]],
                    target=[node_index[v] for v in data[spec.target]],
                    value=(data[spec.value] if spec.value else [1] * len(data)),
                ),
            )
        )

        if spec.title:
            fig.update_layout(title=spec.title)

    # Hierarchical charts
    elif isinstance(spec, HierarchySpec):
        fig = getattr(px, spec.chart)(
            data,
            path=spec.path,
            values=spec.value,
            title=spec.title,
        )

    # Geographic charts
    elif isinstance(spec, GeoSpec):
        fig = getattr(px, spec.chart)(
            data,
            locations=spec.location,
            lat=spec.lat,
            lon=spec.lon,
            color=spec.value,
            title=spec.title,
        )

    # Polar charts
    elif isinstance(spec, PolarSpec):
        fig = getattr(px, spec.chart)(
            data,
            r=spec.r,
            theta=spec.theta,
            color=spec.series,
            title=spec.title,
        )

    # Ternary charts
    elif isinstance(spec, TernarySpec):
        fig = getattr(px, spec.chart)(
            data,
            a=spec.a,
            b=spec.b,
            c=spec.c,
            color=spec.series,
            size=spec.size,
            title=spec.title,
        )

    # 3D charts
    elif isinstance(spec, ThreeDSpec):
        fig = getattr(px, spec.chart)(
            data,
            x=spec.x,
            y=spec.y,
            z=spec.z,
            color=spec.series,
            size=spec.size,
            title=spec.title,
        )

    # Financial charts
    elif isinstance(spec, FinancialSpec):
        # Funnel charts use x and y directly
        fig = getattr(px, spec.chart)(
            data,
            x=spec.x,
            y=spec.y,
            title=spec.title,
        )

    # Parallel coordinates/categories
    elif isinstance(spec, ParallelSpec):
        fig = getattr(px, spec.chart)(
            data,
            dimensions=spec.dimensions,
            color=spec.color,
            title=spec.title,
        )

    # Timeline/Gantt charts
    elif isinstance(spec, TimelineSpec):
        fig = px.timeline(
            data,
            x_start=spec.x_start,
            x_end=spec.x_end,
            y=spec.y,
            color=spec.series,
            title=spec.title,
        )

    else:
        raise NotImplementedError(
            f"Plotly plugin does not support spec type: {type(spec).__name__}"
        )

    if spec.legend_title:
        fig.update_layout(legend_title_text=spec.legend_title)

    return fig
