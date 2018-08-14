import altair as alt
import numpy as np
from .common import to_dataframe
from .docstrings import make_docstring, Docstring as D


def qqplot(data, x, y, mark={}, encoding={}, properties={}):
    """See below."""
    data = to_dataframe(data)
    n = data.shape[0]
    data = data.quantile(np.arange(0, 1, step=10 / n))
    return alt.Chart(data).mark_point(**mark).encode(
        x=x, y=y, **encoding).properties(**properties)


qqplot.__doc__ = make_docstring(
    summary="Generate a quantile-quantile plot.",
    params=[D.data, D.x, D.y, D.mark, D.encoding, D.properties])
