import dash
import dash_cytoscape as cyto
from dash import html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=[
                {
                    "data": {"id": "one", "label": "Node 1"},
                    "position": {"x": 50, "y": 50},
                },
                {
                    "data": {"id": "two", "label": "Node 2"},
                    "position": {"x": 200, "y": 200},
                },
                {"data": {"source": "one", "target": "two", "label": "1 to 2"}},
            ],
            layout={"name": "preset"},
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
