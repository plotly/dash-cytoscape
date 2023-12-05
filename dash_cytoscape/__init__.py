from __future__ import print_function as _

import os as _os
import sys as _sys
import json

import dash as _dash

# noinspection PyUnresolvedReferences
from ._imports_ import *
from ._imports_ import __all__
from . import utils

# Import CyLeaflet AIO component
from .CyLeaflet import CyLeaflet


if not hasattr(_dash, "__plotly_dash") and not hasattr(_dash, "development"):
    print(
        "Dash was not successfully imported. "
        "Make sure you don't have a file "
        'named \n"dash.py" in your current directory.',
        file=_sys.stderr,
    )
    _sys.exit(1)

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, "package.json"))
with open(_filepath) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")
__version__ = package["version"]

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]


_js_dist = [
    {
        "relative_package_path": "dash_cytoscape.min.js",
        "dev_package_path": "dash_cytoscape.dev.js",
        "external_url": "https://unpkg.com/dash-cytoscape@{2}/{1}/{1}.min.js".format(
            package_name, __name__, __version__
        ),
        "namespace": package_name,
    }
]

_css_dist = []


for _component in __all__:
    setattr(locals()[_component], "_js_dist", _js_dist)
    setattr(locals()[_component], "_css_dist", _css_dist)


def load_extra_layouts():
    """
    Load 3rd party layouts that are not included by default with Cytoscape. You can find the
    documentation about those layouts here:
        - `cose-bilkent`: https://github.com/cytoscape/cytoscape.js-cose-bilkent
        - `cola`: https://github.com/cytoscape/cytoscape.js-cola
        - `euler`: https://github.com/cytoscape/cytoscape.js-dagre
        - `spread`: https://github.com/cytoscape/cytoscape.js-spread
        - `dagre`: https://github.com/cytoscape/cytoscape.js-dagre
        - `klay`: https://github.com/cytoscape/cytoscape.js-klay

    Example:

    ```
    import dash
    from dash import html
    import dash_cytoscape as cyto

    cyto.load_extra_layouts()

    app = dash.Dash(__name__)

    app.layout = html.Div([
        cyto.Cytoscape(...),
    ])
    ```

    Be careful about using the extra layouts when not necessary, since they require supplementary
    bandwidth for loading, which impacts the startup time of the app.
    """
    global _js_dist

    _js_dist = [
        {
            "relative_package_path": "dash_cytoscape_extra.min.js",
            "dev_package_path": "dash_cytoscape_extra.dev.js",
            "external_url": "https://unpkg.com/dash-cytoscape@{}/{}/{}.min.js".format(
                __version__, __name__, "dash_cytoscape_extra"
            ),
            "namespace": package_name,
        }
    ]


def _display_default_values():
    out_string = ""

    metadata_path = _os.path.join(
        _os.path.dirname(_os.path.realpath(__file__)), "metadata.json"
    )

    with open(metadata_path, "r") as file:
        data = json.loads(file.read())

    for component in data:
        component_name = component.replace("src/lib/components/", "").replace(
            ".react.js", ""
        )
        metadata = data[component]
        props = metadata["props"]

        out_string += "## {} Default Values\n\n".format(component_name)

        for prop_name in props:
            prop = props[prop_name]

            if "defaultValue" in prop:
                default = prop["defaultValue"]["value"]

                out_string += "* *{}*: {}\n".format(prop_name, default)

    return out_string
