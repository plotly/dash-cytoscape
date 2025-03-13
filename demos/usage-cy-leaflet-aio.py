import dash
from dash import (
    html,
    callback,
    Input,
    Output,
    dcc,
)
import dash_cytoscape as cyto
import dash_leaflet as dl
import random

cyto.load_extra_layouts()

app = dash.Dash(__name__)
server = app.server


cy_stylesheet = [
    {"selector": "node", "style": {"width": "20px", "height": "20px"}},
    {"selector": "edge", "style": {"width": "10px"}},
    {"selector": "node", "style": {"label": "data(label)"}},
]

default_div_style = {
    "height": "650px",
    "width": "800px",
    "border": "2px solid gray",
    "padding": "10px",
    "margin": "5px",
}

location_options = [
    {"label": x, "value": x}
    for x in [
        "Montreal",
        "Reykjavik",
        "Punta Arenas",
        "Quito",
        "Santa Cruz de Tenerife",
        "Gold Coast",
    ]
]

city_lat_lon = {
    "Montreal": (45.52028867870132, -73.5757529436986),
    "Reykjavik": (64.14536852496903, -21.930855990003625),
    "Punta Arenas": (-53.16155139684391, -70.90581697003078),
    "Quito": (-0.181573087774938, -78.48203920834054),
    "Santa Cruz de Tenerife": (28.4636, -16.2518),
    "Gold Coast": (-28.026901440211205, 153.4208293956674),
}

# Create an instance of CyLeaflet
cyleaflet_instance = cyto.CyLeaflet(
    id="my-cy-leaflet",
    cytoscape_props={
        "elements": [],
        "stylesheet": cy_stylesheet,
    },
    width=int(default_div_style["width"][:-2]),
    height=int(default_div_style["height"][:-2]),
)


# App
app.layout = html.Div(
    [
        html.Div(
            cyleaflet_instance,
            id="cy-leaflet-div",
            style=default_div_style,
        ),
        html.Div(id="bounds-display"),
        html.Div(id="extent-display"),
        html.Div(
            [
                "Settings",
                dcc.Dropdown(
                    id="location-dropdown",
                    options=location_options,
                    value=location_options[0]["value"],
                ),
                "Width",
                dcc.Input(
                    id="width-input",
                    type="number",
                    value=int(default_div_style["width"][:-2]),
                    debounce=True,
                ),
                "Height",
                dcc.Input(
                    id="height-input",
                    type="number",
                    value=int(default_div_style["height"][:-2]),
                    debounce=True,
                ),
                "Max zoom",
                dcc.Input(id="max-zoom", type="number", value=18, debounce=True),
                "Number of Nodes",
                dcc.Input(id="n-nodes", type="number", value=4, debounce=True),
            ],
        ),
        html.Div(id="elements"),
    ],
)


@callback(Output("elements", "children"), Input(cyleaflet_instance.ELEMENTS_ID, "data"))
def show_elements(elements):
    return str(elements)


def generate_elements(n_nodes, location):
    d = 0.00005
    lat, lon = city_lat_lon[location]
    if n_nodes < 2:
        n_nodes = 2
    elif n_nodes > 10000:
        n_nodes = 10000

    elements = []
    for i in range(n_nodes):
        rand_lat, rand_lon = random.randint(-5, 5) * i, random.randint(-5, 5) * i
        elements.append(
            {
                "data": {
                    "id": f"{i}",
                    "label": f"Node {i}",
                    "lat": lat + d * rand_lat,
                    "lon": lon + d * rand_lon,
                }
            }
        )
    elements.append({"data": {"id": "0-1", "source": "0", "target": "1"}})
    return elements


@callback(
    Output(cyleaflet_instance.CYTOSCAPE_ID, "elements", allow_duplicate=True),
    Input("n-nodes", "value"),
    Input("location-dropdown", "value"),
    prevent_initial_call=True,
)
def control_number_nodes(n_nodes, location):
    return generate_elements(n_nodes, location)


@callback(
    Output("cy-leaflet-div", "children"),
    Output("cy-leaflet-div", "style"),
    Output(cyleaflet_instance.LEAFLET_ID, "children"),
    Input("location-dropdown", "value"),
    Input("width-input", "value"),
    Input("height-input", "value"),
    Input("max-zoom", "value"),
)
def update_location(location, width, height, max_zoom):
    new_elements = generate_elements(4, location)
    markers = [
        dl.Marker(
            position=[e["data"]["lat"], e["data"]["lon"]],
            children=[
                dl.Tooltip(
                    "(" + str(e["data"]["lat"]) + ", " + str(e["data"]["lon"]) + ")"
                ),
            ],
        )
        for e in new_elements
        if "lat" in e["data"]
    ]
    leaflet_children = [dl.TileLayer(maxZoom=max_zoom)] + markers
    new_style = dict(default_div_style)
    new_style["width"] = str(width) + "px" if width else default_div_style["width"]
    new_style["height"] = str(height) + "px" if height else default_div_style["height"]
    return (
        cyto.CyLeaflet(
            id="my-cy-leaflet",
            cytoscape_props={
                "elements": new_elements,
                "stylesheet": cy_stylesheet,
            },
            width=width,
            height=height,
        ),
        new_style,
        leaflet_children,
    )


@callback(
    Output("bounds-display", "children"),
    Output("extent-display", "children"),
    Input(cyleaflet_instance.LEAFLET_ID, "bounds"),
    Input(cyleaflet_instance.CYTOSCAPE_ID, "extent"),
)
def display_leaf_bounds(bounds, extent):
    bounds = (
        [
            [f"{bounds[0][0]:.5f}", f"{bounds[0][1]:.5f}"],
            [f"{bounds[1][0]:.5f}", f"{bounds[1][1]:.5f}"],
        ]
        if bounds
        else None
    )
    extent = (
        [
            [f"{-extent['y2']/ 100000:.5f}", f"{extent['x1']/ 100000:.5f}"],
            [f"{-extent['y1']/ 100000:.5f}", f"{extent['x2']/ 100000:.5f}"],
        ]
        if extent
        else None
    )
    # extent = {k: v / 100000 for k, v in extent.items() if k in {"x1", "x2", "y1", "y2"}}

    return [
        "Leaflet bounds:" + str(bounds),
        "Cy extent:" + str(extent),
    ]


if __name__ == "__main__":
    app.run(debug=True)
