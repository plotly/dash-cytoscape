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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


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

    def calculate_edge_position(node_1, node_2):
        x = round((node_1[0] + node_2[0]) * 0.5)
        y = round((node_1[1] + node_2[1]) * 0.5)
        return (x, y)

    edges_positions = {
        "Edge from Node 1 to Node 2": calculate_edge_position(
            init_pos["Node 1"], init_pos["Node 2"]
        ),
        "Edge from Node 2 to Node 4": calculate_edge_position(
            init_pos["Node 2"], init_pos["Node 4"]
        ),
        "Edge from Node 5 to Node 1": calculate_edge_position(
            init_pos["Node 5"], init_pos["Node 1"]
        ),
    }
    return init_pos, actions, edges_positions


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
        dash_duo.driver.find_element(By.TAG_NAME, "body"), x, y
    )
    actions.drag_and_drop_by_offset(source=None, xoffset=delta_x, yoffset=delta_y)
    actions.perform()
    time.sleep(1)

    elem_json = json.loads(elem.text)
    new_pos = (
        elem_json[0].get("position")
        if "position" in elem_json[0].keys()
        else elem_json[0].get("renderedPosition")
    )
    dragged_label = elem_json[0].get("data", {}).get("label")

    node_x = round(new_pos["x"])
    node_y = round(new_pos["y"])

    save_screenshot(
        dash_duo,
        dir_name,
        f"Dragged{dragged_label.replace(' ', '')}By{node_x}x{node_y}y",
    )

    return node_x, node_y


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
        dash_duo.driver.find_element(By.TAG_NAME, "body"), x, y
    )
    actions.click()
    actions.perform()

    time.sleep(1)
    clicked_label = json.loads(elem.text).get("data", {}).get("label")

    save_screenshot(dash_duo, dir_name, "Clicked" + clicked_label.replace(" ", ""))

    return clicked_label


def perform_mouseover(
    dash_duo, x, y, elem, actions, dir_name="interactions", screenshot_name="Mouseover"
):
    actions.reset_actions()
    actions.move_to_element_with_offset(
        dash_duo.driver.find_element(By.TAG_NAME, "body"), x - 50, y
    )
    actions.move_by_offset(50, 0)
    actions.perform()
    time.sleep(1)

    text = json.loads(elem.text)
    mouseover_label = json.loads(elem.text).get("label") if text else "null"

    save_screenshot(
        dash_duo, dir_name, screenshot_name + mouseover_label.replace(" ", "")
    )

    return mouseover_label


def test_cyin001_dragging(dash_duo):
    init_pos, actions, _ = create_app(dash_duo)

    # View module docstring for more information about initial positions
    init_x, init_y = init_pos["Node 1"]

    # Open the Drag data JSON tab
    actions.move_to_element(dash_duo.find_element("#tabs > div:nth-child(5)"))
    actions.click().perform()
    time.sleep(1)

    # Select the JSON output element
    elem_tap = dash_duo.find_element("pre#elements-data-json-output")

    # Get initial positions. Not actualy dragging
    init_node_x, init_node_y = perform_dragging(
        dash_duo, init_x, init_y, 1, 1, elem_tap, actions
    )

    def _test(newpos, expected_shift):
        dx, dy = expected_shift
        newx, newy = newpos
        expx = (dx / pixels_to_position_conv_factor) + init_node_x
        expy = (dy / pixels_to_position_conv_factor) + init_node_y
        assert abs(newx - expx) < 3
        assert abs(newy - expy) < 3

    pixels_to_position_conv_factor = 1280 * 0.00085
    # Test dragging the nodes around
    _test(
        perform_dragging(dash_duo, init_x, init_y, 150, 0, elem_tap, actions), (150, 0)
    )
    _test(
        perform_dragging(dash_duo, init_x + 150, init_y, 0, 150, elem_tap, actions),
        (150, 150),
    )
    _test(
        perform_dragging(
            dash_duo, init_x + 150, init_y + 150, -150, -150, elem_tap, actions
        ),
        (0, 0),
    )
    _test(
        perform_dragging(dash_duo, init_x, init_y, 100, -100, elem_tap, actions),
        (100, -100),
    )


