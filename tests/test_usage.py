import os
import importlib
from .IntegrationTests import IntegrationTests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Tests(IntegrationTests):
    def create_usage_test(self, filename, dir_name='usage'):
        app = importlib.import_module(filename).app

        self.startServer(app)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "cytoscape"))
        )

        directory_path = os.path.join(
            os.path.dirname(__file__),
            'screenshots',
            dir_name
        )

        # Create directory if it doesn't already exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        self.driver.save_screenshot(os.path.join(
            os.path.dirname(__file__),
            'screenshots',
            dir_name,
            filename + '.png'
        ))

    def test_usage_advanced(self):
        self.create_usage_test('usage-advanced')

    def test_usage_animated_bfs(self):
        self.create_usage_test('demos.usage-animated-bfs')

    def test_usage_breadthfirst_layout(self):
        self.create_usage_test('demos.usage-breadthfirst-layout')

    def test_usage_compound_nodes(self):
        self.create_usage_test('demos.usage-compound-nodes')

    def test_usage_events(self):
        self.create_usage_test('usage-events')

    def test_usage_elements(self):
        self.create_usage_test('usage-elements')

    def test_usage_pie_style(self):
        self.create_usage_test('demos.usage-pie-style')

    def test_usage_simple(self):
        self.create_usage_test('usage')

    def test_usage_stylesheet(self):
        self.create_usage_test('usage-stylesheet')

    def test_usage_initialisation(self):
        self.create_usage_test('demos.usage-initialisation')

    def test_usage_linkout_example(self):
        self.create_usage_test('demos.usage-linkout-example')

    def test_usage_image_export(self):
        self.create_usage_test('demos.usage-image-export')

    def test_usage_responsive_graph(self):
        self.create_usage_test('demos.usage-responsive-graph')
