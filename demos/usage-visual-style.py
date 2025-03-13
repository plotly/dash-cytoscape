"""
Original Demo: http://js.cytoscape.org/demos/visual-style/
"""
import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


elements = [
    {
        "data": {
            "id": "j",
            "name": "Jerry",
            "weight": 65,
            "faveColor": "#6FB1FC",
            "faveShape": "triangle",
        }
    },
    {
        "data": {
            "id": "e",
            "name": "Elaine",
            "weight": 45,
            "faveColor": "#EDA1ED",
            "faveShape": "ellipse",
        }
    },
    {
        "data": {
            "id": "k",
            "name": "Kramer",
            "weight": 75,
            "faveColor": "#86B342",
            "faveShape": "octagon",
        }
    },
    {
        "data": {
            "id": "g",
            "name": "George",
            "weight": 70,
            "faveColor": "#F5A45D",
            "faveShape": "rectangle",
        }
    },
    {"data": {"source": "j", "target": "e", "faveColor": "#6FB1FC", "strength": 90}},
    {"data": {"source": "j", "target": "k", "faveColor": "#6FB1FC", "strength": 70}},
    {"data": {"source": "j", "target": "g", "faveColor": "#6FB1FC", "strength": 80}},
    {"data": {"source": "e", "target": "j", "faveColor": "#EDA1ED", "strength": 95}},
    {
        "data": {"source": "e", "target": "k", "faveColor": "#EDA1ED", "strength": 60},
        "classes": "questionable",
    },
    {"data": {"source": "k", "target": "j", "faveColor": "#86B342", "strength": 100}},
    {"data": {"source": "k", "target": "e", "faveColor": "#86B342", "strength": 100}},
    {"data": {"source": "k", "target": "g", "faveColor": "#86B342", "strength": 100}},
    {"data": {"source": "g", "target": "j", "faveColor": "#F5A45D", "strength": 90}},
]

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            layout={"name": "cose", "padding": 10},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "shape": "data(faveShape)",
                        "width": "mapData(weight, 40, 80, 20, 60)",
                        "content": "data(name)",
                        "text-valign": "center",
                        "text-outline-width": 2,
                        "text-outline-color": "data(faveColor)",
                        "background-color": "data(faveColor)",
                        "color": "#fff",
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "bezier",
                        "opacity": 0.666,
                        "width": "mapData(strength, 70, 100, 2, 6)",
                        "target-arrow-shape": "triangle",
                        "source-arrow-shape": "circle",
                        "line-color": "data(faveColor)",
                        "source-arrow-color": "data(faveColor)",
                        "target-arrow-color": "data(faveColor)",
                    },
                },
                {
                    "selector": ":selected",
                    "style": {"border-width": 3, "border-color": "#333"},
                },
                {
                    "selector": "edge.questionable",
                    "style": {"line-style": "dotted", "target-arrow-shape": "diamond"},
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
