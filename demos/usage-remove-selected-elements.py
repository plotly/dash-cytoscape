import json
import os
import random

import dash
from dash import Input, Output, State, dcc, html, callback

import dash_cytoscape as cyto

asset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

app = dash.Dash(__name__, assets_folder=asset_path)
server = app.server

random.seed(2019)

nodes = [{"data": {"id": str(i), "label": f"Node {i}"}} for i in range(1, 21)]

edges = [
    {
        "data": {
            "source": str(random.randint(1, 20)),
            "target": str(random.randint(1, 20)),
        }
    }
    for _ in range(30)
]

default_elements = nodes + edges

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
                    elements=default_elements,
                    layout={"name": "grid"},
                    style={"height": "95vh", "width": "100%"},
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
                            label="Actions",
                            children=[
                                html.Button("Remove Selected Node", id="remove-button")
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
                    ],
                ),
            ],
        ),
    ]
)


@callback(
    Output("cytoscape", "elements"),
    Input("remove-button", "n_clicks"),
    State("cytoscape", "elements"),
    State("cytoscape", "selectedNodeData"),
)
def remove_selected_nodes(_, elements, data):
    if elements and data:
        ids_to_remove = {ele_data["id"] for ele_data in data}
        print("Before:", elements)
        new_elements = [
            ele for ele in elements if ele["data"]["id"] not in ids_to_remove
        ]
        print("After:", new_elements)
        return new_elements

    return elements


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


if __name__ == "__main__":
    app.run(debug=True)
