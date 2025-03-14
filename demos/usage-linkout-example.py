"""
Original Demo: http://js.cytoscape.org/demos/linkout-example/

Note: Href Links do not work

"""
import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


elements = [
    {"data": {"id": "desktop", "name": "Cytoscape", "href": "http://cytoscape.org"}},
    {"data": {"id": "js", "name": "Cytoscape.js", "href": "http://js.cytoscape.org"}},
    {"data": {"source": "desktop", "target": "js"}},
]

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            boxSelectionEnabled=False,
            autounselectify=True,
            layout={"name": "grid", "padding": 10},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "content": "data(name)",
                        "text-valign": "center",
                        "color": "white",
                        "text-outline-width": 2,
                        "text-outline-color": "#888",
                        "background-color": "#888",
                    },
                },
                {
                    "selector": ":selected",
                    "style": {
                        "background-color": "black",
                        "line-color": "black",
                        "target-arrow-color": "black",
                        "source-arrow-color": "black",
                        "text-outline-color": "black",
                    },
                },
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