def test_cyin002_clicking(dash_duo):
    init_pos, actions, _ = create_app(dash_duo)
    click_error = "Unable to click Cytoscape nodes properly"

    # Select the JSON output element
    elem_tap = dash_duo.find_element("pre#tap-node-json-output")

    # Test clicking the nodes
    for i in range(1, 7):
        label = f"Node {i}"
        assert (
            perform_clicking(dash_duo, *init_pos[label], elem_tap, actions) == label
        ), click_error


def test_cyin003_clicking_edges(dash_duo):
    _, actions, edges_positions = create_app(dash_duo)

    # Select the JSON output element
    elem_tap = dash_duo.find_element("pre#tap-edge-json-output")

    # Test clicking the edges
    for label, positions in edges_positions.items():
        assert perform_clicking(dash_duo, *positions, elem_tap, actions) == label


def test_cyin004_mouseover(dash_duo):
    init_pos, actions, _ = create_app(dash_duo)
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


def test_cyin005_mouseover_edges(dash_duo):
    _, actions, edges_positions = create_app(dash_duo)

    # Open the Mouseover JSON tab
    actions.move_to_element(dash_duo.find_element("#tabs > div:nth-child(3)"))
    actions.click().perform()
    time.sleep(1)

    # Select the JSON output element
    elem_mouseover = dash_duo.find_element("pre#mouseover-edge-data-json-output")

    # Test mouseover the edges
    for label, positions in edges_positions.items():
        assert perform_mouseover(dash_duo, *positions, elem_mouseover, actions) == label


def test_cyin006_mouseover_unhover(dash_duo):
    init_pos, actions, _ = create_app(dash_duo)
    mouseover_error = "Unable to mouseover Cytoscape nodes properly"

    # Open the Mouseover JSON tab
    actions.move_to_element(dash_duo.find_element("#tabs > div:nth-child(3)"))
    actions.click().perform()
    time.sleep(1)

    # Select the JSON output element
    elem_mouseover = dash_duo.find_element("pre#mouseover-node-data-json-output")

    # Test hovering the nodes
    label = "Node 1"
    assert (
        perform_mouseover(
            dash_duo,
            *init_pos[label],
            elem_mouseover,
            actions,
            screenshot_name="MouseoverHover",
        )
        == label
    ), mouseover_error

    # Test unhover
    label = "null"
    assert (
        perform_mouseover(
            dash_duo,
            70,
            250,
            elem_mouseover,
            actions,
            screenshot_name="MouseoverUnhover",
        )
        == label
    ), mouseover_error


def test_cyin007_click_twice(dash_duo):
    init_pos, actions, _ = create_app(dash_duo)

    # Open the Tap Data JSON tab
    actions.move_to_element(dash_duo.find_element("#tabs > div:nth-child(2)"))
    actions.click().perform()
    time.sleep(1)

    # Select the JSON output element
    elem_tap = dash_duo.find_element("pre#tap-node-data-json-output")

    # Test clicking the same node twice
    label = "Node 1"
    x, y = init_pos[label]

    actions.reset_actions()
    actions.move_to_element_with_offset(
        dash_duo.driver.find_element(By.TAG_NAME, "body"), x, y
    )
    actions.click()
    actions.perform()

    time.sleep(1)
    clicked_label_1 = json.loads(elem_tap.text).get("label")
    clicked_timestamp_1 = json.loads(elem_tap.text).get("timeStamp")

    # Second click
    actions.click()
    actions.perform()

    time.sleep(1)
    clicked_label_2 = json.loads(elem_tap.text).get("label")
    clicked_timestamp_2 = json.loads(elem_tap.text).get("timeStamp")

    assert clicked_label_1 == clicked_label_2
    assert clicked_timestamp_1 != clicked_timestamp_2


