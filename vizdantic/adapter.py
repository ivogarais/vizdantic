from typing import Union, Annotated
from pydantic import Field, TypeAdapter

from .spec import (
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

AnyVizSpec = Annotated[
    Union[
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
    ],
    Field(discriminator="kind"),
]

VIZ_SPEC_ADAPTER = TypeAdapter(AnyVizSpec)
