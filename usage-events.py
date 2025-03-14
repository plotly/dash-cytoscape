import json

import dash
from dash import Input, Output, dcc, html, callback

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server

# Object declaration
basic_elements = [
    {"data": {"id": "one", "label": "Node 1"}, "renderedPosition": {"x": 50, "y": 50}},
    {
        "data": {"id": "two", "label": "Node 2"},
        "renderedPosition": {"x": 200, "y": 200},
    },
    {
        "data": {"id": "three", "label": "Node 3"},
        "renderedPosition": {"x": 100, "y": 150},
    },
    {
        "data": {"id": "four", "label": "Node 4"},
        "renderedPosition": {"x": 400, "y": 50},
    },
    {
        "data": {"id": "five", "label": "Node 5"},
        "renderedPosition": {"x": 250, "y": 100},
    },
    {
        "data": {"id": "six", "label": "Node 6", "parent": "three"},
        "renderedPosition": {"x": 150, "y": 150},
    },
    {
        "data": {
            "id": "one-two",
            "source": "one",
            "target": "two",
            "label": "Edge from Node 1 to Node 2",
        }
    },
    {
        "data": {
            "id": "one-five",
            "source": "one",
            "target": "five",
            "label": "Edge from Node 1 to Node 5",
        }
    },
    {
        "data": {
            "id": "two-four",
            "source": "two",
            "target": "four",
            "label": "Edge from Node 2 to Node 4",
        }
    },
    {
        "data": {
            "id": "three-five",
            "source": "three",
            "target": "five",
            "label": "Edge from Node 3 to Node 5",
        }
    },
    {
        "data": {
            "id": "three-two",
            "source": "three",
            "target": "two",
            "label": "Edge from Node 3 to Node 2",
        }
    },
    {
        "data": {
            "id": "four-four",
            "source": "four",
            "target": "four",
            "label": "Edge from Node 4 to Node 4",
        }
    },
    {
        "data": {
            "id": "four-six",
            "source": "four",
            "target": "six",
            "label": "Edge from Node 4 to Node 6",
        }
    },
    {
        "data": {
            "id": "five-one",
            "source": "five",
            "target": "one",
            "label": "Edge from Node 5 to Node 1",
        }
    },
]
context_menu = [
    {
        "id": "add-node",
        "label": "Add Node (JS)",
        "tooltipText": "Add Node",
        "availableOn": ["canvas"],
        "onClick": "add_node",
    },
    {
        "id": "remove",
        "label": "Remove (JS)",
        "tooltipText": "Remove",
        "availableOn": ["node", "edge"],
        "onClick": "remove",
    },
    {
        "id": "add-edge",
        "label": "Add Edge (JS)",
        "tooltipText": "add edge",
        "availableOn": ["node"],
        "onClick": "add_edge",
    },
]

styles = {
    "json-output": {
        "overflow-y": "scroll",
        "height": "calc(50% - 25px)",
        "border": "thin lightgrey solid",
    },
    "tab": {"height": "calc(98vh - 115px)"},
}

app.layout = html.Div(
    [
        html.Div(
            className="eight columns",
            children=[
                cyto.Cytoscape(
                    id="cytoscape",
                    elements=basic_elements,
                    contextMenu=context_menu,
                    layout={"name": "preset"},
                    style={"height": "500px", "width": "500px"},
                    clearOnUnhover=True,
                )
            ],
        ),
        html.Div(
            className="four columns",
            children=[
                dcc.Tabs(
                    id="tabs",
                    children=[
                        dcc.Tab(
                            label="Tap Objects",
                            children=[
                                html.Div(
                                    style=styles["tab"],
                                    children=[
                                        html.P("Node Object JSON:"),
                                        html.Pre(
                                            id="tap-node-json-output",
                                            style=styles["json-output"],
                                        ),
                                        html.P("Edge Object JSON:"),
                                        html.Pre(
                                            id="tap-edge-json-output",
                                            style=styles["json-output"],
                                        ),
                                    ],
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Tap Data",
                            children=[
                                html.Div(
                                    style=styles["tab"],
                                    children=[
                                        html.P("Node Data JSON:"),
                                        html.Pre(
                                            id="tap-node-data-json-output",
                                            style=styles["json-output"],
                                        ),
                                        html.P("Edge Data JSON:"),
                                        html.Pre(
                                            id="tap-edge-data-json-output",
                                            style=styles["json-output"],
                                        ),
                                    ],
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Mouseover Data",
                            children=[
                                html.Div(
                                    style=styles["tab"],
                                    children=[
                                        html.P("Node Data JSON:"),
                                        html.Pre(
                                            id="mouseover-node-data-json-output",
                                            style=styles["json-output"],
                                        ),
                                        html.P("Edge Data JSON:"),
                                        html.Pre(
                                            id="mouseover-edge-data-json-output",
                                            style=styles["json-output"],
                                        ),
                                    ],
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Selected Data",
                            children=[
                                html.Div(
                                    style=styles["tab"],
                                    children=[
                                        html.P("Node Data JSON:"),
                                        html.Pre(
                                            id="selected-node-data-json-output",
                                            style=styles["json-output"],
                                        ),
                                        html.P("Edge Data JSON:"),
                                        html.Pre(
                                            id="selected-edge-data-json-output",
                                            style=styles["json-output"],
                                        ),
                                    ],
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Drag Data",
                            children=[
                                html.Div(
                                    style=styles["tab"],
                                    children=[
                                        html.P("Elements Data JSON:"),
                                        html.Pre(
                                            id="elements-data-json-output",
                                            style=styles["json-output"],
                                        ),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(id="placeholder"),
    ]
)


@callback(Output("tap-node-json-output", "children"), Input("cytoscape", "tapNode"))
def displayTapNode(data):
    return json.dumps(data, indent=2)


@callback(Output("tap-edge-json-output", "children"), Input("cytoscape", "tapEdge"))
def displayTapEdge(data):
    return json.dumps(data, indent=2)


@callback(
    Output("tap-node-data-json-output", "children"), Input("cytoscape", "tapNodeData")
)
def displayTapNodeData(data):
    return json.dumps(data, indent=2)


@callback(
    Output("tap-edge-data-json-output", "children"), Input("cytoscape", "tapEdgeData")
)
def displayTapEdgeData(data):
    return json.dumps(data, indent=2)


@callback(
    Output("mouseover-node-data-json-output", "children"),
    Input("cytoscape", "mouseoverNodeData"),
)
def displayMouseoverNodeData(data):
    return json.dumps(data, indent=2)


@callback(
    Output("mouseover-edge-data-json-output", "children"),
    Input("cytoscape", "mouseoverEdgeData"),
)
def displayMouseoverEdgeData(data):
    return json.dumps(data, indent=2)


@callback(
    Output("selected-node-data-json-output", "children"),
    Input("cytoscape", "selectedNodeData"),
)
def displaySelectedNodeData(data):
    return json.dumps(data, indent=2)


@callback(
    Output("selected-edge-data-json-output", "children"),
    Input("cytoscape", "selectedEdgeData"),
)
def displaySelectedEdgeData(data):
    return json.dumps(data, indent=2)


@callback(
    Output("elements-data-json-output", "children"),
    Input("cytoscape", "elements"),
)
def displayElementsData(data):
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    app.run(debug=True)
