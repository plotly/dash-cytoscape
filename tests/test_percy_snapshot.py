import base64
import os
import sys
import time

from .IntegrationTests import IntegrationTests
import dash
import dash_html_components as html
import dash_core_components as dcc
import percy
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

    Here, we extend the setUpClass method from IntegrationTests by adding
    percy runner initialization. This is because other classes that inherits
    from IntegrationTests do not necessarily need to initialize Percy (since
    all they do is save snapshots), and doing so causes Percy to render an
    empty build that ends up failing. Therefore, we decide to initialize and
    finalize the Percy runner in this class rather than inside
    IntegrationTests.
    """

    @staticmethod
    def create_app(dir_name):
        def encode(name):
            path = os.path.join(
                os.path.dirname(__file__),
                'screenshots',
                dir_name,
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

        return app

    def percy_snapshot(self, name=''):
        if os.environ.get('PERCY_ENABLED', False):
            snapshot_name = '{} (Python {}.{})'.format(
                name,
                sys.version_info.major,
                sys.version_info.minor
            )

            self.percy_runner.snapshot(
                name=snapshot_name
            )

    @classmethod
    def setUpClass(cls):
        super(Tests, cls).setUpClass()

        if os.environ.get('PERCY_ENABLED', False):
            loader = percy.ResourceLoader(webdriver=cls.driver)
            percy_config = percy.Config(default_widths=[1280])
            cls.percy_runner = percy.Runner(loader=loader, config=percy_config)
            cls.percy_runner.initialize_build()

    @classmethod
    def tearDownClass(cls):
        super(Tests, cls).tearDownClass()

        if os.environ.get('PERCY_ENABLED', False):
            cls.percy_runner.finalize_build()

    def run_percy_on(self, dir_name):
        # Find the names of all the screenshots
        asset_list = os.listdir(os.path.join(
            os.path.dirname(__file__),
            'screenshots',
            dir_name
        ))

        # Run Percy
        for image in asset_list:
            if image.endswith('png'):
                output_name = image.replace('.png', '')

                self.driver.get('http://localhost:8050/{}'.format(image))

                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, image))
                )

                self.percy_snapshot(
                    name='{}: {}'.format(dir_name.upper(), output_name)
                )
                time.sleep(2)

    def test_usage(self):
        # Create and start the app
        app = self.create_app(dir_name='usage')
        self.startServer(app)

        self.run_percy_on('usage')

    def test_elements(self):
        app = self.create_app(dir_name='elements')
        self.startServer(app)

        self.run_percy_on('elements')

    def test_layouts(self):
        app = self.create_app(dir_name='layouts')
        self.startServer(app)

        self.run_percy_on('layouts')

    def test_style(self):
        app = self.create_app(dir_name='style')
        self.startServer(app)

        self.run_percy_on('style')

    def test_interactions(self):
        app = self.create_app(dir_name='interactions')
        self.startServer(app)

        self.run_percy_on('interactions')