def test_cyin008_ctx_menu_remove_node(dash_duo):
    _, actions, _ = create_app(dash_duo)

    # Open the Drag data JSON tab
    actions.move_to_element(dash_duo.find_element("#tabs > div:nth-child(5)"))
    actions.click().perform()
    time.sleep(1)

    # Select the JSON output element before removal
    elements = dash_duo.find_element("pre#elements-data-json-output")
    nb_elements_before = len(json.loads(elements.text))

    # move mouse to first node and right click and click on remove
    actions.move_by_offset(-1170, 130)
    actions.context_click()
    actions.move_to_element(dash_duo.find_element("button#remove"))
    actions.click()
    actions.perform()
    time.sleep(1)

    # Select the JSON output element after removal
    elements = dash_duo.find_element("pre#elements-data-json-output")
    nb_elements_after = len(json.loads(elements.text))
    # removed one node and 3 edges
    assert nb_elements_before - 4 == nb_elements_after


def test_cyin009_ctx_menu_remove_edge(dash_duo):
    _, actions, _ = create_app(dash_duo)

    # Open the Drag data JSON tab
    actions.move_to_element(dash_duo.find_element("#tabs > div:nth-child(5)"))
    actions.click().perform()
    time.sleep(1)

    # Select the JSON output element before removal
    elements = dash_duo.find_element("pre#elements-data-json-output")
    nb_elements_before = len(json.loads(elements.text))

    # move mouse to an edge and right click and click on remove
    actions.move_by_offset(-1100, 150)
    actions.context_click()
    actions.move_to_element(dash_duo.find_element("button#remove"))
    actions.click()
    actions.perform()
    time.sleep(1)

    # Select the JSON output element after removal
    elements = dash_duo.find_element("pre#elements-data-json-output")
    nb_elements_after = len(json.loads(elements.text))

    assert nb_elements_before - 1 == nb_elements_after


def test_cyin010_ctx_menu_add_node(dash_duo):
    _, actions, _ = create_app(dash_duo)

    # Open the Drag data JSON tab
    actions.move_to_element(dash_duo.find_element("#tabs > div:nth-child(5)"))
    actions.click().perform()
    time.sleep(1)

    # Select the JSON output element before addition
    elements = dash_duo.find_element("pre#elements-data-json-output")
    nb_elements_before = len(json.loads(elements.text))

    # click anywhere to add a node
    actions.move_by_offset(-1000, 40)
    actions.context_click()
    actions.move_to_element(dash_duo.find_element("button#add-node"))
    actions.click()
    actions.perform()
    time.sleep(1)

    # Select the JSON output element after addition
    elements = dash_duo.find_element("pre#elements-data-json-output")
    nb_elements_after = len(json.loads(elements.text))

    assert nb_elements_before + 1 == nb_elements_after


def test_cyin011_ctx_menu_add_edge(dash_duo):
    _, actions, _ = create_app(dash_duo)

    # Open the Drag data JSON tab
    actions.move_to_element(dash_duo.find_element("#tabs > div:nth-child(5)"))
    actions.click().perform()
    time.sleep(1)

    # Select the JSON output element before addition
    elements = dash_duo.find_element("pre#elements-data-json-output")
    nb_elements_before = len(json.loads(elements.text))

    # click on 2 nodes to add an edge between them
    actions.key_down(Keys.COMMAND)
    actions.move_by_offset(-1170, 130)
    actions.click()
    actions.move_by_offset(400, 0)
    actions.click()
    actions.context_click()
    actions.move_to_element(dash_duo.find_element("button#add-edge"))
    actions.click()
    actions.perform()
    time.sleep(1)

    # Select the JSON output element after addition
    elements = dash_duo.find_element("pre#elements-data-json-output")
    nb_elements_after = len(json.loads(elements.text))

    assert nb_elements_before + 1 == nb_elements_after
