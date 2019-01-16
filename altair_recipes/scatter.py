"""Scatter plots."""
from .common import choose_kwargs, constant_cl_hcl_scale
from .signatures import bivariate_recipe, multivariate_recipe, color, tooltip
import altair as alt
from autosig import autosig, Signature, param
from numbers import Number


scatter_sig = Signature(
    color=color(default=None, position=3),
    opacity=param(
        default=1,
        position=4,
        converter=float,
        docstring="""`float`
A constant value for the opacity of the mark""",
    ),
    tooltip=tooltip(default=None, position=5),
)


@autosig(bivariate_recipe + scatter_sig)
def scatter(data, x=0, y=1, color=None, opacity=1, tooltip=None, height=600, width=800):
    """Generate a scatter plot."""
    if opacity < 1 and color is not None and isinstance(data[color][0], Number):
        color = alt.Color(color, scale=constant_cl_hcl_scale)
    kwargs = choose_kwargs(from_=locals(), which=["color", "tooltip"])
    return alt.Chart(
        data,
        height=height,
        width=width,
        mark=alt.MarkDef(type="point" if opacity == 1 else "circle", opacity=opacity),
    ).encode(x=x, y=y, **kwargs)


@autosig(multivariate_recipe + scatter_sig)
def multiscatter(
    data,
    columns=None,
    group_by=None,
    color=None,
    opacity=1,
    tooltip=None,
    height=600,
    width=800,
):
    """Generate many scatter plots.

    Based on several columns, pairwise.
    """
    kwargs = choose_kwargs(from_=locals(), which=["color", "tooltip"])

    assert group_by is None, "Long format not supported yet"
    return (
        alt.Chart(data, height=height / len(columns), width=width / len(columns))
        .mark_point(size=1 / len(columns), opacity=opacity)
        .encode(
            alt.X(alt.repeat("column"), type="quantitative"),
            alt.Y(alt.repeat("row"), type="quantitative"),
            **kwargs
        )
        .repeat(row=columns, column=columns)
    )
