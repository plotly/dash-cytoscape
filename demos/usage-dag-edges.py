import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

import demos.dash_reusable_components as drc


def flatten(z):
    return [x for y in z for x in y]


app = dash.Dash(__name__)
server = app.server

# Define a tree in the adjacency list format
adj_dict = {
    'root': ['l', 'r'],
    'l': ['ll', 'lr'],
    'r': ['rl', 'rr'],
    'll': ['lll', 'llr'],
    'rr': ['rrl', 'rrr']
}

# Flatten values, then only keep the unique entries
node_ids = list(set(flatten(adj_dict.values()))) + ['root']

nodes = [{'data': {'id': node_id}} for node_id in node_ids]
edges = flatten([
    [
        {'data': {'source': src, 'target': tar}}
        for tar in adj_dict[src]
    ]
    for src in adj_dict
])

elements = nodes + edges

# Start the app
app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-edge-style',
        options=drc.DropdownOptionsList(
            'bezier',
            'taxi',
            'unbundled-bezier',
            'loop',
            'haystack',
            'segments',
            'straight'
        ),
        value='bezier',
        clearable=False
    ),
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={
            'name': 'breadthfirst',
            'roots': ['root']
        },
        style={
            'height': '95vh',
            'width': '100%'
        }
    )
])


@app.callback(Output('cytoscape', 'stylesheet'),
              [Input('dropdown-edge-style', 'value')])
def update_edge_style(style):
    return [
        {
            'selector': 'edge',
            'style': {
                'curve-style': style
            }
        }
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
