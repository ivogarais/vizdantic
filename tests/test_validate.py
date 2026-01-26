import pytest
from pydantic import ValidationError

from vizdantic import (
    validate,
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


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        (
            {"kind": "cartesian", "chart": "line", "x": "x", "y": "y", "series": "group"},
            CartesianSpec,
        ),
        (
            {"kind": "points", "chart": "scatter", "x": "x", "y": "y"},
            PointsSpec,
        ),
        (
            {"kind": "distribution", "chart": "histogram", "value": "value"},
            DistributionSpec,
        ),
        (
            {"kind": "parts", "chart": "pie", "label": "label", "value": "value"},
            PartsSpec,
        ),
        (
            {"kind": "matrix", "chart": "density_heatmap", "x": "x", "y": "y", "value": "value"},
            MatrixSpec,
        ),
        (
            {"kind": "flow", "chart": "sankey", "source": "source", "target": "target"},
            FlowSpec,
        ),
        (
            {"kind": "hierarchy", "chart": "treemap", "path": ["continent", "country"]},
            HierarchySpec,
        ),
        (
            {"kind": "geo", "chart": "scatter_geo", "location": "country"},
            GeoSpec,
        ),
        (
            {"kind": "polar", "chart": "scatter_polar", "r": "radius", "theta": "angle"},
            PolarSpec,
        ),
        (
            {"kind": "ternary", "chart": "scatter_ternary", "a": "a", "b": "b", "c": "c"},
            TernarySpec,
        ),
        (
            {"kind": "3d", "chart": "scatter_3d", "x": "x", "y": "y", "z": "z"},
            ThreeDSpec,
        ),
        (
            {"kind": "financial", "chart": "funnel", "x": "stage", "y": "value"},
            FinancialSpec,
        ),
        (
            {"kind": "parallel", "chart": "parallel_coordinates", "dimensions": ["a", "b", "c"]},
            ParallelSpec,
        ),
        (
            {
                "kind": "timeline",
                "chart": "timeline",
                "x_start": "start",
                "x_end": "end",
                "y": "task",
            },
            TimelineSpec,
        ),
    ],
)
def test_validate_returns_concrete_spec(payload, expected_type):
    result = validate(payload)
    assert isinstance(result, expected_type)
    assert result.kind == payload["kind"]
    assert result.chart == payload["chart"]


def test_validate_rejects_unknown_kind():
    with pytest.raises(ValidationError):
        validate({"kind": "unknown", "chart": "bar"})


def test_validate_requires_chart():
    with pytest.raises(ValidationError):
        validate({"kind": "cartesian", "x": "x", "y": "y"})
