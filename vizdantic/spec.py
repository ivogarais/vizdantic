from typing import Optional, Literal, List
from pydantic import BaseModel, Field


Backend = Literal["plotly", "seaborn", "matplotlib", "altair", "vega_lite", "any"]

CartesianChart = Literal["bar", "line", "area", "scatter"]
PointsChart = Literal["scatter"]
DistributionChart = Literal["histogram", "box", "violin", "strip"]
PartsChart = Literal["pie"]
MatrixChart = Literal["density_heatmap", "imshow"]
FlowChart = Literal["sankey"]
HierarchyChart = Literal["treemap", "sunburst", "icicle"]
GeoChart = Literal["scatter_geo", "line_geo", "choropleth", "scatter_mapbox", "choropleth_mapbox"]
PolarChart = Literal["scatter_polar", "line_polar", "bar_polar"]
TernaryChart = Literal["scatter_ternary", "line_ternary"]
ThreeDChart = Literal["scatter_3d", "line_3d"]
FinancialChart = Literal["funnel", "funnel_area"]
ParallelChart = Literal["parallel_coordinates", "parallel_categories"]
TimelineChart = Literal["timeline"]


class VizSpec(BaseModel):
    """
    Base visualization specification.

    Represents validated visualization intent produced by an upstream system (often an LLM),
    but this library itself does not do any LLM work.
    """

    title: Optional[str] = Field(default=None, description="Semantic title for the visualization.")
    legend_title: Optional[str] = Field(default=None, description="Semantic title for the legend.")
    backend: Optional[Backend] = Field(
        default=None,
        description="Optional preferred backend. Pure metadata; does not affect validation.",
    )


class CartesianSpec(VizSpec):
    """
    Cartesian (x–y) visualization.
    """

    kind: Literal["cartesian"] = Field(
        "cartesian", description="Cartesian coordinate visualization."
    )
    chart: CartesianChart = Field(description="Cartesian chart type.")

    x: str = Field(description="Column mapped to the x-axis.")
    y: str = Field(description="Column mapped to the y-axis.")

    series: Optional[str] = Field(
        default=None, description="Column used to group or color series."
    )
    facet: Optional[str] = Field(
        default=None, description="Column used to split the chart into facets."
    )


class PointsSpec(VizSpec):
    """
    Point-based visualization.
    """

    kind: Literal["points"] = Field("points", description="Point-based visualization.")
    chart: PointsChart = Field(description="Points chart type.")

    x: str = Field(description="Column mapped to the x-axis.")
    y: str = Field(description="Column mapped to the y-axis.")

    series: Optional[str] = Field(
        default=None, description="Column used to group or color points."
    )
    size: Optional[str] = Field(default=None, description="Column controlling point size.")


class DistributionSpec(VizSpec):
    """
    Distribution visualization.
    """

    kind: Literal["distribution"] = Field(
        "distribution", description="Distribution-based visualization."
    )
    chart: DistributionChart = Field(description="Distribution chart type.")

    value: str = Field(description="Column containing values to distribute.")
    category: Optional[str] = Field(default=None, description="Optional grouping column.")


class PartsSpec(VizSpec):
    """
    Part-to-whole visualization.
    """

    kind: Literal["parts"] = Field("parts", description="Part-to-whole visualization.")
    chart: PartsChart = Field(description="Parts chart type.")

    label: str = Field(description="Column defining part labels.")
    value: str = Field(description="Column defining part values.")


class MatrixSpec(VizSpec):
    """
    Matrix or grid-based visualization.
    """

    kind: Literal["matrix"] = Field("matrix", description="Matrix or grid visualization.")
    chart: MatrixChart = Field(description="Matrix chart type.")

    x: str = Field(description="Column mapped to the x-axis.")
    y: str = Field(description="Column mapped to the y-axis.")
    value: str = Field(description="Column mapped to cell values.")


class FlowSpec(VizSpec):
    """
    Flow or relationship visualization.
    """

    kind: Literal["flow"] = Field("flow", description="Flow-based visualization.")
    chart: FlowChart = Field(description="Flow chart type.")

    source: str = Field(description="Source node column.")
    target: str = Field(description="Target node column.")
    value: Optional[str] = Field(
        default=None, description="Optional column controlling flow magnitude."
    )


