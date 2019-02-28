import base64
import dash
import dash_html_components as html
import os
from .IntegrationTests import IntegrationTests
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

        def image_section(name):
            return html.Div([
                html.P(name),
                html.Img(src=encode(name))
            ])

        asset_list = os.listdir(os.path.join(
            os.path.dirname(__file__),
            'screenshots'
        ))

        app = dash.Dash(__name__)

        app.layout = html.Div([
            image_section(name)
            for name in asset_list if name.endswith('png')
        ])

        self.startServer(app)

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
        )

        self.percy_snapshot(name='Snapshot of all usage apps')
