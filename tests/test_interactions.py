"""Notes for the hardcoded values in the `init_pos` dictionary:

It's impossible to programatically get the initial rendered positions of the nodes, since we would
need to obtain the node object (in dictionary format), which can be done either by (a) using the
tapNode callback, which paradoxally requires you to click the node, or (b) by making a complex
calculation relative to the size of the screen w.r.t largest coordinate in the list of elements.
But (b) is unreliable, since we do not know how much padding around the graph is required, so it
will likely be off.

If there is a need to modify the values in `init_pos`, e.g. if the size of the webdriver screen
is changed, you can do the following:
    - Run usage-events.py
    - Resize window size to 1280x1000, or preferred size (can be manually done or with selenium)
    - Tap on a node
    - Inside the "Node Object JSON" section, find "renderedPosition" and use the values there
    - Repeat this for all the nodes

Notice also that there's an offset to Node 3's position. This is because it overlaps with
Node 6, so clicking on Node 3 will erroneously show that you clicked Node 6. Therefore, adding an
offset to the y-axis will ensure that the correct node is clicked.
"""
import os
import importlib
import time
import json

from selenium.webdriver.common.action_chains import ActionChains


def create_app(dash_duo):
    # Initialize the apps
    app = importlib.import_module("usage-events").app

    dash_duo.start_server(app)
    dash_duo.driver.set_window_size(1280, 1000)
    dash_duo.wait_for_element_by_id("cytoscape", 20)

    actions = ActionChains(dash_duo.driver)
    init_pos = {
        "Node 1": (59, 182),
        "Node 2": (222, 345),
        "Node 3": (168, 283 - 20),
        "Node 4": (440, 182),
        "Node 5": (277, 236),
        "Node 6": (168, 283),
    }
    return init_pos, actions


def save_screenshot(dash_duo, dir_name, name):
    directory_path = os.path.join(os.path.dirname(__file__), "screenshots", dir_name)

    # Create directory if it doesn't already exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    dash_duo.driver.save_screenshot(
        os.path.join(os.path.dirname(__file__), "screenshots", dir_name, name + ".png")
    )


def perform_dragging(
    dash_duo, x, y, delta_x, delta_y, elem, actions, dir_name="interactions"
):
    """
    Performs dragging on a node, and return the difference from the start
    :param x: initial position of the node at the start of the action chain
    :param y: initial position of the node at the start of the action chain
    :param delta_x: how much we want to drag the node
    :param delta_y: how much we want to drag the node
    :param dir_name: The directory in which we store our screenshots
    :return: the difference between the position after drag and the starting position
    """
    actions.reset_actions()
    actions.move_to_element_with_offset(
        dash_duo.driver.find_element_by_tag_name("body"), x, y
    )
    actions.drag_and_drop_by_offset(source=None, xoffset=delta_x, yoffset=delta_y)
    actions.click()
    actions.perform()
    time.sleep(1)

    elem_json = json.loads(elem.text)
    new_pos = elem_json.get("renderedPosition")
    clicked_label = elem_json.get("data", {}).get("label")

    diff_x = round(new_pos["x"] - x)
    diff_y = round(new_pos["y"] - y)

    save_screenshot(
        dash_duo,
        dir_name,
        f"Dragged{clicked_label.replace(' ', '')}By{diff_x}x{diff_y}y",
    )

    return diff_x, diff_y


def perform_clicking(dash_duo, x, y, elem, actions, dir_name="interactions"):
    """
    :param x: The position on the screen where we want to click
    :param y: The position on the screen where we want to click
    :param elem: The element object from where we retrieve the JSON
    :param dir_name: The directory in which we store our screenshots
    :return: The label of element most recently clicked, if any
    """
    actions.reset_actions()
    actions.move_to_element_with_offset(
        dash_duo.driver.find_element_by_tag_name("body"), x, y
    )
    actions.click()
    actions.perform()

    time.sleep(1)
    clicked_label = json.loads(elem.text).get("data", {}).get("label")

    save_screenshot(dash_duo, dir_name, "Clicked" + clicked_label.replace(" ", ""))

    return clicked_label


def perform_mouseover(dash_duo, x, y, elem, actions, dir_name="interactions"):
    actions.reset_actions()
    actions.move_to_element_with_offset(
        dash_duo.driver.find_element_by_tag_name("body"), x - 50, y
    )
    actions.move_by_offset(50, 0)
    actions.perform()
    time.sleep(1)

    mouseover_label = json.loads(elem.text).get("label")

    save_screenshot(dash_duo, dir_name, "Mouseover" + mouseover_label.replace(" ", ""))

    return mouseover_label


def test_cyin001_dragging(dash_duo):
    init_pos, actions = create_app(dash_duo)

    drag_error = "Unable to drag Cytoscape nodes properly"

    # View module docstring for more information about initial positions
    init_x, init_y = init_pos["Node 1"]

    # Select the JSON output element
    elem_tap = dash_duo.find_element("pre#tap-node-json-output")

    # Test dragging the nodes around
    offset_x, offset_y = perform_dragging(
        dash_duo, init_x, init_y, 0, 0, elem_tap, actions
    )
    init_x += offset_x
    init_y += offset_y

    assert perform_dragging(dash_duo, init_x, init_y, 150, 0, elem_tap, actions) == (
        150,
        0,
    ), drag_error
    assert perform_dragging(
        dash_duo, init_x + 150, init_y, 0, 150, elem_tap, actions
    ) == (0, 150), drag_error
    assert perform_dragging(
        dash_duo, init_x + 150, init_y + 150, -150, -150, elem_tap, actions
    ) == (-150, -150), drag_error


def test_cyin002_clicking(dash_duo):
    init_pos, actions = create_app(dash_duo)
    click_error = "Unable to click Cytoscape nodes properly"

    # Select the JSON output element
    elem_tap = dash_duo.find_element("pre#tap-node-json-output")

    # Test clicking the nodes
    for i in range(1, 7):
        label = f"Node {i}"
        assert (
            perform_clicking(dash_duo, *init_pos[label], elem_tap, actions) == label
        ), click_error


def test_cyin003_mouseover(dash_duo):
    init_pos, actions = create_app(dash_duo)
    mouseover_error = "Unable to mouseover Cytoscape nodes properly"

    # Open the Mouseover JSON tab
    actions.move_to_element(dash_duo.find_element("#tabs > div:nth-child(3)"))
    actions.click().perform()
    time.sleep(1)

    # Select the JSON output element
    elem_mouseover = dash_duo.find_element("pre#mouseover-node-data-json-output")

    # Test hovering the nodes
    for i in range(1, 7):
        label = f"Node {i}"
        assert (
            perform_mouseover(dash_duo, *init_pos[label], elem_mouseover, actions)
            == label
        ), mouseover_error
