"""
Original Demo: http://js.cytoscape.org/demos/circle-layout/
"""
import json

import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


# Load Data
with open("data/circle-layout/data.json", "r", encoding="utf-8") as f:
    elements = json.loads(f.read())

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            layout={"name": "circle"},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {"height": 20, "width": 20, "background-color": "#e8e406"},
                },
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "haystack",
                        "haystack-radius": 0,
                        "width": 5,
                        "opacity": 0.5,
                        "line-color": "#f2f08c",
                    },
                },
            ],
            style={
                "width": "100%",
                "height": "100%",
                "position": "absolute",
                "left": 0,
                "top": 0,
                "z-index": 999,
            },
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
