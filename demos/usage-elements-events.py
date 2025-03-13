import dash
from dash import callback, Input, Output, html
import dash_cytoscape as cyto
import json

app = dash.Dash(__name__)
server = app.server

cyto_elements = [
    {"data": {"id": "Node 1", "label": "Node 1"}, "position": {"x": 0, "y": 0}},
    {"data": {"id": "Node 2", "label": "Node 2"}, "position": {"x": 50, "y": 50}},
    {"data": {"source": "Node 1", "target": "Node 2", "label": ""}},
]


app.layout = html.Div(
    [
        html.Div(
            cyto.Cytoscape(
                id="cytoscape",
                elements=cyto_elements,
                responsive=True,
                clearOnUnhover=True,
            ),
        ),
        html.Div(
            [
                html.Div(id="mouse-over-node"),
                html.Div(id="mouse-over-edge"),
                html.Div(id="elements"),
                html.Div(id="tap-element"),
            ]
        ),
    ]
)


@callback(
    Output("mouse-over-node", "children"),
    Output("mouse-over-edge", "children"),
    Input("cytoscape", "mouseoverNodeData"),
    Input("cytoscape", "mouseoverEdgeData"),
)
def show_mouseoverNodeData(mouseoverNodeData, mouseoverEdgeData):
    return (
        f"Mouse over node: {str(mouseoverNodeData)}",
        f"Mouse over edge: {str(mouseoverEdgeData)}",
    )


@callback(
    Output("elements", "children"),
    Input("cytoscape", "elements"),
)
def show_elements(elements):
    return "Updated elements: " + str(elements)


@callback(
    Output("tap-element", "children"),
    Input("cytoscape", "tapNodeData"),
    Input("cytoscape", "tapEdgeData"),
)
def displayTapNode(data, data_):
    return f"Tap node: {json.dumps(data, indent=2)}, Tap edge: {json.dumps(data_, indent=2)}"


if __name__ == "__main__":
    app.run(debug=True)
