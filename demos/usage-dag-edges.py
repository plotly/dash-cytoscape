import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from dash_cytoscape.utils import Tree
import dash_cytoscape as cyto

import demos.dash_reusable_components as drc


def flatten(z):
    return [x for y in z for x in y]


app = dash.Dash(__name__)
server = app.server

# Define a tree in the adjacency list format
tree = Tree('a', [
    Tree('b', [
        Tree('c'),
        Tree('d')
    ]),
    Tree('e', [
        Tree('g')
    ]),
    Tree('f'),
    Tree('h', [
        Tree('i', [
            Tree('j')
        ])
    ])
])

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
        elements=tree.get_elements(),
        layout={
            'name': 'breadthfirst',
            'roots': ['a']
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
