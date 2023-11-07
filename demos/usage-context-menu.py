import dash
import dash_cytoscape as cyto
import dash_html_components as html
from dash import callback, Input, Output, html, State
import dash_core_components as dcc
import time

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=[
                {
                    "data": {"id": "one"},
                    "position": {"x": 50, "y": 50},
                },
                {
                    "data": {"id": "two"},
                    "position": {"x": 200, "y": 200},
                },
                {"data": {"source": "one", "target": "two"}},
            ],
            layout={"name": "preset"},
            contextMenu=[
                {
                    "id": "add-node",
                    "content": "Add Node (JS)",
                    "tooltipText": "Add Node",
                    "onClick": "add_nodee",
                    "showOnWhiteSpace": True,
                },
                {
                    "id": "remove",
                    "content": "Remove (JS)",
                    "tooltipText": "Remove",
                    "selector": "node, edge",
                    "onClick": "remove",
                },
                {
                    "id": "add-edge",
                    "content": "Add Edge (JS)",
                    "tooltipText": "add edge",
                    "selector": "node",
                    "onClick": "add_edge",
                },
                {
                    "id": "split-edge",
                    "content": "Split Edge (PY)",
                    "tooltipText": "split edge",
                    "selector": "edge",
                },
                {
                    "id": "revert-edge",
                    "content": "Revert Edge (PY)",
                    "tooltipText": "revert edge",
                    "selector": "edge",
                },
                {
                    "id": "add-2-nodes",
                    "content": "Add 2 Nodes (NS)",
                    "tooltipText": "add 2 nodes",
                    "onClickCustom": "add_2_nodes",
                    "showOnWhiteSpace": True,
                },
            ],
            stylesheet=[
                {
                    "selector": "edge",
                    "style": {
                        "target-arrow-color": "grey",
                        "target-arrow-shape": "vee",
                        "curve-style": "straight",
                    },
                },
                {"selector": "node", "style": {"label": "data(label)"}},
            ],
        ),
        html.Div(id="output-selection"),
        html.Div(id="output"),
    ]
)


@callback(
    Output("output", "children"),
    Output("cytoscape", "elements"),
    Input("cytoscape", "contextMenuData"),
    State("cytoscape", "elements"),
)
def update_output(ctxMenuData, elements):
    if not ctxMenuData:
        return "", elements
    if ctxMenuData["menuItemId"] == "split-edge":
        elements = split_edge(elements, ctxMenuData)
    elif ctxMenuData["menuItemId"] == "revert-edge":
        elements = revert_egde(elements, ctxMenuData)
    tap = f"You clicked on: {str(ctxMenuData)}"
    return tap, elements


def split_edge(elements, ctx):
    intermediary_node_id = str(time.time())
    elements.append(
        {
            "data": {"id": intermediary_node_id},
            "position": {"x": ctx["x"], "y": ctx["y"]},
        }
    )
    elements.append(
        {
            "data": {
                "id": str(time.time()),
                "source": ctx["edgeSource"],
                "target": intermediary_node_id,
            }
        }
    )
    elements.append(
        {
            "data": {
                "id": str(time.time()),
                "source": intermediary_node_id,
                "target": ctx["edgeTarget"],
            }
        }
    )
    elements = [e for e in elements if not e["data"]["id"] == ctx["elementId"]]
    return elements


def revert_egde(elements, ctx):
    elements = [e for e in elements if not e["data"]["id"] == ctx["elementId"]]
    elements.append(
        {
            "data": {
                "id": ctx["elementId"],
                "source": ctx["edgeTarget"],
                "target": ctx["edgeSource"],
            }
        }
    )
    return elements


if __name__ == "__main__":
    app.run_server(debug=True)
