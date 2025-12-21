from enum import Enum


class XYChart(str, Enum):
    bar = "bar"
    line = "line"
    area = "area"


class PointsChart(str, Enum):
    scatter = "scatter"


class DistributionChart(str, Enum):
    histogram = "histogram"
    box = "box"
    violin = "violin"


class PartsChart(str, Enum):
    pie = "pie"


class MatrixChart(str, Enum):
    heatmap = "heatmap"


class FlowChart(str, Enum):
    sankey = "sankey"


class HierarchyChart(str, Enum):
    treemap = "treemap"
    sunburst = "sunburst"


class GeoChart(str, Enum):
    choropleth = "choropleth"
    scatter = "scatter"
