from .adapter import AnyVizSpec


def schema() -> dict:
    """
    Return the JSON Schema describing all supported visualization specifications.

    This is intended for LLM prompting / tool calling.

    Returns
    -------
    dict
        JSON Schema dictionary describing all supported visualization specifications.
    """
    return AnyVizSpec.model_json_schema()
