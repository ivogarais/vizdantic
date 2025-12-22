from .adapter import VIZ_SPEC_ADAPTER

def schema() -> dict:
    """
    Return the JSON Schema for all Vizdantic visualization specs.

    Returns
    -------
    dict
        The JSON Schema for all Vizdantic visualization specs.
    """
    return VIZ_SPEC_ADAPTER.json_schema()
