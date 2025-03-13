import dash
from dash import html, dcc, callback, Input, Output
import dash_cytoscape as cyto
import dash_leaflet as dl


ELEMENTS = [
    {"data": {"id": "a", "label": "Node A", "lat": 45.519, "lon": -73.576}},
    {"data": {"id": "b", "label": "Node B", "lat": 45.521, "lon": -73.574}},
    {"data": {"id": "c", "label": "Node C", "lat": 45.520, "lon": -73.572}},
    {"data": {"id": "ab", "source": "a", "target": "b"}},
]


cyleaflet_leaflet_id = {
    "id": "cyleaflet_tiles_from_callback",
    "component": "cyleaflet",
    "sub": "leaf",
}


def serve_layout():
    return html.Div(
        children=[
            cyto.CyLeaflet(
                id="cyleaflet_tiles_from_callback",
                cytoscape_props={
                    "elements": ELEMENTS,
                },
            ),
            "Max zoom",
            dcc.Input(value=18, type="number", id="max-zoom"),
        ],
    )


app = dash.Dash(__name__)
server = app.server
app.layout = serve_layout


@callback(Output(cyleaflet_leaflet_id, "children"), Input("max-zoom", "value"))
def update_max_zoom(max_zoom):
    return dl.TileLayer(
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png",
        maxZoom=max_zoom,
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    )


if __name__ == "__main__":
    app.run(debug=True)
