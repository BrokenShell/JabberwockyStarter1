import altair as alt


def visualizer(df, x_axis, y_axis, target, name):

    text_color = "#AAAAAA"
    graph_color = "#333333"
    graph_bg = "#252525"

    if name != "All Monsters":
        title = f"{name}s"
        data = df[df['name'] == name]
    else:
        title = name
        data = df

    graph = alt.Chart(
        data,
        title=title,
    ).mark_circle(size=100).encode(
        x=alt.X(x_axis, axis=alt.Axis(title=x_axis)),
        y=alt.Y(y_axis, axis=alt.Axis(title=y_axis)),
        color=target,
        tooltip=alt.Tooltip(list(df.columns)),
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
