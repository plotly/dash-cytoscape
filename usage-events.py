import json

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server

# Object declaration
basic_elements = [
    {
        'data': {'id': 'one', 'label': 'Node 1'},
        'position': {'x': 50, 'y': 50}
    },
    {
        'data': {'id': 'two', 'label': 'Node 2'},
        'position': {'x': 400, 'y': 50}
    },
    {
        'data': {'id': 'three', 'label': 'Node 3'},
        'position': {'x': 400, 'y': 400}
    },
    {
        'data': {'id': 'four', 'label': 'Node 4'},
        'position': {'x': 50, 'y': 400}
    },
    {
        'data': {'id': 'five', 'label': 'Node 5'},
        'position': {'x': 150, 'y': 225}
    },
    {
        'data': {'id': 'six', 'label': 'Node 6'},
        'position': {'x': 300, 'y': 225}
    },
    {
        'data': {
            'id': 'one-two',
            'source': 'one',
            'target': 'two',
            'label': 'Edge from Node1 to Node2'
        }
    },
    {
        'data': {
            'id': 'one-four',
            'source': 'one',
            'target': 'four',
            'label': 'Edge from Node1 to Node4'
        }
    },
    {
        'data': {
            'id': 'one-five',
            'source': 'one',
            'target': 'five',
            'label': 'Edge from Node1 to Node5'
        }
    },
    {
        'data': {
            'id': 'two-three',
            'source': 'two',
            'target': 'three',
            'label': 'Edge from Node2 to Node3'
        }
    },
    {
        'data': {
            'id': 'two-six',
            'source': 'two',
            'target': 'six',
            'label': 'Edge from Node2 to Node6'
        }
    },
    {
        'data': {
            'id': 'three-four',
            'source': 'three',
            'target': 'four',
            'label': 'Edge from Node3 to Node4'
        }
    },
    {
        'data': {
            'id': 'three-six',
            'source': 'three',
            'target': 'six',
            'label': 'Edge from Node3 to Node6'
        }
    },
    {
        'data': {
            'id': 'four-five',
            'source': 'four',
            'target': 'five',
            'label': 'Edge from Node4 to Node5'
        }
    },
    {
        'data': {
            'id': 'five-six',
            'source': 'five',
            'target': 'six',
            'label': 'Edge from Node5 to Node6'
        }
    },
]

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 115px)'}
}

app.layout = html.Div([
    html.Div(className='eight columns', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=basic_elements,
            layout={
                'name': 'preset'
            },
            style={
                'height': '95vh',
                'width': '100%'
            }
        )
    ]),

    html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs', children=[
            dcc.Tab(label='Tap Objects', children=[
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
            ]),

            dcc.Tab(label='Tap Data', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Node Data JSON:'),
                    html.Pre(
                        id='tap-node-data-json-output',
                        style=styles['json-output']
                    ),
                    html.P('Edge Data JSON:'),
                    html.Pre(
                        id='tap-edge-data-json-output',
                        style=styles['json-output']
                    )
                ])
            ]),

            dcc.Tab(label='Mouseover Data', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Node Data JSON:'),
                    html.Pre(
                        id='mouseover-node-data-json-output',
                        style=styles['json-output']
                    ),
                    html.P('Edge Data JSON:'),
                    html.Pre(
                        id='mouseover-edge-data-json-output',
                        style=styles['json-output']
                    )
                ])
            ]),
            dcc.Tab(label='Selected Data', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Node Data JSON:'),
                    html.Pre(
                        id='selected-node-data-json-output',
                        style=styles['json-output']
                    ),
                    html.P('Edge Data JSON:'),
                    html.Pre(
                        id='selected-edge-data-json-output',
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


@app.callback(Output('tap-node-data-json-output', 'children'),
              [Input('cytoscape', 'tapNodeData')])
def displayTapNodeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('tap-edge-data-json-output', 'children'),
              [Input('cytoscape', 'tapEdgeData')])
def displayTapEdgeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('mouseover-node-data-json-output', 'children'),
              [Input('cytoscape', 'mouseoverNodeData')])
def displayMouseoverNodeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('mouseover-edge-data-json-output', 'children'),
              [Input('cytoscape', 'mouseoverEdgeData')])
def displayMouseoverEdgeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('selected-node-data-json-output', 'children'),
              [Input('cytoscape', 'selectedNodeData')])
def displaySelectedNodeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('selected-edge-data-json-output', 'children'),
              [Input('cytoscape', 'selectedEdgeData')])
def displaySelectedEdgeData(data):
    return json.dumps(data, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
