import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

cyto.load_extra_layouts()

app = dash.Dash(__name__)


elements = [
    {
        "data": { 
            "id": "1",
            "label": "1",
        }
    },

    {
        "data": { 
            "id": "2",
            "label": "2",
            "parent": "2_parent",
        }
    },

    {
        "data": { 
            "id": "2_parent",
            "label": "2_parent",
        }
    },

    {
        "data": {
            "source": "1",
            "target": "2",
        }
    }
]

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-compound',
        layout={
            "name": "dagre",
            "nodeDimensionsIncludeLabels": True,
            "animate": True,
            "animationDuration": 2000
        },
        style={'width': '50%', 'height': '400px', "background-color": "azure",},
        stylesheet=[
            {
                'selector': 'node',
                'style': {'content': 'data(label)'}
            },
            {
                "selector": "edge",
                "style": {
                    "curve-style": "straight",
                    "target-arrow-shape": "triangle",
                    "arrow-scale": 2,
                },
            },
        ],
        elements=elements,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)