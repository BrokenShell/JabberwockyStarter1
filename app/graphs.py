import altair as alt
from pandas import DataFrame


def visualizer(df: DataFrame, x_axis: str, y_axis: str, target: str, name: str):

    text_color = "#AAAAAA"
    graph_color = "#333333"
    graph_bg = "#252525"

    if name == "All Monsters":
        title = name
        data = df
    else:
        title = f"{name}s"
        data = df[df['name'] == name]

    x_axis = x_axis.title()
    y_axis = y_axis.title()
    target = target.title()
    data.columns = map(lambda s: s.title(), df.columns)

    graph = alt.Chart(
        data,
        title=title,
    ).mark_circle(size=100).encode(
        x=alt.X(x_axis, axis=alt.Axis(title=x_axis.title())),
        y=alt.Y(y_axis, axis=alt.Axis(title=y_axis.title())),
        color=target,
        tooltip=alt.Tooltip(list(data.columns)),
    ).properties(
        width=400,
        height=440,
        background=graph_bg,
        padding=40,
    ).configure(
        legend={
            "titleColor": text_color,
            "labelColor": text_color,
            "padding": 10,
        },
        title={
            "color": text_color,
            "fontSize": 26,
            "offset": 30,
        },
        axis={
            "titlePadding": 20,
            "titleColor": text_color,
            "labelPadding": 5,
            "labelColor": text_color,
            "gridColor": graph_color,
            "tickColor": graph_color,
            "tickSize": 10,
        },
        view={
            "stroke": graph_color,
        },
    )
    return graph.to_json()
