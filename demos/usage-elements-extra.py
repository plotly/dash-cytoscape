import json
import os

import dash
from dash import Input, Output, State, dcc, html, callback

import dash_cytoscape as cyto
from demos import dash_reusable_components as drc

# Load extra layouts
cyto.load_extra_layouts()


asset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

app = dash.Dash(__name__, assets_folder=asset_path)
server = app.server


# ###################### DATA PREPROCESSING ######################
# Load data
with open("data/sample_network.txt", "r", encoding="utf-8") as f:
    network_data = f.read().split("\n")

# We select the first 750 edges and associated nodes for an easier visualization
edges = network_data[:750]
nodes = set()

following_node_di = {}  # user id -> list of users they are following
following_edges_di = {}  # user id -> list of cy edges starting from user id

followers_node_di = {}  # user id -> list of followers (cy_node format)
followers_edges_di = {}  # user id -> list of cy edges ending at user id

cy_edges = []
cy_nodes = []

for edge in edges:
    if " " not in edge:
        continue

    source, target = edge.split(" ")

    cy_edge = {"data": {"id": source + target, "source": source, "target": target}}
    cy_target = {"data": {"id": target, "label": "User #" + str(target[-5:])}}
    cy_source = {"data": {"id": source, "label": "User #" + str(source[-5:])}}

    if source not in nodes:
        nodes.add(source)
        cy_nodes.append(cy_source)
    if target not in nodes:
        nodes.add(target)
        cy_nodes.append(cy_target)

    # Process dictionary of following
    if not following_node_di.get(source):
        following_node_di[source] = []
    if not following_edges_di.get(source):
        following_edges_di[source] = []

    following_node_di[source].append(cy_target)
    following_edges_di[source].append(cy_edge)

    # Process dictionary of followers
    if not followers_node_di.get(target):
        followers_node_di[target] = []
    if not followers_edges_di.get(target):
        followers_edges_di[target] = []

    followers_node_di[target].append(cy_source)
    followers_edges_di[target].append(cy_edge)

genesis_node = cy_nodes[0]
genesis_node["classes"] = "genesis"
default_elements = [genesis_node]

default_stylesheet = [
    {"selector": "node", "style": {"opacity": 0.65, "z-index": 9999}},
    {
        "selector": "edge",
        "style": {"curve-style": "bezier", "opacity": 0.45, "z-index": 5000},
    },
    {"selector": ".followerNode", "style": {"background-color": "#0074D9"}},
    {
        "selector": ".followerEdge",
        "style": {
            "mid-target-arrow-color": "blue",
            "mid-target-arrow-shape": "vee",
            "line-color": "#0074D9",
        },
    },
    {"selector": ".followingNode", "style": {"background-color": "#FF4136"}},
    {
        "selector": ".followingEdge",
        "style": {
            "mid-target-arrow-color": "red",
            "mid-target-arrow-shape": "vee",
            "line-color": "#FF4136",
        },
    },
    {
        "selector": ".genesis",
        "style": {
            "background-color": "#B10DC9",
            "border-width": 2,
            "border-color": "purple",
            "border-opacity": 1,
            "opacity": 1,
            "label": "data(label)",
            "color": "#B10DC9",
            "text-opacity": 1,
            "font-size": 12,
            "z-index": 9999,
        },
    },
    {
        "selector": ":selected",
        "style": {
            "border-width": 2,
            "border-color": "black",
            "border-opacity": 1,
            "opacity": 1,
            "label": "data(label)",
            "color": "black",
            "font-size": 12,
            "z-index": 9999,
        },
    },
]

# ################################# APP LAYOUT ################################
styles = {
    "json-output": {
        "overflow-y": "scroll",
        "height": "calc(50% - 25px)",
        "border": "thin lightgrey solid",
    },
    "tab": {"height": "calc(98vh - 80px)"},
}

app.layout = html.Div(
    [
        html.Div(
            className="eight columns",
            children=[
                cyto.Cytoscape(
                    id="cytoscape",
                    elements=default_elements,
                    stylesheet=default_stylesheet,
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
                                        "cose-bilkent",
                                        "dagre",
                                        "cola",
                                        "klay",
                                        "spread",
                                        "euler",
                                    ),
                                    value="grid",
                                    clearable=False,
                                ),
                                drc.NamedRadioItems(
                                    name="Expand",
                                    id="radio-expand",
                                    options=drc.DropdownOptionsList(
                                        "followers", "following"
                                    ),
                                    value="followers",
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


# ############################## CALLBACKS ####################################
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
    Output("cytoscape", "elements"),
    Input("cytoscape", "tapNodeData"),
    State("cytoscape", "elements"),
    State("radio-expand", "value"),
)
def generate_elements(nodeData, elements, expansion_mode):
    if not nodeData:
        return default_elements

    # If the node has already been expanded, we don't expand it again
    if nodeData.get("expanded"):
        return elements

    # This retrieves the currently selected element, and tag it as expanded
    for element in elements:
        if nodeData["id"] == element.get("data").get("id"):
            element["data"]["expanded"] = True
            break

    if expansion_mode == "followers":
        followers_nodes = followers_node_di.get(nodeData["id"])
        followers_edges = followers_edges_di.get(nodeData["id"])

        if followers_nodes:
            for node in followers_nodes:
                node["classes"] = "followerNode"
            elements.extend(followers_nodes)

        if followers_edges:
            for follower_edge in followers_edges:
                follower_edge["classes"] = "followerEdge"
            elements.extend(followers_edges)

    elif expansion_mode == "following":
        following_nodes = following_node_di.get(nodeData["id"])
        following_edges = following_edges_di.get(nodeData["id"])

        if following_nodes:
            for node in following_nodes:
                if node["data"]["id"] != genesis_node["data"]["id"]:
                    node["classes"] = "followingNode"
                    elements.append(node)

        if following_edges:
            for follower_edge in following_edges:
                follower_edge["classes"] = "followingEdge"
            elements.extend(following_edges)

    return elements


if __name__ == "__main__":
    app.run(debug=True)
