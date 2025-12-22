from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class VizSpec(BaseModel):
    chart: str
    title: Optional[str] = None
    legend_title: Optional[str] = None


class XYSpec(VizSpec):
    kind: Literal["xy"] = Field("xy")

    x: str
    y: str

    series: Optional[str] = None
    facet: Optional[str] = None


class PointsSpec(VizSpec):
    kind: Literal["points"] = Field("points")

    x: str
    y: str

    series: Optional[str] = None
    size: Optional[str] = None


class DistributionSpec(VizSpec):
    kind: Literal["distribution"] = Field("distribution")

    value: str
    category: Optional[str] = None


class PartsSpec(VizSpec):
    kind: Literal["parts"] = Field("parts")

    label: str
    value: str


class MatrixSpec(VizSpec):
    kind: Literal["matrix"] = Field("matrix")

    x: str
    y: str
    value: str


class FlowSpec(VizSpec):
    kind: Literal["flow"] = Field("flow")

    source: str
    target: str
    value: Optional[str] = None


class HierarchySpec(VizSpec):
    kind: Literal["hierarchy"] = Field("hierarchy")

    path: List[str]
    value: Optional[str] = None


class GeoSpec(VizSpec):
    kind: Literal["geo"] = Field("geo")

    location: Optional[str] = None
    lat: Optional[str] = None
    lon: Optional[str] = None
    value: Optional[str] = None
