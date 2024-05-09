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

# Create an instance of CyLeaflet
cyleaflet_instance = cyto.CyLeaflet(
    id="cyleaflet_tiles_from_callback",
    cytoscape_props={
        "elements": ELEMENTS,
    },
)


def serve_layout():
    return html.Div(
        children=[
            html.Div("Tiles dropdown"),
            dcc.Dropdown(
                id="tiles_dropdown",
                options=[{"label": x, "value": x} for x in ["OSM", "CARTO"]],
                value="CARTO",
            ),
            cyleaflet_instance,
        ],
    )


app = dash.Dash(__name__)
server = app.server
app.layout = serve_layout


@callback(
    Output(cyleaflet_instance.LEAFLET_ID, "children"),
    Input("tiles_dropdown", "value"),
)
def update_tiles(tiles):
    if tiles == "OSM":
        return cyto.CyLeaflet.OSM
    return CARTO_TILES


if __name__ == "__main__":
    app.run_server(debug=True)
