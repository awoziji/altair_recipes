"""Boxplot implementation."""
from .common import multivariate_preprocess, ndistinct
from .signatures import multivariate_recipe
import altair as alt
from autosig import autosig, Signature, param


@autosig(
    multivariate_recipe
    + Signature(
        color=param(
            default=False,
            converter=bool,
            docstring="""bool
Whether to color the interquartile bars accoding to the x dimension""",
            position=3,
        )
    )
)
def boxplot(data, columns=None, group_by=None, color=False, height=600, width=800):
    """Generate a boxplot."""
    data, key, value = multivariate_preprocess(data, columns, group_by)
    # long form assumed from here
    chart = alt.Chart(
        height=height,
        width=width
        // (
            ndistinct(data, key) if color is not None else 1
        ),  # TODO: use col_cardinality instead
    )
    chart_bar = chart.mark_bar(stroke="black", fill="#4682b4")
    chart_tick = chart.mark_tick()
    encode_args = dict(x=key + ":N")
    min_value = "min(" + value + ")"
    max_value = "max(" + value + ")"
    median_value = "median(" + value + ")"
    min_tick = chart_tick.encode(y=min_value, **encode_args)
    max_tick = chart_tick.encode(y=max_value, **encode_args)
    q1 = "q1(" + value + ")"
    q3 = "q3(" + value + ")"
    if color:
        encode_args["color"] = key
    q1_bar = chart_bar.encode(y=q1, y2=median_value, **encode_args)
    q3_bar = chart_bar.encode(y=median_value, y2=q3, **encode_args)

    rule = chart.mark_rule().encode(
        y=alt.Y(min_value, axis=alt.Axis(title=value)), y2=max_value, **encode_args
    )
    return (rule + min_tick + max_tick + q1_bar + q3_bar).properties(data=data)
