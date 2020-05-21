import json

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
    {'data': {'id': 'j', 'name': 'Jerry'}},
    {'data': {'id': 'e', 'name': 'Elaine'}},
    {'data': {'id': 'k', 'name': 'Kramer'}},
    {'data': {'id': 'g', 'name': 'George'}},
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
    html.P(
        id="output-div",
        style={
            "position": "fixed",
            "width": "100%",
            "height": "50%",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center"

        },
        children=["Option Id:"]
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
        ctxmenu=[
            {
                'selector': 'node',
                'commands': [
                    {
                        'content': 'Node Option 1',
                        'id': '1',
                        'format': [
                            "position",
                            {'key': 'position', 'props': ['x']},
                            "group"
                        ]
                    },
                    {
                        'content': 'Node Option 2',
                        'id': '2'
                    },
                    {
                        'content': '<i>Node Option 3</i>',
                        'id': '3',
                        'enabled': False
                    }
                ]
            },
            {
                'selector': 'core',
                'commands': [
                    {
                        'content': 'Core 1',
                        'id': 'a',
                        'format': [
                            "pan",
                            "zoom",
                            {
                                'key': 'elements',
                                'props': [
                                    'node',
                                    'nodes',
                                    {
                                        'key': 'edges',
                                        'filter': {
                                            'data': {
                                                'source': 'j'
                                            }
                                        },
                                        'props': [
                                            'data',
                                            {
                                                'key': 'position',
                                                'props': ['x']
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'content': 'Core 2',
                        'id': 'b'
                    }
                ]
            },
            {
                'selector': 'edge',
                'commands': [
                    {
                        'content': 'Edge 1',
                        'id': 'x'
                    },
                    {
                        'content': 'Edge 2',
                        'id': 'y'
                    }
                ]
            }
        ],
        style={
            'width': '100%',
            'height': '100%',
            'position': 'absolute',
            'left': 0,
            'top': 0
        }
    )
])

@app.callback(Output('output-div', 'children'),
              [Input('cytoscape', 'ctxmenuData')])
def handleCtxmenuReturn(ctxmenuData):
    app.logger.info(json.dumps(ctxmenuData, indent=4, sort_keys=True))
    if ctxmenuData is None:
        return "Option Id:"
    return "Option Id: " + ctxmenuData["id"]

if __name__ == '__main__':
    app.run_server(debug=True)
