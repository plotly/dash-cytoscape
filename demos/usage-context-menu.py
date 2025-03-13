import dash
import dash_cytoscape as cyto
import dash_html_components as html
from dash import callback, Input, Output, State
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
                    "label": "Add Node (JS)",
                    "tooltipText": "Add Node",
                    "onClick": "add_node",
                    "availableOn": ["canvas"],
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
                {
                    "id": "split-edge",
                    "label": "Split Edge (PY)",
                    "tooltipText": "split edge",
                    "availableOn": ["edge"],
                },
                {
                    "id": "reverse-edge",
                    "label": "Reverse Edge (PY)",
                    "tooltipText": "reverse edge",
                    "availableOn": ["edge"],
                },
                {
                    "id": "add-2-nodes",
                    "label": "Add 2 Nodes (NS)",
                    "tooltipText": "add 2 nodes",
                    "onClickCustom": "add_2_nodes",
                    "availableOn": ["canvas"],
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
    elif ctxMenuData["menuItemId"] == "reverse-edge":
        elements = reverse_egde(elements, ctxMenuData)
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


def reverse_egde(elements, ctx):
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
    app.run(debug=True)
