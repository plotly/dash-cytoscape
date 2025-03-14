"""
Original Demo: http://js.cytoscape.org/demos/cose-layout/

Note: This implementation looks different from the original implementation,
although the input paramters are exactly the same.
"""
import json

import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


# Load Data
with open("data/cose-layout/data.json", "r", encoding="utf-8") as f:
    elements = json.loads(f.read())

with open("data/cose-layout/cy-style.json", "r", encoding="utf-8") as f:
    stylesheet = json.loads(f.read())

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            stylesheet=stylesheet,
            style={
                "width": "100%",
                "height": "100%",
                "position": "absolute",
                "left": 0,
                "top": 0,
                "z-index": 999,
            },
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
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
