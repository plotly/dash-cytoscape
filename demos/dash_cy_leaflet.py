from dash import (
    clientside_callback,
    ClientsideFunction,
    Output,
    Input,
    State,
    html,
    dcc,
)

import dash_cytoscape as cyto
import dash_leaflet as dl


class DashCyLeaflet(html.Div):
    def __init__(self, id, cytoscape_props=None, leaflet_props=None):
        cytoscape_props = cytoscape_props or {}
        leaflet_props = leaflet_props or {}
        elements = cytoscape_props["elements"]
        self.ids = {
            s: {"id": id, "sub": s}
            for s in ["cy", "leaf", "elements-store", "avg-coor-store"]
        }
        cytoscape_props = dict(
            cytoscape_props,
            id=self.ids["cy"],
            elements=[],
            boxSelectionEnabled=True,
            layout={"name": "preset"},
            style={
                "width": "100%",
                "height": "100%",
            },
            maxZoom=5,
            minZoom=3 / 100000,
        )
        leaflet_props = dict(
            leaflet_props,
            id=self.ids["leaf"],
            children=dl.TileLayer(),
            zoomSnap=0,
            zoomControl=False,
            zoomAnimation=False,
            inertia=False,
            maxZoom=100000,
            maxBoundsViscosity=1,
            maxBounds=[[-85, -180.0], [85, 180.0]],
            style={"width": "100%", "height": "100%"},
        )

        def find_average_lat_lon(elements):
            # Variables to store the total latitudes and longitudes
            total_lat = 0
            total_lon = 0

            # Count of elements with valid latitudes and longitudes
            count = 0

            # Loop through the elements list
            for element in elements:
                if (
                    "data" in element
                    and "lat" in element["data"]
                    and "lon" in element["data"]
                ):
                    total_lat += element["data"]["lat"]
                    total_lon += element["data"]["lon"]
                    count += 1

            # Calculate the average latitude and longitude
            average_lat = total_lat / count if count > 0 else 0.01
            average_lon = total_lon / count if count > 0 else 0.01

            return {"averageLat": average_lat, "averageLon": average_lon}

        avg_coordinates = find_average_lat_lon(elements)

        super().__init__(
            [
                html.Div(
                    cyto.Cytoscape(**cytoscape_props),
                    style={
                        "height": "100%",
                        "width": "100%",
                        "position": "absolute",
                        "top": 0,
                        "left": 0,
                        "zIndex": 2,
                    },
                ),
                html.Div(
                    dl.Map(**leaflet_props),
                    style={
                        "height": "100%",
                        "width": "100%",
                        "position": "absolute",
                        "top": 0,
                        "left": 0,
                        "zIndex": 1,
                    },
                ),
                dcc.Store(id=self.ids["elements-store"], data=elements),
                dcc.Store(id=self.ids["avg-coor-store"], data=avg_coordinates),
            ],
            style={
                "height": "100%",
                "width": "100%",
                "position": "relative",
            },
        )
        self.add_clientside_callbacks()

    def add_clientside_callbacks(self):
        clientside_callback(
            ClientsideFunction(
                namespace="clientside", function_name="updateLeafBoundsAIO"
            ),
            Output(self.ids["leaf"], "bounds"),
            Input(self.ids["cy"], "extent"),
            State(self.ids["avg-coor-store"], "data"),
        )
        clientside_callback(
            ClientsideFunction(
                namespace="clientside", function_name="transformElements"
            ),
            Output(self.ids["cy"], "elements"),
            Input(self.ids["elements-store"], "data"),
        )
