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
app.title = "test-dc"
route = dcc.Location(id="url", refresh=False)

elements = [
    {"data": {"id": "one", "label": "Node 1"}, "position": {"x": 50, "y": 50}},
    {"data": {"id": "two", "label": "Node 2"}, "position": {"x": 200, "y": 200}},
    {"data": {"source": "one", "target": "two", "label": "Edge from Node1 to Node2"}},
]

app.layout = html.Div(
    children=[
        route,
        html.H1("My app"),
        html.Button("Get Image as png", id="btn-getPNG"),
        html.Button("Get Image as jpg", id="btn-getJPG"),
        html.Button("Get Image as svg", id="btn-getSVG"),
        cyto.Cytoscape(id="cy", elements=elements)
    ]
)


@app.callback(
    Output("cy", "generateImage"),
    [
        Input("btn-getPNG", "n_clicks"),
        Input("btn-getJPG", "n_clicks"),
        Input("btn-getSVG", "n_clicks"),
    ],
)
def get_image(getPNG_clicks, getJPG_clicks, getSVG_clicks):

    if getPNG_clicks is None and getJPG_clicks is None and getSVG_clicks is None:
        raise PreventUpdate

    ctx = dash.callback_context
    if ctx.triggered:
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        print(input_id)

        ftype = "png"
        if input_id == "btn-getJPG":
            ftype = "jpg"
        elif input_id == "btn-getSVG":
            ftype = "svg"

        # Set options here
        return {
            "type": ftype,
            "action": "download",
        }

if __name__ == "__main__":
    app.run_server(debug=False)
