import dash
from dash import html
import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server

elements = [
    {"data": {"id": "Node 1", "label": "Node 1"}, "position": {"x": 0, "y": 0}},
    {"data": {"id": "Node 2", "label": "Node 2"}, "position": {"x": 50, "y": 50}},
    {"data": {"source": "Node 1", "target": "Node 2", "label": ""}},
]


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Low wheel sensitivity (0.01)"),
                cyto.Cytoscape(
                    id="cytoscape-slow",
                    elements=elements,
                    wheelSensitivity=0.01,
                ),
            ]
        ),
        html.Div(
            [
                html.H1("Default wheel sensitivity (1)"),
                cyto.Cytoscape(
                    id="cytoscape-normal",
                    elements=elements,
                    wheelSensitivity=1,
                ),
            ]
        ),
        html.Div(
            [
                html.H1("High wheel sensitivity (100)"),
                cyto.Cytoscape(
                    id="cytoscape-fast",
                    elements=elements,
                    wheelSensitivity=100,
                ),
            ]
        ),
    ],
    style={"display": "flex"},
)


if __name__ == "__main__":
    app.run(debug=True)
