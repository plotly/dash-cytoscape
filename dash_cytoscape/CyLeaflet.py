from dash import (
    clientside_callback,
    ClientsideFunction,
    Output,
    Input,
    html,
    dcc,
)

import dash_cytoscape as cyto
import dash_leaflet as dl


class CyLeaflet(html.Div):
    def __init__(self, id, cytoscape_props=None, leaflet_props=None):
        cytoscape_props = cytoscape_props or {}
        leaflet_props = leaflet_props or {}
        elements = cytoscape_props["elements"]
        self.ids = {s: {"id": id, "sub": s} for s in ["cy", "leaf", "elements"]}
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
            contextMenu=[
                {
                    "id": "add-node",
                    "label": "Add Node (JS)",
                    "tooltipText": "Add Node",
                    "onClick": "add_node",
                    "availableOn": ["canvas"],
                },
                {
                    "id": "remove",
                    "label": "Remove (JS)",
                    "tooltipText": "Remove",
                    "availableOn": ["node", "edge"],
                    "onClick": "remove",
                },
                {
                    "id": "add-edge",
                    "label": "Add Edge (JS)",
                    "tooltipText": "add edge",
                    "availableOn": ["node"],
                    "onClick": "add_edge",
                },
            ],
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
                dcc.Store(id=self.ids["elements"], data=elements),
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
                namespace="cyleaflet", function_name="updateLeafBoundsAIO"
            ),
            Output(self.ids["leaf"], "viewport"),
            Input(self.ids["cy"], "extent"),
        )
        clientside_callback(
            ClientsideFunction(
                namespace="cyleaflet", function_name="transformElements"
            ),
            Output(self.ids["cy"], "elements"),
            Input(self.ids["elements"], "data"),
        )
