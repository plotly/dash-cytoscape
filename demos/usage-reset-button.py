"""
An example to show how to reset the position, zoom level, and layout of a Cytoscape graph, using a
button attached to a callback.
"""
import dash
from dash import Input, Output, html, callback
import dash_cytoscape as cyto


elements = [
    {"data": {"id": "one", "label": "Node 1"}, "position": {"x": 50, "y": 50}},
    {"data": {"id": "two", "label": "Node 2"}, "position": {"x": 200, "y": 200}},
    {"data": {"source": "one", "target": "two", "label": "Node 1 to 2"}},
]

layout = {"name": "grid"}

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Button("Reset", id="bt-reset"),
        cyto.Cytoscape(id="cytoscape", elements=elements, layout=layout, zoom=1),
    ]
)


@callback(
    Output("cytoscape", "zoom"),
    Output("cytoscape", "elements"),
    Input("bt-reset", "n_clicks"),
)
def reset_layout(n_clicks):
    print(n_clicks, "click")

    return [1, elements]


if __name__ == "__main__":
    app.run(debug=True)
