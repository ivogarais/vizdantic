from .adapter import VIZ_SPEC_ADAPTER


def validate(data):
    """
    Validate LLM-generated visualization intent.

    Parameters
    ----------
    data : dict
        Untrusted output from an LLM.

    Returns
    -------
    VizSpec
        A concrete visualization spec (CartesianSpec, PointsSpec, etc.).

    Raises
    ------
    ValidationError
        If the input does not match any supported Vizdantic schema.
    """
    return VIZ_SPEC_ADAPTER.validate_python(data)
