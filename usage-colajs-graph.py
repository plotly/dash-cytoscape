import my_dash_component
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import json

app = dash.Dash('')

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

with open('data/colajs-graph/data.json', 'r') as f:
    elements = json.loads(f.read())

with open('data/colajs-graph/cy-style.json', 'r') as f:
    stylesheet = json.loads(f.read())


app.layout = html.Div([
    my_dash_component.Cytoscape(
        id='cytoscape',
        elements=elements,
        stylesheet=stylesheet,
        style={'height': '75vh', 'width': '75vw'}
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
