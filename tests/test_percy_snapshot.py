"""
In order to render snapshots, Percy collects the DOM of the project and
uses a custom rendering method, different from Selenium. Therefore, it
is unable to render Canvas elements, so can't render Cytoscape charts
directly.

Instead, we use Selenium webdrivers to automatically screenshot each of
the apps being tested in test_usage.py, display them in a simple
Dash app, and use Percy to take a snapshot for CVI.

Here, we extend the setUpClass method from IntegrationTests by adding
percy runner initialization. This is because other classes that inherits
from IntegrationTests do not necessarily need to initialize Percy (since
all they do is save snapshots), and doing so causes Percy to render an
empty build that ends up failing. Therefore, we decide to initialize and
finalize the Percy runner in this class rather than inside
IntegrationTests.
"""

import base64
import os
import sys
import time
import pytest
import dash
from dash import html, dcc, Input, Output, callback


def create_app(dir_name):
    def encode(name):
        path = os.path.join(os.path.dirname(__file__), "screenshots", dir_name, name)

        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return "data:image/png;base64," + encoded_string.decode("ascii")

    # Define the app
    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            # represents the URL bar, doesn't render anything
            dcc.Location(id="url", refresh=False),
            # content will be rendered in this element
            html.Div(id="page-content"),
        ]
    )

    @callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
    )
    def display_image(pathname):  # pylint: disable=W0612
        """
        Assign the url path to return the image it represent. For example,
        to return "usage.png", you can visit localhost/usage.png.
        :param pathname: name of the screenshot, prefixed with "/"
        :return: An html.Img object containing the base64 encoded image
        """
        if not pathname or pathname == "/":
            return None

        name = pathname.replace("/", "")
        return html.Img(id=name, src=encode(name))

    return app


def percy_snapshot(dash_duo, name=""):
    snapshot_name = f"{name} (Python {sys.version_info.major}.{sys.version_info.minor})"

    dash_duo.percy_snapshot(name=snapshot_name)


def run_percy_on(dir_name, dash_duo):
    # Find the names of all the screenshots
    asset_list = os.listdir(
        os.path.join(os.path.dirname(__file__), "screenshots", dir_name)
    )

    current_url = dash_duo.driver.current_url
    # Run Percy
    for image in asset_list:
        if image.endswith("png"):
            output_name = image.replace(".png", "")

            dash_duo.driver.get(current_url + image)

            dash_duo.wait_for_element_by_id(image, 20)

            percy_snapshot(dash_duo, name=f"{dir_name.upper()}: {output_name}")
            time.sleep(2)


@pytest.mark.parametrize(
    "name", ["usage", "elements", "layouts", "style", "interactions"]
)
def test_cyps001_snapshots(name, dash_duo):
    app = create_app(dir_name=name)
    dash_duo.start_server(app)

    run_percy_on(name, dash_duo)
