from typing import Optional, Literal
from pydantic import BaseModel, Field


class ChartSpec(BaseModel):
    chart: str
    title: Optional[str] = None
    legend_title: Optional[str] = None


class XYSpec(ChartSpec):
    kind: Literal["xy"] = Field("xy")
    x: str
    y: str
    series: Optional[str] = None


class PointSpec(ChartSpec):
    kind: Literal["points"] = Field("points")
    x: str
    y: str
    series: Optional[str] = None

class PartsSpec(ChartSpec):
    kind: Literal["parts"] = Field("parts")
    x: str
    y: str
    series: Optional[str] = None
