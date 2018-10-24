import my_dash_component
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import json

from cytoscape import dash_reusable_components as drc

app = dash.Dash('')

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

# ###################### DATA PREPROCESSING ######################
# Load data
with open('100518419853963396365.edges', 'r') as f:
    data = f.read().split('\n')

edges = data[:750]
nodes = set()

cy_edges = []
cy_nodes = []

for edge in edges:
    source, target = edge.split(" ")

    if source not in nodes:
        nodes.add(source)
        cy_nodes.append({"data": {"id": source, "label": "User #" + source[-5:]}})
    if target not in nodes:
        nodes.add(target)
        cy_nodes.append({"data": {"id": target, "label": "User #" + target[-5:]}})

    cy_edges.append({
        'data': {
            'source': source,
            'target': target
        }
    })

default_stylesheet = [
    {
        "selector": 'node',
        'style': {
            "opacity": 0.65
        }
    },
    {
        "selector": 'edge',
        'style': {
            "curve-style": "bezier",
            "opacity": 0.65
        }
    },
]

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 80px)'}
}

app.layout = html.Div([
    html.Div(className='eight columns', children=[
        my_dash_component.Cytoscape(
            id='cytoscape',
            elements=cy_edges + cy_nodes,
            style={
                'height': '95vh',
                'width': '100%'
            }
        )
    ]),

    html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs', children=[
            dcc.Tab(label='Control Panel', children=[
                drc.NamedDropdown(
                    name='Layout',
                    id='dropdown-layout',
                    options=drc.DropdownOptionsList(
                        'random',
                        'grid',
                        'circle',
                        'concentric',
                        'breadthfirst',
                        'cose'
                    ),
                    value='random',
                    clearable=False
                ),
            ]),

            dcc.Tab(label='JSON', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Node Object JSON:'),
                    html.Pre(
                        id='tap-node-json-output',
                        style=styles['json-output']
                    ),
                    html.P('Edge Object JSON:'),
                    html.Pre(
                        id='tap-edge-json-output',
                        style=styles['json-output']
                    )
                ])
            ])
        ]),

    ])
])


@app.callback(Output('tap-node-json-output', 'children'),
              [Input('cytoscape', 'tapNode')])
def displayTapNode(data):
    return json.dumps(data, indent=2)


@app.callback(Output('tap-edge-json-output', 'children'),
              [Input('cytoscape', 'tapEdge')])
def displayTapEdge(data):
    return json.dumps(data, indent=2)


@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout}


@app.callback(Output('cytoscape', 'stylesheet'),
              [Input('cytoscape', 'tapNode')])
def generate_stylesheet(node):
    if not node:
        return default_stylesheet

    stylesheet = [{
        "selector": 'node',
        'style': {'opacity': 0.3}
    }, {
        'selector': 'edge',
        'style': {
            'opacity': 0.2,
            "curve-style": "bezier",
        }
    }, {
        "selector": 'node[id = "{}"]'.format(node['data']['id']),
        "style": {
            'background-color': '#B10DC9',
            "border-width": 2,
            "border-color": "purple",
            "border-opacity": 1,
            "opacity": 1,

            "label": "data(label)",
            "color": "#B10DC9",
            "text-opacity": 1,
            "font-size": 12,
            'z-index': 9999
        }
    }]

    for edge in node['edgesData']:
        if edge['source'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['target']),
                "style": {
                    'background-color': '#FF4136',
                    'opacity': 0.9
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-target-arrow-color": "red",
                    "mid-target-arrow-shape": "vee",
                    "line-color": "#FF4136",
                    'opacity': 0.9,
                    'z-index': 5000
                }
            })

        if edge['target'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['source']),
                "style": {
                    'background-color': '#0074D9',
                    'opacity': 0.9,
                    'z-index': 9999
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-target-arrow-color": "blue",
                    "mid-target-arrow-shape": "vee",
                    "line-color": "#0074D9",
                    'opacity': 1,
                    'z-index': 5000
                }
            })

    return stylesheet


if __name__ == '__main__':
    app.run_server(debug=True)
