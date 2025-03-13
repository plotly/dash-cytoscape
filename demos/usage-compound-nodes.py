"""
Original Demo: http://js.cytoscape.org/demos/compound-nodes/

Note: The Dash version is also uncentered. Otherwise it works.
"""
import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


elements = [
    {"data": {"id": "a", "parent": "b"}, "position": {"x": 215, "y": 85}},
    {"data": {"id": "b"}},
    {"data": {"id": "c", "parent": "b"}, "position": {"x": 300, "y": 85}},
    {"data": {"id": "d"}, "position": {"x": 215, "y": 175}},
    {"data": {"id": "e"}},
    {"data": {"id": "f", "parent": "e"}, "position": {"x": 300, "y": 175}},
    {"data": {"id": "ad", "source": "a", "target": "d"}},
    {"data": {"id": "eb", "source": "e", "target": "b"}},
]

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            boxSelectionEnabled=False,
            autounselectify=True,
            layout={"name": "preset", "padding": 5},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "content": "data(id)",
                        "text-valign": "center",
                        "text-halign": "center",
                    },
                },
                {
                    "selector": "$node > node",
                    "style": {
                        "padding-top": "10px",
                        "padding-left": "10px",
                        "padding-bottom": "10px",
                        "padding-right": "10px",
                        "text-valign": "top",
                        "text-halign": "center",
                        "background-color": "#bbb",
                    },
                },
                {
                    "selector": ":selected",
                    "style": {
                        "background-color": "black",
                        "line-color": "black",
                        "target-arrow-color": "black",
                        "source-arrow-color": "black",
                    },
                },
                {"selector": "edge", "style": {"target-arrow-shape": "triangle"}},
            ],
            style={
                "width": "100%",
                "height": "100%",
                "position": "absolute",
                "left": 0,
                "top": 0,
            },
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
