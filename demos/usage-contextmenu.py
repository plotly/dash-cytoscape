import json

import dash
from dash.dependencies import Input, Output
from dash import html

import dash_cytoscape as cyto
cyto.load_extra_layouts()

app = dash.Dash(__name__)
server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

elements = [
    {'data': {'id': 'j', 'name': 'Node1'}},
    {'data': {'id': 'e', 'name': 'Node2'}},
    {'data': {'id': 'k', 'name': 'Node3'}},
    {'data': {'id': 'g', 'name': 'Node4'}},
    {'data': {'source': 'j', 'target': 'e'}},
    {'data': {'source': 'j', 'target': 'k'}},
    {'data': {'source': 'j', 'target': 'g'}},
    {'data': {'source': 'e', 'target': 'j'}},
    {'data': {'source': 'e', 'target': 'k'}},
    {'data': {'source': 'k', 'target': 'j'}},
    {'data': {'source': 'k', 'target': 'e'}},
    {'data': {'source': 'k', 'target': 'g'}},
    {'data': {'source': 'g', 'target': 'j'}}
]

# App
app.layout = html.Div([
    html.Div(
        id="output-div",
        style={
            "position": "absolute",
            "display": "flex",
            "alignItems": "center",
            "zIndex": "10",
        },
        children=[
            html.Button("Toggle Context Menu", id='toggle-button'),
            html.Span(style={"marginLeft": "10px"}, id="output-span"),
        ]
    ),
    cyto.Cytoscape(
        id='cytoscape',
        boxSelectionEnabled=False,
        autounselectify=True,
        elements=elements,
        layout={
            'name': 'grid',
            'padding': 10
        },
        stylesheet=[{
            'selector': 'node',
            'style': {
                'content': 'data(name)',
                'text-valign': 'center',
                'color': 'white',
                'text-outline-width': 2,
                'background-color': '#999',
                'text-outline-color': '#999'
            }
        }, {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'target-arrow-color': '#ccc',
                'line-color': '#ccc',
                'width': 1
            }
        }, {
            'selector': ':selected',
            'style': {
                'background-color': 'black',
                'line-color': 'black',
                'target-arrow-color': 'black',
                'source-arrow-color': 'black'
            }
        }, {
            'selector': 'edge.questionable',
            'style': {
                'line-style': 'dotted',
                'target-arrow-shape': 'diamond'
            }
        }, {
            'selector': '.faded',
            'style': {
                'opacity': 0.25,
                'text-opacity': 0
            }
        }],
        style={
            'width': '100%',
            'height': '100%',
            'position': 'absolute',
            'left': 0,
            'top': 0
        }
    )
])


@app.callback(Output('cytoscape', 'contextmenu'), [Input('toggle-button', 'n_clicks')])
def toggle_contextmenu_options(n_clicks):
    n_clicks = 2 if n_clicks is None else n_clicks
    toggle_on = n_clicks % 2 == 0
    if toggle_on:
        return [
            {
                'selector': '*',
                'content': 'All',
                'id': 'A',
            },
            {
                'selector': 'edge, core',
                'content': 'Edge or Core',
                'id': 'CE',
            },
            {
                'selector': 'node, edge',
                'content': 'Node or Edge',
                'tooltipText': 'This option appears on both nodes and edges',
                'id': 'NE',
            },
            {
                'selector': 'node',
                'content': 'Node Option 1',
                'id': 'N1',
            },
            {
                'selector': 'node',
                'content': '<i>Node Option 2</i>',
                'id': 'N2',
            },
            {
                'selector': 'node',
                'content': 'Node Option 3',
                'id': 'N3',
                'disabled': True
            },
            {
                'selector': 'edge',
                'content': 'Edge Option 1',
                'id': 'E1',
            },
            {
                'selector': 'edge',
                'content': 'Edge Option 2',
                'id': 'E2',
            }
        ]
    return [
        {
            'content': 'Context Menu Change',
            'id': 'CH',
        }
    ]


@app.callback(Output('output-span', 'children'),
              [Input('cytoscape', 'contextmenuData')])
def handleCtxmenuReturn(contextmenuData):
    app.logger.info(json.dumps(contextmenuData, indent=4, sort_keys=True))
    if contextmenuData is None:
        return "Option ID:"
    return "Option ID: " + contextmenuData["id"]


if __name__ == '__main__':
    app.run_server(debug=True)