class HierarchySpec(VizSpec):
    """
    Hierarchical visualization.
    """

    kind: Literal["hierarchy"] = Field("hierarchy", description="Hierarchical visualization.")
    chart: HierarchyChart = Field(description="Hierarchy chart type.")

    path: List[str] = Field(description="Ordered list of columns defining hierarchy levels.")
    value: Optional[str] = Field(default=None, description="Optional column defining node values.")


class GeoSpec(VizSpec):
    """
    Geographic visualization.
    """

    kind: Literal["geo"] = Field("geo", description="Geographic visualization.")
    chart: GeoChart = Field(description="Geographic chart type.")

    location: Optional[str] = Field(
        default=None, description="Location or region identifier column."
    )
    lat: Optional[str] = Field(default=None, description="Latitude column.")
    lon: Optional[str] = Field(default=None, description="Longitude column.")
    value: Optional[str] = Field(default=None, description="Column used for color or magnitude.")


class PolarSpec(VizSpec):
    """
    Polar coordinate visualization.
    """

    kind: Literal["polar"] = Field("polar", description="Polar coordinate visualization.")
    chart: PolarChart = Field(description="Polar chart type.")

    r: str = Field(description="Column mapped to the radial axis.")
    theta: str = Field(description="Column mapped to the angular axis.")
    series: Optional[str] = Field(
        default=None, description="Column used to group or color series."
    )


class TernarySpec(VizSpec):
    """
    Ternary coordinate visualization.
    """

    kind: Literal["ternary"] = Field("ternary", description="Ternary coordinate visualization.")
    chart: TernaryChart = Field(description="Ternary chart type.")

    a: str = Field(description="Column mapped to the first ternary axis.")
    b: str = Field(description="Column mapped to the second ternary axis.")
    c: str = Field(description="Column mapped to the third ternary axis.")
    series: Optional[str] = Field(
        default=None, description="Column used to group or color series."
    )
    size: Optional[str] = Field(default=None, description="Column controlling point size.")


class ThreeDSpec(VizSpec):
    """
    3D coordinate visualization.
    """

    kind: Literal["3d"] = Field("3d", description="3D coordinate visualization.")
    chart: ThreeDChart = Field(description="3D chart type.")

    x: str = Field(description="Column mapped to the x-axis.")
    y: str = Field(description="Column mapped to the y-axis.")
    z: str = Field(description="Column mapped to the z-axis.")
    series: Optional[str] = Field(
        default=None, description="Column used to group or color series."
    )
    size: Optional[str] = Field(default=None, description="Column controlling point size.")


class FinancialSpec(VizSpec):
    """
    Financial visualization (funnel, waterfall).
    """

    kind: Literal["financial"] = Field("financial", description="Financial visualization.")
    chart: FinancialChart = Field(description="Financial chart type.")

    x: Optional[str] = Field(default=None, description="Column mapped to the x-axis.")
    y: Optional[str] = Field(default=None, description="Column mapped to the y-axis.")
    value: Optional[str] = Field(default=None, description="Column containing values.")
    label: Optional[str] = Field(default=None, description="Column defining labels.")


class ParallelSpec(VizSpec):
    """
    Parallel coordinates or categories visualization.
    """

    kind: Literal["parallel"] = Field(
        "parallel", description="Parallel coordinates visualization."
    )
    chart: ParallelChart = Field(description="Parallel chart type.")

    dimensions: List[str] = Field(description="List of columns to display as parallel dimensions.")
    color: Optional[str] = Field(default=None, description="Column used for coloring.")


class TimelineSpec(VizSpec):
    """
    Timeline or Gantt chart visualization.
    """

    kind: Literal["timeline"] = Field("timeline", description="Timeline visualization.")
    chart: TimelineChart = Field(description="Timeline chart type.")

    x_start: str = Field(description="Column containing start times/dates.")
    x_end: str = Field(description="Column containing end times/dates.")
    y: str = Field(description="Column mapped to the y-axis (task names).")
    series: Optional[str] = Field(
        default=None, description="Column used to group or color series."
    )
