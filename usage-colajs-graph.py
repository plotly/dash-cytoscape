import my_dash_component
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import json

app = dash.Dash(__name__)
server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
#
# with open('data/colajs-graph/data.json', 'r') as f:
#     elements = json.loads(f.read())


app.layout = html.Div([
    html.Div(className='row', children=[
        html.Div(className='eight columns', children=[
            my_dash_component.Cytoscape(
                id='cytoscape',
                style={'height': '98vh'},
                layout='random'
            )
        ]),

        html.Div(className='four columns', children=[
            dcc.Dropdown(
                id='dropdown-dataset',
                options=[
                    {'label': 'Demo with Cola.js', 'value': 'colajs-graph'},
                    # {'label': 'Tokyo Railway map', 'value': 'tokyo-railway'},
                    # {'label': 'Wine and Cheese', 'value': 'wineandcheese'},
                    {'label': 'Spread Layout', 'value': 'spread-layout'}
                ],
                value='colajs-graph',
            )
        ])
    ]),
])


@app.callback(Output('cytoscape', 'elements'),
              [Input('dropdown-dataset', 'value')])
def update_cytoscape_elements(dataset):
    if dataset is None:
        return [
            {'data': {'id': 'one', 'label': 'Node 1'},
             'position': {'x': 50, 'y': 50}},
            {'data': {'id': 'two', 'label': 'Node 2'},
             'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two',
                      'label': 'Edge from Node1 to Node2'}}
        ]

    with open(f'data/{dataset}/data.json', 'r') as f:
        elements = json.loads(f.read())

    print('Data updated.')
    return elements


@app.callback(Output('cytoscape', 'stylesheet'),
              [Input('dropdown-dataset', 'value')])
def update_cytoscape_stylesheet(dataset):
    if dataset is None:
        return {}

    with open(f'data/{dataset}/cy-style.json', 'r') as f:
        stylesheet = json.loads(f.read())

    print('Style Updated.')
    return stylesheet


if __name__ == '__main__':
    app.run_server(debug=True)
