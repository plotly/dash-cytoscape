"""
Original Demo: http://js.cytoscape.org/demos/cose-layout/

Note: This implementation looks different from the original implementation,
although the input paramters are exactly the same.
"""
import urllib.request
import json

import dash
from dash import Input, Output, html, callback

import dash_cytoscape as cyto


app = dash.Dash(__name__)
server = app.server


# Load Data
with urllib.request.urlopen(
    "https://js.cytoscape.org/demos/colajs-graph/data.json"
) as url:
    elements = json.loads(url.read().decode())

with urllib.request.urlopen(
    "https://js.cytoscape.org/demos/colajs-graph/cy-style.json"
) as url:
    stylesheet = json.loads(url.read().decode())

styles = {
    "container": {
        "position": "fixed",
        "display": "flex",
        "flex-direction": "column",
        "height": "100%",
        "width": "100%",
    },
    "cy-container": {"flex": "1", "position": "relative"},
    "cytoscape": {
        "position": "absolute",
        "width": "100%",
        "height": "100%",
        "z-index": 999,
    },
}

# App
app.layout = html.Div(
    style=styles["container"],
    children=[
        html.Div(
            [
                html.Button("Responsive Toggle", id="toggle-button"),
                html.Div(id="toggle-text"),
            ]
        ),
        html.Div(
            className="cy-container",
            style=styles["cy-container"],
            children=[
                cyto.Cytoscape(
                    id="cytoscape",
                    elements=elements,
                    stylesheet=stylesheet,
                    style=styles["cytoscape"],
                    layout={
                        "name": "cose",
                        "idealEdgeLength": 100,
                        "nodeOverlap": 20,
                        "refresh": 20,
                        "fit": True,
                        "padding": 30,
                        "randomize": False,
                        "componentSpacing": 100,
                        "nodeRepulsion": 400000,
                        "edgeElasticity": 100,
                        "nestingFactor": 5,
                        "gravity": 80,
                        "numIter": 1000,
                        "initialTemp": 200,
                        "coolingFactor": 0.95,
                        "minTemp": 1.0,
                    },
                    responsive=True,
                )
            ],
        ),
    ],
)


@callback(Output("cytoscape", "responsive"), Input("toggle-button", "n_clicks"))
def toggle_responsive(n_clicks):
    n_clicks = 2 if n_clicks is None else n_clicks
    toggle_on = n_clicks % 2 == 0
    return toggle_on


@callback(Output("toggle-text", "children"), Input("cytoscape", "responsive"))
def update_toggle_text(responsive):
    return "\t" + "Responsive " + ("On" if responsive else "Off")


if __name__ == "__main__":
    app.run(debug=True)
