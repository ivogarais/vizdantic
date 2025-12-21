from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field

from .enums import (
    XYChart,
    PointsChart,
    DistributionChart,
    PartsChart,
    MatrixChart,
    FlowChart,
    HierarchyChart,
    GeoChart,
)


class ChartSpec(BaseModel):

    chart: Enum
    title: Optional[str] = None
    legend_title: Optional[str] = None


class XYSpec(ChartSpec):
    kind: Literal["xy"] = Field("xy")
    chart: XYChart

    x: str
    y: str
    series: Optional[str] = None


class PointsSpec(ChartSpec):
    kind: Literal["points"] = Field("points")
    chart: PointsChart

    x: str
    y: str
    series: Optional[str] = None


class DistributionSpec(ChartSpec):
    kind: Literal["distribution"] = Field("distribution")
    chart: DistributionChart

    value: str
    category: Optional[str] = None


class PartsSpec(ChartSpec):
    kind: Literal["parts"] = Field("parts")
    chart: PartsChart

    label: str
    value: str


class MatrixSpec(ChartSpec):
    kind: Literal["matrix"] = Field("matrix")
    chart: MatrixChart

    x: str
    y: str
    value: str


class FlowSpec(ChartSpec):
    kind: Literal["flow"] = Field("flow")
    chart: FlowChart

    source: str
    target: str
    value: str


class HierarchySpec(ChartSpec):
    kind: Literal["hierarchy"] = Field("hierarchy")
    chart: HierarchyChart

    path: list[str]
    value: str


class GeoSpec(ChartSpec):
    kind: Literal["geo"] = Field("geo")
    chart: GeoChart

    location: str
    value: Optional[str] = None
