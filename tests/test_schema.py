from vizdantic.schema import schema


def test_schema_uses_kind_discriminator():
    data = schema()
    assert data["discriminator"]["propertyName"] == "kind"
    mapping = data["discriminator"]["mapping"]
    expected = {
        "cartesian",
        "points",
        "distribution",
        "parts",
        "matrix",
        "flow",
        "hierarchy",
        "geo",
        "polar",
        "ternary",
        "3d",
        "financial",
        "parallel",
        "timeline",
    }
    assert expected.issubset(set(mapping))
