"""
Shows how to animate a graph using preset positions that are modified by a callback
"""
import dash
from dash import Input, Output, html, callback
import dash_cytoscape as cyto


app = dash.Dash(__name__)

nodes = [
    {
        "data": {"id": short, "label": label},
        "position": {"x": 20 * lat, "y": -20 * longitude},
    }
    for short, label, longitude, lat in (
        ("la", "Los Angeles", 34.03, -118.25),
        ("nyc", "New York", 40.71, -74),
    )
]

edges = [
    {"data": {"source": source, "target": target}}
    for source, target in (("la", "nyc"),)
]

elements = nodes + edges

default_stylesheet = [
    {
        "selector": "node",
        "style": {"background-color": "BFD7B5", "label": "data(label)"},
    },
    {"selector": "edge", "style": {"line-color": "#A3C4BC"}},
]

app.layout = html.Div(
    [
        html.Div(html.Button("Change elements", id="button")),
        cyto.Cytoscape(
            id="cytoscape-elements-callbacks",
            layout={"name": "preset", "animate": True, "animationDuration": 1000},
            autoRefreshLayout=True,
            stylesheet=default_stylesheet,
            style={"width": "100%", "height": "450px"},
            elements=elements,
        ),
    ]
)


@callback(Output("cytoscape-elements-callbacks", "layout"), Input("button", "n_clicks"))
def update_elements(n_clicks):
    if not n_clicks:
        n_clicks = 0

    layout = {
        "name": "preset",
        "animate": True,
        "animationDuration": 1000,
        "positions": {
            node_id: {"x": 20 * lat, "y": -20 * longitude}
            for node_id, longitude, lat in (
                ("la", 34.03, -118.25 + 10 * n_clicks),
                ("nyc", 40.71, -74),
            )
        },
    }

    return layout


if __name__ == "__main__":
    app.run(debug=False)
