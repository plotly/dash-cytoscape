import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_cytoscape as cyto

from base64 import b64decode

app = dash.Dash(__name__)
server = app.server
app.scripts.config.serve_locally = True
app.title = 'test-dc'
route = dcc.Location(id='url', refresh=False)

elements = [
    {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}},
    {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
    {'data': {'source': 'one', 'target': 'two', 'label': 'Edge from Node1 to Node2'}},
]

app.layout = html.Div(
    children=[
        route,
        html.H1('My app'),
        html.Button('Get Image', id='button'),
        # Specifying generateImage here should do nothing
        cyto.Cytoscape(
            id='cy',
            elements=elements
        ),
        dcc.Textarea('image-text', value='Image data here'),
    ]
)


@app.callback(
    Output('cy', 'generateImage'),
    [Input('button', 'n_clicks')])
def get_image(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    # Set options here
    return {
        'type': 'png',
    }


@app.callback(
    Output('image-text', 'value'),
    [Input('cy', 'imageData')])
def put_image_string(data):

    if data is not None:
        with open('test_output.png', 'wb') as f:
            f.write(
                b64decode(
                    data.split(',')[1]
                    )
            )

    return data

if __name__ == '__main__':
    app.run_server(debug=False)
