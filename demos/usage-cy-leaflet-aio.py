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

# App
app.layout = html.Div(
    [
        html.Div(
            cyto.CyLeaflet(
                id="my-cy-leaflet",
                cytoscape_props={
                    "elements": [],
                    "stylesheet": cy_stylesheet,
                },
                width=int(default_div_style["width"][:-2]),
                height=int(default_div_style["height"][:-2]),
            ),
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
                dcc.Input(
                    id="width-input",
                    type="number",
                    value=int(default_div_style["width"][:-2]),
                    debounce=True,
                ),
                dcc.Input(
                    id="height-input",
                    type="number",
                    value=int(default_div_style["height"][:-2]),
                    debounce=True,
                ),
            ],
        ),
    ],
)


@callback(
    Output("cy-leaflet-div", "children"),
    Output("cy-leaflet-div", "style"),
    Output(
        {"id": "my-cy-leaflet", "sub": "leaf", "component": "cyleaflet"}, "children"
    ),
    Input("location-dropdown", "value"),
    Input("width-input", "value"),
    Input("height-input", "value"),
)
def update_location(location, width, height):
    d = 0.001
    d2 = 0.0001
    lat, lon = city_lat_lon[location]
    new_elements = [
        {"data": {"id": "a", "label": "Node A", "lat": lat - d, "lon": lon - d}},
        {"data": {"id": "b", "label": "Node B", "lat": lat + d, "lon": lon + d}},
        {"data": {"id": "c", "label": "Node C", "lat": lat + d - d2, "lon": lon + d}},
        {"data": {"id": "ab", "source": "a", "target": "b"}},
    ]
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
    leaflet_children = [dl.TileLayer()] + markers
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
    Input({"id": "my-cy-leaflet", "sub": "leaf", "component": "cyleaflet"}, "bounds"),
    Input({"id": "my-cy-leaflet", "sub": "cy", "component": "cyleaflet"}, "extent"),
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
    app.run_server(debug=True)
