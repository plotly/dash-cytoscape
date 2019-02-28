import base64
import dash
import dash_html_components as html
import os
from .IntegrationTests import IntegrationTests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Tests(IntegrationTests):
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
