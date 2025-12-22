def render(spec, data, lib, bindings):
    """
    Generic render helper.

    Parameters
    ----------
    spec : VizSpec
        Validated visualization intent
    data : Any
        User data (DataFrame, array, etc.)
    lib : module
        Plotting library (e.g. plotly.express, altair)
    bindings : dict[type, callable]
        Mapping of VizSpec type -> render function
    """
    for spec_type, fn in bindings.items():
        if isinstance(spec, spec_type):
            return fn(lib, spec, data)

    raise TypeError(f"No renderer registered for {type(spec).__name__}")
