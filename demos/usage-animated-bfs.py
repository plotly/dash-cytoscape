"""
Original Demo: http://js.cytoscape.org/demos/animated-bfs/
Code: https://github.com/cytoscape/cytoscape.js/tree/master/documentation/demos/animated-bfs

Note: Animation Not Implemented yet, please refer to code.
"""
import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


elements = [
    {"data": {"id": "a"}},
    {"data": {"id": "b"}},
    {"data": {"id": "c"}},
    {"data": {"id": "d"}},
    {"data": {"id": "e"}},
    {"data": {"id": 'a"e', "weight": 1, "source": "a", "target": "e"}},
    {"data": {"id": "ab", "weight": 3, "source": "a", "target": "b"}},
    {"data": {"id": "be", "weight": 4, "source": "b", "target": "e"}},
    {"data": {"id": "bc", "weight": 5, "source": "b", "target": "c"}},
    {"data": {"id": "ce", "weight": 6, "source": "c", "target": "e"}},
    {"data": {"id": "cd", "weight": 2, "source": "c", "target": "d"}},
    {"data": {"id": "de", "weight": 7, "source": "d", "target": "e"}},
]

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            layout={
                "name": "breadthfirst",
                "directed": True,
                "roots": "#a",
                "padding": 10,
            },
            stylesheet=[
                {"selector": "node", "style": {"content": "data(id)"}},
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "bezier",
                        "target-arrow-shape": "triangle",
                        "width": 4,
                        "line-color": "#ddd",
                        "target-arrow-color": "#ddd",
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
