"""
Original Demo: http://js.cytoscape.org/demos/pie-style/
"""
import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


elements = [
    {"data": {"id": "a", "foo": 3, "bar": 5, "baz": 2}},
    {"data": {"id": "b", "foo": 6, "bar": 1, "baz": 3}},
    {"data": {"id": "c", "foo": 2, "bar": 3, "baz": 5}},
    {"data": {"id": "d", "foo": 7, "bar": 1, "baz": 2}},
    {"data": {"id": "e", "foo": 2, "bar": 3, "baz": 5}},
    {"data": {"id": "ae", "weight": 1, "source": "a", "target": "e"}},
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
            layout={"name": "circle", "padding": 10},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "width": "60px",
                        "height": "60px",
                        "content": "data(id)",
                        "pie-size": "80%",
                        "pie-1-background-color": "#E8747C",
                        "pie-1-background-size": "mapData(foo, 0, 10, 0, 100)",
                        "pie-2-background-color": "#74CBE8",
                        "pie-2-background-size": "mapData(bar, 0, 10, 0, 100)",
                        "pie-3-background-color": "#74E883",
                        "pie-3-background-size": "mapData(baz, 0, 10, 0, 100)",
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "bezier",
                        "width": 4,
                        "target-arrow-shape": "triangle",
                        "opacity": 0.5,
                    },
                },
                {
                    "selector": ":selected",
                    "style": {
                        "background-color": "black",
                        "line-color": "black",
                        "target-arrow-color": "black",
                        "source-arrow-color": "black",
                        "opacity": 1,
                    },
                },
                {"selector": ".faded", "style": {"opacity": 0.25, "text-opacity": 0}},
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
