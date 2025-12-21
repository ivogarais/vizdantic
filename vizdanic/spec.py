from typing import Union, Annotated
from pydantic import Field, TypeAdapter

from .viz import (
    XYSpec,
    PointsSpec,
    DistributionSpec,
    PartsSpec,
    MatrixSpec,
    FlowSpec,
    HierarchySpec,
    GeoSpec,
)

# Discriminated union over all supported visualization specs
VizSpec = Annotated[
    Union[
        XYSpec,
        PointsSpec,
        DistributionSpec,
        PartsSpec,
        MatrixSpec,
        FlowSpec,
        HierarchySpec,
        GeoSpec,
    ],
    Field(discriminator="kind"),
]

VIZ_SPEC_ADAPTER = TypeAdapter(VizSpec)
