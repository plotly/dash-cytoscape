import dash
import dash_cytoscape as cyto
import dash_html_components as html
from dash import callback, Input, Output, html
import dash_core_components as dcc

contextMenuItems = {
    "add-node": {
        "id": "add-node",
        "label": "Add Node (JS)",
        "tooltipText": "Add Node",
        "onClick": "add_node",
        "availableOn": ["canvas"],
    },
    "remove": {
        "id": "remove",
        "label": "Remove (JS)",
        "tooltipText": "Remove",
        "availableOn": ["node", "edge"],
        "onClick": "remove",
    },
    "add-edge": {
        "id": "add-edge",
        "label": "Add Edge (JS)",
        "tooltipText": "add edge",
        "availableOn": ["node"],
        "onClick": "add_edge",
    },
}


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
        dcc.Dropdown(
            options=[{"label": l, "value": l} for l in contextMenuItems.keys()],
            id="dropdown",
        ),
    ]
)


@callback(
    Output("cytoscape", "contextMenu"),
    Input("dropdown", "value"),
    prevent_initial_call=True,
)
def update_output(dropdown_value):
    return [contextMenuItems[dropdown_value]]


if __name__ == "__main__":
    app.run(debug=True)
