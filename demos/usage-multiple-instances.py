"""
Original Demo: http://js.cytoscape.org/demos/multiple-instances/
"""
import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


elements = [
    {"data": {"id": "a", "foo": 3, "bar": 5, "baz": 7}},
    {"data": {"id": "b", "foo": 7, "bar": 1, "baz": 3}},
    {"data": {"id": "c", "foo": 2, "bar": 7, "baz": 6}},
    {"data": {"id": "d", "foo": 9, "bar": 5, "baz": 2}},
    {"data": {"id": "e", "foo": 2, "bar": 4, "baz": 5}},
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
            id="cytoscape-top",
            elements=elements,
            layout={"name": "circle", "padding": 10},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "background-color": "#B3767E",
                        "width": "mapData(baz, 0, 10, 10, 40)",
                        "height": "mapData(baz, 0, 10, 10, 40)",
                        "content": "data(id)",
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#F2B1BA",
                        "target-arrow-color": "#F2B1BA",
                        "width": 2,
                        "target-arrow-shape": "circle",
                        "opacity": 0.8,
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
                "height": "50%",
                "position": "absolute",
                "background-color": "#FAEDEF",
                "left": 0,
                "top": 0,
            },
        ),
        cyto.Cytoscape(
            id="cytoscape-bottom",
            elements=elements,
            layout={"name": "breadthfirst", "directed": True, "padding": 10},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "background-color": "#6272A3",
                        "shape": "rectangle",
                        "width": "mapData(foo, 0, 10, 10, 30)",
                        "height": "mapData(bar, 0, 10, 10, 50)",
                        "content": "data(id)",
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "width": "mapData(weight, 0, 10, 3, 9)",
                        "line-color": "#B1C1F2",
                        "target-arrow-color": "#B1C1F2",
                        "target-arrow-shape": "triangle",
                        "opacity": 0.8,
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
                "height": "50%",
                "position": "absolute",
                "background-color": "#EDF1FA",
                "left": 0,
                "top": "50%",
                "border-top": "1px solid #ccc",
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
