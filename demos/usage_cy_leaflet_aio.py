import dash
from dash import (
    html,
    callback,
    clientside_callback,
    ClientsideFunction,
    Input,
    Output,
    State,
    dcc,
)
import dash_cytoscape as cyto
import dash_leaflet as dl
from dash_cy_leaflet import DashCyLeaflet

cyto.load_extra_layouts()

app = dash.Dash(__name__)
server = app.server


cy_stylesheet = [
    {"selector": "node", "style": {"width": "20px", "height": "20px"}},
    {"selector": "edge", "style": {"width": "10px"}},
    {"selector": "node", "style": {"label": "data(label)"}},
]

default_div_style = {
    "height": "600px",
    "width": "800px",
    "border": "2px solid gray",
    "padding": "10px",
    "margin": "5px",
}

location_options = [
    {"label": x, "value": x}
    for x in [
        "Nort of Montreal",
        "Montreal",
        "Reykjavik",
        "Punta Arenas",
        "Quito",
        "Santa Cruz de Tenerife",
        "Gold Coast",
    ]
]

city_lat_lon = {
    "Nort of Montreal": (
        80,
        -73.5757529436986,
    ),  # poco y: 0.4942222 , 0.59125 ------ -0.65
    "Montreal": (
        45.52028867870132,
        -73.5757529436986,
    ),  # poco y: 0.4942222 , 0.59125 ------ 0.4
    "Reykjavik": (
        64.14536852496903,
        -21.930855990003625,
    ),  # poco x: 0.287273, 0.87815 ----- -0.131 lat
    "Punta Arenas": (
        -53.16155139684391,
        -70.90581697003078,
    ),  # poco mas x: 0.4093, 0.6061 ------  0.2 lat
    "Quito": (
        -0.181573087774938,
        -78.48203920834054,
    ),  # poco mas y: 0.9980, 0.5639 ------ 1 lat
    "Santa Cruz de Tenerife": (
        28.4636,
        -16.2518,
    ),  # bastante y: 0.68373, 0.9097 ----- 0.75 lat
    "Gold Coast": (
        -28.026901440211205,
        153.4208293956674,
    ),  # bastante x: 0.68859, 0.14765 ------ 0.75 lon
}

# App
app.layout = html.Div(
    [
        html.Div(
            DashCyLeaflet(
                id="my-cy-leaflet",
                cytoscape_props=dict(
                    elements=[],
                    stylesheet=cy_stylesheet,
                ),
            ),
            id="cy-leaflet-div",
            style=default_div_style,
        ),
        html.Div(id="bounds-display"),
        html.Div(
            [
                "Settings",
                dcc.Dropdown(
                    id="location-dropdown",
                    options=location_options,
                    value=location_options[0]["value"],
                ),
            ],
        ),
    ],
)


@callback(
    Output("cy-leaflet-div", "children"),
    Input("location-dropdown", "value"),
)
def update_location(location):
    d = 0.01
    d2 = 0.001
    lat, lon = city_lat_lon[location]
    new_elements = [
        {"data": {"id": "a", "label": "Node A", "lat": lat - d, "lon": lon - d}},
        {"data": {"id": "b", "label": "Node B", "lat": lat + d, "lon": lon + d}},
        {"data": {"id": "c", "label": "Node C", "lat": lat + d - d2, "lon": lon + d}},
        {"data": {"id": "ab", "source": "a", "target": "b"}},
    ]
    return DashCyLeaflet(
        id="my-cy-leaflet",
        cytoscape_props=dict(
            elements=new_elements,
            stylesheet=cy_stylesheet,
        ),
    )


@callback(
    Output("bounds-display", "children"),
    Input({"id": "my-cy-leaflet", "sub": "leaf"}, "bounds"),
)
def display_leaf_bounds(bounds):
    return "Leaflet bounds:" + str(bounds)


if __name__ == "__main__":
    app.run_server(debug=True)
