import dash
from dash.dependencies import Input, Output
import dash_html_components as html

import dash_cytoscape as cyto
cyto.load_extra_layouts()

app = dash.Dash(__name__)
server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

elements = [
    {'data': {'id': 'a', 'lat': 43.662402, 'lon': -79.388910}},
    {'data': {'id': 'b', 'lat': 43.658560, 'lon': -79.384574}},
    {'data': {'id': 'ab', 'source': 'a', 'target': 'b'}}
]

# App
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        boxSelectionEnabled=False,
        autounselectify=True,
        elements=elements,
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
                    'content': 'data(id)',
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
            'tileUrl': 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png',
            'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            'maxZoom': 18,
        }
    )
])



if __name__ == '__main__':
    app.run_server(debug=True)
