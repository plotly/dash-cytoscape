import os
import importlib
import pytest
import time


def create_usage_test(dash_duo, filename, dir_name="usage"):
    app = importlib.import_module(filename).app

    dash_duo.start_server(app)
    dash_duo.wait_for_element_by_id("cytoscape", 20)

    # Wait for the flickr images to load
    if filename == "demos.usage-breadthfirst-layout":
        time.sleep(1)

    directory_path = os.path.join(os.path.dirname(__file__), "screenshots", dir_name)

    # Create directory if it doesn't already exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    dash_duo.driver.save_screenshot(
        os.path.join(
            os.path.dirname(__file__), "screenshots", dir_name, filename + ".png"
        )
    )


@pytest.mark.parametrize(
    "name",
    [
        "usage-advanced",
        "demos.usage-animated-bfs",
        "demos.usage-breadthfirst-layout",
        "demos.usage-compound-nodes",
        "usage-events",
        "usage-elements",
        "demos.usage-pie-style",
        "usage",
        "usage-stylesheet",
        "demos.usage-initialisation",
        "demos.usage-linkout-example",
        "demos.usage-image-export",
        "demos.usage-responsive-graph",
    ],
)
def test_cyug001_usage(name, dash_duo):
    create_usage_test(dash_duo, name)
