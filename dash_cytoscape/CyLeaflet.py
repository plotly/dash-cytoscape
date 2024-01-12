from dash import (
    clientside_callback,
    callback,
    ClientsideFunction,
    Output,
    Input,
    html,
    dcc,
    MATCH,
)

import dash_cytoscape as cyto

try:
    import dash_leaflet as dl
except ImportError:
    dl = None


class CyLeaflet(html.Div):
    def __init__(
        self,
        id,
        cytoscape_props=None,
        leaflet_props=None,
        width="600px",
        height="480px",
    ):
        # Throw error if `dash_leaflet` package is not installed
        if dl is None:
            raise ImportError(
                "dash_leaflet not found. Please install it, either directly (`pip install dash_leaflet`) "
                + "or by using `pip install dash_cytoscape[leaflet]`"
            )

        self.ids = {
            s: {"id": id, "component": "cyleaflet", "sub": s}
            for s in ["cy", "leaf", "elements"]
        }
        self.ids["component"] = "leaflet"
        cytoscape_props = cytoscape_props or {}
        leaflet_props = leaflet_props or {}
        elements = cytoscape_props.get("elements", [])
        cytoscape_props, leaflet_props = self.set_default_props_and_overrides(
            cytoscape_props, leaflet_props
        )

        super().__init__(
            html.Div(
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
                    "width": width,
                    "height": height,
                },
            ),
            style={
                "height": "100%",
                "width": "100%",
                "position": "relative",
            },
        )

    def set_default_props_and_overrides(self, user_cytoscape_props, user_leaflet_props):
        # Props where we want to override values supplied by the user
        # These are props which are required for CyLeaflet to work properly
        cytoscape_overrides = {
            "id": self.ids["cy"],
            "elements": [],  # Elements are set via clientside callback, so set to empty list initially
            "layout": {"name": "preset"},
            "style": {"width": "100%", "height": "100%"},
            "minZoom": 3 / 100000,
        }
        # Note: Leaflet MUST be initialized with a center and zoom to avoid an error,
        # even though these will be immediately overwritten by syncing w/ Cytoscape
        leaflet_overrides = {
            "id": self.ids["leaf"],
            "center": [0, 0],
            "zoom": 6,
            "zoomSnap": 0,
            "zoomControl": False,
            "zoomAnimation": False,
            "maxZoom": 100000,
            "maxBoundsViscosity": 1,
            "maxBounds": [[-85, -180.0], [85, 180.0]],
            "style": {"width": "100%", "height": "100%"},
        }

        # Props where we want to fill in a default value
        # if a value is not supplied by the user
        cytoscape_defaults = {
            "boxSelectionEnabled": True,
            "maxZoom": 1.67,
        }
        leaflet_defaults = {
            "children": dl.TileLayer(),
        }

        # Start with default props
        cytoscape_props = dict(cytoscape_defaults)
        leaflet_props = dict(leaflet_defaults)

        # Update with user-supplied props
        cytoscape_props.update(user_cytoscape_props)
        leaflet_props.update(user_leaflet_props)

        # Update with overrides
        cytoscape_props.update(cytoscape_overrides)
        leaflet_props.update(leaflet_overrides)

        return cytoscape_props, leaflet_props


if dl is not None:
    clientside_callback(
        ClientsideFunction(namespace="cyleaflet", function_name="updateLeafBounds"),
        Output(
            {"id": MATCH, "component": "cyleaflet", "sub": "leaf"}, "invalidateSize"
        ),
        Output({"id": MATCH, "component": "cyleaflet", "sub": "leaf"}, "viewport"),
        Input({"id": MATCH, "component": "cyleaflet", "sub": "cy"}, "extent"),
    )
    clientside_callback(
        ClientsideFunction(namespace="cyleaflet", function_name="transformElements"),
        Output({"id": MATCH, "component": "cyleaflet", "sub": "cy"}, "elements"),
        Input({"id": MATCH, "component": "cyleaflet", "sub": "elements"}, "data"),
    )
