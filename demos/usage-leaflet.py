import dash
from dash.dependencies import Input, Output
import dash_html_components as html

import dash_cytoscape as cyto
cyto.load_extra_layouts()

app = dash.Dash(__name__)
server = app.server

elements = [
    {'data': {'id': 'a', 'label': 'Node A', 'lat': 43.662402, 'lon': -79.388910}},
    {'data': {'id': 'b', 'label': 'Node B', 'lat': 43.658560, 'lon': -79.384574}},
    {'data': {'id': 'ab', 'source': 'a', 'target': 'b'}}
]

# App
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        boxSelectionEnabled=True,
        layout={
            'name': 'preset',
            'padding': 10
        },
        stylesheet=[
            {
                'selector': 'core',
                'style': {
                    'active-bg-opacity': 0
                },
            },
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)',
                    'background-color': 'yellow',
                    'width': 15,
                    'height': 15
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'line-color': 'yellow',
                    'target-arrow-color': 'yellow'
                }
            },
            {
                'selector': ':selected',
                'style': {
                    'line-color': '#0056DA',
                    'target-arrow-color': '#0056DA',
                    'background-color': '#0056DA'
                }
            },
            {
                'selector': 'node, edge',
                'style': {
                    'transition-property': 'opacity',
                    'transition-duration': '250ms',
                    'transition-timing-function': 'ease-in-out'
                }
            },
            {
                'selector': '.leaflet-viewport',
                'style': {
                    'opacity': 0.333,
                    'transition-duration': '0ms',
                }
            }
        ],
        style={
            'width': '100%',
            'height': '100%',
            'position': 'absolute',
            'left': 0,
            'top': 0
        },
        leaflet={
            'preset': 'CartoDB.Positron'
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
