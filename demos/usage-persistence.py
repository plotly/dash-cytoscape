"""
An example to show how to use persistence. After loading data, refreshing
the page should not loose the cytoscape data nor the selection of nodes/edges.
Persistence should be set to:
- local
- session
- memory
Read more about persistence here: https://dash.plotly.com/persistence
"""
import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_cytoscape as cyto
import dash_html_components as html


elements = [
    {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}},
    {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
    {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
]

layout = {'name': 'grid'}

app = dash.Dash(__name__)
app.layout =  html.Div([
    html.Button('Load data', id='bt-load'),
    cyto.Cytoscape(
        id='cytoscape',
        layout=layout,
        # persistence=True
    ),
])

@app.callback(
    Output('cytoscape', 'elements'),
    [Input('bt-load', 'n_clicks')]
)
def load_elements(_):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    return elements

if __name__ == '__main__':
    app.run_server(debug=True)
