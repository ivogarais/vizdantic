from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class VizSpec(BaseModel):
    """
    Base visualization specification.

    Represents validated visualization intent produced by an LLM.
    """

    chart: str = Field(description="Chart type to render (e.g. bar, line, scatter, pie).")
    title: Optional[str] = Field(default=None, description="Semantic title for the visualization.")
    legend_title: Optional[str] = Field(default=None, description="Semantic title for the legend.")


class CartesianSpec(VizSpec):
    """
    Cartesian (x–y) visualization.
    """

    kind: Literal["cartesian"] = Field(
        "cartesian", description="Cartesian coordinate visualization."
    )

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

    value: str = Field(description="Column containing values to distribute.")
    category: Optional[str] = Field(default=None, description="Optional grouping column.")


class PartsSpec(VizSpec):
    """
    Part-to-whole visualization.
    """

    kind: Literal["parts"] = Field("parts", description="Part-to-whole visualization.")

    label: str = Field(description="Column defining part labels.")
    value: str = Field(description="Column defining part values.")


class MatrixSpec(VizSpec):
    """
    Matrix or grid-based visualization.
    """

    kind: Literal["matrix"] = Field("matrix", description="Matrix or grid visualization.")

    x: str = Field(description="Column mapped to the x-axis.")
    y: str = Field(description="Column mapped to the y-axis.")
    value: str = Field(description="Column mapped to cell values.")


class FlowSpec(VizSpec):
    """
    Flow or relationship visualization.
    """

    kind: Literal["flow"] = Field("flow", description="Flow-based visualization.")

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

    path: List[str] = Field(description="Ordered list of columns defining hierarchy levels.")
    value: Optional[str] = Field(default=None, description="Optional column defining node values.")


class GeoSpec(VizSpec):
    """
    Geographic visualization.
    """

    kind: Literal["geo"] = Field("geo", description="Geographic visualization.")

    location: Optional[str] = Field(
        default=None, description="Location or region identifier column."
    )
    lat: Optional[str] = Field(default=None, description="Latitude column.")
    lon: Optional[str] = Field(default=None, description="Longitude column.")
    value: Optional[str] = Field(default=None, description="Column used for color or magnitude.")
