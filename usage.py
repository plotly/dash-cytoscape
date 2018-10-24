import dash_cytoscape
import dash
from dash.dependencies import Input, Output
import dash_html_components as html

app = dash.Dash('')

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

# Dictionary declaration
elements_dict = [
    {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}},
    {'data': {'id': 'two', 'label': 'Node 2'},
     'position': {'x': 200, 'y': 200}},
    {'data': {'source': 'one', 'target': 'two',
              'label': 'Edge from Node1 to Node2'}}
]

app.layout = html.Div([
    dash_cytoscape.Cytoscape(
        id='cytoscape',
        elements=elements_dict,
        layout={
            'name': 'preset'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
