"""
Original Demo: http://js.cytoscape.org/demos/cose-bilkent-layout-compound/

Note: This implementation DOES NOT work yet, since cose-bilkent hasn't been implemented yet

"""
import json

import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server

app.scripts.append_script(
    {
        "external_url": (
            "https://cdn.rawgit.com/cytoscape/cytoscape.js-cose-bilkent/d810281d/"
            "cytoscape-cose-bilkent.js"
        )
    }
)


# Load Data
with open("data/cose-bilkent-layout/data.json", "r", encoding="utf-8") as f:
    elements = json.loads(f.read())

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            layout={"name": "cose-bilkent", "animate": False},
            stylesheet=[
                {"selector": "node", "style": {"background-color": "#ad1a66"}},
                {"selector": "edge", "style": {"width": 3, "line-color": "#ad1a66"}},
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
