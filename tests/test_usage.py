import os
import importlib


class Tests:
    @staticmethod
    def create_usage_test(dash_duo, filename, dir_name='usage'):
        app = importlib.import_module(filename).app

        dash_duo.start_server(app)
        dash_duo.wait_for_element_by_id("cytoscape", 20)

        directory_path = os.path.join(
            os.path.dirname(__file__),
            'screenshots',
            dir_name
        )

        # Create directory if it doesn't already exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        dash_duo.driver.save_screenshot(os.path.join(
            os.path.dirname(__file__),
            'screenshots',
            dir_name,
            filename + '.png'
        ))

    def test_usage_advanced(self, dash_duo):
        self.create_usage_test(dash_duo, 'usage-advanced')

    def test_usage_animated_bfs(self, dash_duo):
        self.create_usage_test(dash_duo, 'demos.usage-animated-bfs')

    def test_usage_breadthfirst_layout(self, dash_duo):
        self.create_usage_test(dash_duo, 'demos.usage-breadthfirst-layout')

    def test_usage_compound_nodes(self, dash_duo):
        self.create_usage_test(dash_duo, 'demos.usage-compound-nodes')

    def test_usage_events(self, dash_duo):
        self.create_usage_test(dash_duo, 'usage-events')

    def test_usage_elements(self, dash_duo):
        self.create_usage_test(dash_duo, 'usage-elements')

    def test_usage_pie_style(self, dash_duo):
        self.create_usage_test(dash_duo, 'demos.usage-pie-style')

    def test_usage_simple(self, dash_duo):
        self.create_usage_test(dash_duo, 'usage')

    def test_usage_stylesheet(self, dash_duo):
        self.create_usage_test(dash_duo, 'usage-stylesheet')

    def test_usage_initialisation(self, dash_duo):
        self.create_usage_test(dash_duo, 'demos.usage-initialisation')

    def test_usage_linkout_example(self, dash_duo):
        self.create_usage_test(dash_duo, 'demos.usage-linkout-example')

    def test_usage_image_export(self, dash_duo):
        self.create_usage_test(dash_duo, 'demos.usage-image-export')

    def test_usage_responsive_graph(self, dash_duo):
        self.create_usage_test(dash_duo, 'demos.usage-responsive-graph')
