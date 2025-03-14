import dash
from dash import html, dcc, callback, Input, Output
import dash_cytoscape as cyto
import dash_leaflet as dl

CARTO_TILES = dl.TileLayer(
    url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png",
    maxZoom=19,
    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
)

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
            html.Div("Tiles dropdown"),
            dcc.Dropdown(
                id="tiles_dropdown",
                options=[{"label": x, "value": x} for x in ["OSM", "CARTO"]],
                value="CARTO",
            ),
            cyto.CyLeaflet(
                id="cyleaflet_tiles_from_callback",
                cytoscape_props={"elements": ELEMENTS},
                leaflet_props={"zoomSnap": 1},
            ),
            html.Div(id="zoom"),
        ],
    )


app = dash.Dash(__name__)
server = app.server
app.layout = serve_layout


@callback(
    Output(cyleaflet_leaflet_id, "children"),
    Input("tiles_dropdown", "value"),
)
def update_tiles(tiles):
    if tiles == "OSM":
        return cyto.CyLeaflet.OSM
    return CARTO_TILES


@callback(
    Output("zoom", "children"),
    Input(cyleaflet_leaflet_id, "zoom"),
)
def update_zoom(zoom):
    return zoom


if __name__ == "__main__":
    app.run(debug=True)
