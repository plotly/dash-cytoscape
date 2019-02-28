import base64
import os
import time

from .IntegrationTests import IntegrationTests
import dash
import dash_html_components as html
import dash_core_components as dcc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Tests(IntegrationTests):
    """
    In order to render snapshots, Percy collects the DOM of the project and
    uses a custom rendering method, different from Selenium. Therefore, it
    is unable to render Canvas elements, so can't render Cytoscape charts
    directly.

    Instead, we use Selenium webdrivers to automatically screenshot each of
    the apps being tested in test_usage.py, display them in a simple
    Dash app, and use Percy to take a snapshot for CVI.
    """

    def test_usage(self):
        def encode(name):
            path = os.path.join(
                os.path.dirname(__file__),
                'screenshots',
                name
            )

            with open(path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read())
            return "data:image/png;base64," + encoded_string.decode('ascii')

        # Define the app
        app = dash.Dash(__name__)

        app.layout = html.Div([
            # represents the URL bar, doesn't render anything
            dcc.Location(id='url', refresh=False),
            # content will be rendered in this element
            html.Div(id='page-content')
        ])

        @app.callback(dash.dependencies.Output('page-content', 'children'),
                      [dash.dependencies.Input('url', 'pathname')])
        def display_image(pathname):  # pylint: disable=W0612
            """
            Assign the url path to return the image it represent. For example,
            to return "usage.png", you can visit localhost/usage.png.
            :param pathname: name of the screenshot, prefixed with "/"
            :return: An html.Img object containing the base64 encoded image
            """
            if not pathname or pathname == '/':
                return None

            name = pathname.replace('/', '')
            return html.Img(id=name, src=encode(name))

        # Start the app
        self.startServer(app)

        # Find the names of all the screenshots
        asset_list = os.listdir(os.path.join(
            os.path.dirname(__file__),
            'screenshots'
        ))

        # Run Percy
        for image in asset_list:
            if image.endswith('png'):
                self.driver.get('http://localhost:8050/{}'.format(image))

                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, image))
                )

                self.percy_snapshot(name=image)
                time.sleep(2)
