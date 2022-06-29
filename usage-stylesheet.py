import json
from typing import List, Any

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto
from demos import dash_reusable_components as drc
from random import randint

app = dash.Dash(__name__)
server = app.server

# ###################### DATA PREPROCESSING ######################
# Load data
with open('demos/data/sample_network.txt', 'r') as f:
    network_data = f.read().split('\n')

# We select the first 750 edges and associated nodes for an easier visualization
edges = network_data[:50]
nodes = set()

cy_edges = []
cy_nodes = []

for network_edge in edges:
    source, target = network_edge.split(" ")

    if source not in nodes:
        nodes.add(source)
        cy_nodes.append({"data": {"id": source,
                                  "label": "Контракт #" + source[-5:]}})
    if target not in nodes:
        nodes.add(target)
        cy_nodes.append({"data": {"id": target,
                                  "label": "Контракт #" + target[-5:]}})

    cy_edges.append({
        'data': {
            'source': source,
            'target': target,
            'weight': randint(-100, 100)
        }
    })

default_stylesheet = [
    {
        "selector": 'node',
        'style': {
            "opacity": 0.65,
        }
    },
    {
        "selector": 'edge',
        'style': {
            "curve-style": "bezier",
            "opacity": 0.65,
            "mid-target-arrow-shape": "tee",
        }
    },
    {
      "selector": "[weight > 50]",
      "style": {
            "mid-target-arrow-color": "red",
            "mid-target-arrow-shape": f"tee-{1}"
      }
    },
{
      "selector": "[weight < 0]",
      "style": {
            "mid-target-arrow-color": "blue",
            "mid-target-arrow-shape": f"tee-{5}"
      }
    }
]

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {
        'height': 'calc(98vh - 105px)'
    }
}

app.layout = html.Div([
    html.Div(className='eight columns', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=cy_edges + cy_nodes,
            style={
                'height': '95vh',
                'width': '100%'
            },
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
                    value='grid',
                    clearable=False
                ),

                drc.NamedDropdown(
                    name='Node Shape',
                    id='dropdown-node-shape',
                    value='ellipse',
                    clearable=False,
                    options=drc.DropdownOptionsList(
                        'ellipse',
                        'triangle',
                        'rectangle',
                        'diamond',
                        'pentagon',
                        'hexagon',
                        'heptagon',
                        'octagon',
                        'star',
                        'polygon',
                    )
                ),

                drc.NamedDropdown(
                    name='Засечка',
                    id='dropdown-edge-arrow',
                    value='tee-1',
                    clearable=False,
                    options=drc.DropdownOptionsList(
                        'triangle',
                        'triangle-tee',
                        'circle-triangle',
                        'triangle-cross',
                        'triangle-backcurve',
                        'vee',
                        'tee-1',
                        'tee-2',
                        'tee-3',
                        'tee-4',
                        'tee-5',
                        'square',
                        'circle',
                        'diamond',
                        'chevron',
                        'none'
                    )
                ),

                drc.NamedInput(
                    name='Followers Color',
                    id='input-follower-color',
                    type='text',
                    value='#0074D9',
                ),

                drc.NamedInput(
                    name='Following Color',
                    id='input-following-color',
                    type='text',
                    value='#FF4136',
                ),
            ]),

            dcc.Tab(label='JSON', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Drag Node JSON:'),
                    html.Pre(
                        id='drag-node-json-output',
                        style=styles['json-output']
                    )
                ])
            ])
        ]),
    ])
])



@app.callback(Output('drag-node-json-output', 'children'),
              [Input('cytoscape', 'grabNodeData'),
               Input('cytoscape', 'dragNodeData')])
def display_drag_node(dragData, grabData):
    data = {}
    if grabData and dragData:
        data = {**grabData, **dragData}
    print(data)
    return json.dumps(data, indent=2)

@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout}


# засечки применяются при нажатии на узел
@app.callback(Output('cytoscape', 'stylesheet'),
              [Input('cytoscape', 'tapNode'),
               Input('input-follower-color', 'value'),
               Input('input-following-color', 'value'),
               Input('dropdown-edge-arrow', 'value'),
               Input('dropdown-node-shape', 'value')])
def generate_stylesheet(node, follower_color, following_color, edge_arrow, node_shape):
    if not node:
        return default_stylesheet

    stylesheet = [{
        "selector": 'node',
        'style': {
            'opacity': 0.3,
            'shape': node_shape
        }
    }, {
        'selector': 'edge',
        'style': {
            'opacity': 0.2,
            "mid-target-arrow-shape": edge_arrow,
            "curve-style": "bezier",
        }
    }]

    for edge in node['edgesData']:
        if edge['source'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['target']),
                "style": {
                    'background-color': following_color,
                    'opacity': 0.9
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-target-arrow-color": "black",
                    "mid-target-arrow-shape": edge_arrow,
                    "line-color": following_color,
                    'opacity': 0.9,
                    'z-index': 5000
                }
            })

        if edge['target'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['source']),
                "style": {
                    'background-color': follower_color,
                    'opacity': 0.9,
                    'z-index': 9999
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-target-arrow-color": "black",
                    "mid-target-arrow-shape": edge_arrow,
                    "line-color": follower_color,
                    'opacity': 1,
                    'z-index': 5000
                }
            })

    return stylesheet


if __name__ == '__main__':
    app.run_server(debug=True)
