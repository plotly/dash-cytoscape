import json

import dash
from dash import Input, Output, dcc, html, callback

import dash_cytoscape as cyto
from demos import dash_reusable_components as drc

app = dash.Dash(__name__)
server = app.server

# ###################### DATA PREPROCESSING ######################
# Load data
with open("demos/data/sample_network.txt", "r", encoding="utf-8") as f:
    network_data = f.read().split("\n")

# We select the first 750 edges and associated nodes for an easier visualization
edges = network_data[:750]
nodes = set()

cy_edges = []
cy_nodes = []

for network_edge in edges:
    source, target = network_edge.split(" ")

    if source not in nodes:
        nodes.add(source)
        cy_nodes.append({"data": {"id": source, "label": "User #" + source[-5:]}})
    if target not in nodes:
        nodes.add(target)
        cy_nodes.append({"data": {"id": target, "label": "User #" + target[-5:]}})

    cy_edges.append({"data": {"source": source, "target": target}})

default_stylesheet = [
    {
        "selector": "node",
        "style": {
            "opacity": 0.65,
        },
    },
    {"selector": "edge", "style": {"curve-style": "bezier", "opacity": 0.65}},
]

styles = {
    "json-output": {
        "overflow-y": "scroll",
        "height": "calc(50% - 25px)",
        "border": "thin lightgrey solid",
    },
    "tab": {"height": "calc(98vh - 105px)"},
}

app.layout = html.Div(
    [
        html.Div(
            className="eight columns",
            children=[
                cyto.Cytoscape(
                    id="cytoscape",
                    elements=cy_edges + cy_nodes,
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
                            label="Control Panel",
                            children=[
                                drc.NamedDropdown(
                                    name="Layout",
                                    id="dropdown-layout",
                                    options=drc.DropdownOptionsList(
                                        "random",
                                        "grid",
                                        "circle",
                                        "concentric",
                                        "breadthfirst",
                                        "cose",
                                    ),
                                    value="grid",
                                    clearable=False,
                                ),
                                drc.NamedDropdown(
                                    name="Node Shape",
                                    id="dropdown-node-shape",
                                    value="ellipse",
                                    clearable=False,
                                    options=drc.DropdownOptionsList(
                                        "ellipse",
                                        "triangle",
                                        "rectangle",
                                        "diamond",
                                        "pentagon",
                                        "hexagon",
                                        "heptagon",
                                        "octagon",
                                        "star",
                                        "polygon",
                                    ),
                                ),
                                drc.NamedInput(
                                    name="Followers Color",
                                    id="input-follower-color",
                                    type="text",
                                    value="#0074D9",
                                ),
                                drc.NamedInput(
                                    name="Following Color",
                                    id="input-following-color",
                                    type="text",
                                    value="#FF4136",
                                ),
                            ],
                        ),
                        dcc.Tab(
                            label="JSON",
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
                    ],
                ),
            ],
        ),
    ]
)


@callback(Output("tap-node-json-output", "children"), Input("cytoscape", "tapNode"))
def display_tap_node(data):
    return json.dumps(data, indent=2)


@callback(Output("tap-edge-json-output", "children"), Input("cytoscape", "tapEdge"))
def display_tap_edge(data):
    return json.dumps(data, indent=2)


@callback(Output("cytoscape", "layout"), Input("dropdown-layout", "value"))
def update_cytoscape_layout(layout):
    return {"name": layout}


@callback(
    Output("cytoscape", "stylesheet"),
    [
        Input("cytoscape", "tapNode"),
        Input("input-follower-color", "value"),
        Input("input-following-color", "value"),
        Input("dropdown-node-shape", "value"),
    ],
)
def generate_stylesheet(node, follower_color, following_color, node_shape):
    if not node:
        return default_stylesheet

    stylesheet = [
        {"selector": "node", "style": {"opacity": 0.3, "shape": node_shape}},
        {
            "selector": "edge",
            "style": {
                "opacity": 0.2,
                "curve-style": "bezier",
            },
        },
        {
            "selector": f'node[id = "{node["data"]["id"]}"]',
            "style": {
                "background-color": "#B10DC9",
                "border-color": "purple",
                "border-width": 2,
                "border-opacity": 1,
                "opacity": 1,
                "label": "data(label)",
                "color": "#B10DC9",
                "text-opacity": 1,
                "font-size": 12,
                "z-index": 9999,
            },
        },
    ]

    for edge in node["edgesData"]:
        if edge["source"] == node["data"]["id"]:
            stylesheet.append(
                {
                    "selector": f'node[id = "{edge["target"]}"]',
                    "style": {"background-color": following_color, "opacity": 0.9},
                }
            )
            stylesheet.append(
                {
                    "selector": f'edge[id= "{edge["id"]}"]',
                    "style": {
                        "mid-target-arrow-color": following_color,
                        "mid-target-arrow-shape": "vee",
                        "line-color": following_color,
                        "opacity": 0.9,
                        "z-index": 5000,
                    },
                }
            )

        if edge["target"] == node["data"]["id"]:
            stylesheet.append(
                {
                    "selector": f'node[id = "{edge["source"]}"]',
                    "style": {
                        "background-color": follower_color,
                        "opacity": 0.9,
                        "z-index": 9999,
                    },
                }
            )
            stylesheet.append(
                {
                    "selector": f'edge[id= "{edge["id"]}"]',
                    "style": {
                        "mid-target-arrow-color": follower_color,
                        "mid-target-arrow-shape": "vee",
                        "line-color": follower_color,
                        "opacity": 1,
                        "z-index": 5000,
                    },
                }
            )

    return stylesheet


if __name__ == "__main__":
    app.run(debug=True)
