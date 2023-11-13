import os
import importlib

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def create_input_and_save(
    dash_duo, css_selector, dir_name, options, prefix=None, name_map=None, save=True
):
    elem = dash_duo.find_element(css_selector)

    directory_path = os.path.join(os.path.dirname(__file__), "screenshots", dir_name)

    # Create directory if it doesn't already exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    if prefix and not name_map:
        name_map = {option: prefix + option for option in options}

    elif not name_map:
        name_map = {}

    for option in options:
        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(option)
        elem.send_keys(Keys.RETURN)

        if save:
            # If the name map doesn't contain a custom name for the option,
            # we default to the value of the option to name the saved
            # screenshot
            name = name_map.get(option, option)
            name = name.replace("(", "_").replace(")", "").replace(",", "_")
            name = name.replace("#", "_hex_").replace(" ", "")

            dash_duo.wait_for_element_by_id("cytoscape", 20)

            path = os.path.join(
                os.path.dirname(__file__), "screenshots", dir_name, name + ".png"
            )

            dash_duo.driver.save_screenshot(path)


def click_button_and_save(dash_duo, name_to_xpaths, dir_name, save=True):
    for name, xpath in name_to_xpaths.items():
        button = dash_duo.driver.find_element(By.XPATH, xpath)
        button.click()

        if save:
            dash_duo.wait_for_element_by_id("cytoscape", 20)

            path = os.path.join(
                os.path.dirname(__file__), "screenshots", dir_name, name + ".png"
            )

            dash_duo.driver.save_screenshot(path)


def test_cycb001_callbacks(dash_duo):
    app = importlib.import_module("usage-advanced").app

    dash_duo.start_server(app)
    dash_duo.wait_for_element_by_id("cytoscape", 20)

    create_input_and_save(
        dash_duo,
        css_selector="#dropdown-select-element-list input",
        dir_name="elements",
        options=["Basic", "Compound", "Gene", "Wineandcheese"],
    )

    create_input_and_save(
        dash_duo,
        css_selector="#dropdown-layout input",
        dir_name="layouts",
        options=["Preset", "Grid", "Circle", "Concentric", "Breadthfirst", "Cose"],
    )

    # Reset the input to what it was at the beginning
    create_input_and_save(
        dash_duo,
        css_selector="#dropdown-select-element-list input",
        dir_name="elements",
        options=["Basic"],
        save=False,
    )
    create_input_and_save(
        dash_duo,
        css_selector="#dropdown-layout input",
        dir_name="layouts",
        options=["Circle"],
        save=False,
    )

    # Input Different types of Node Content
    create_input_and_save(
        dash_duo,
        css_selector="#input-node-content",
        dir_name="style",
        options=["Hello", "data(id)"],
        name_map={"Hello": "NodeDisplayContentStatic", "data(id)": "NodeDisplayID"},
    )

    # Input Different node widths
    create_input_and_save(
        dash_duo,
        css_selector="#input-node-width",
        dir_name="style",
        options=["30", "50"],
        prefix="NodeWidth",
    )

    # Input Different node heights
    create_input_and_save(
        dash_duo,
        css_selector="#input-node-height",
        dir_name="style",
        options=["40", "60"],
        prefix="NodeHeight",
    )

    # Input different node shapes
    create_input_and_save(
        dash_duo,
        css_selector="#dropdown-node-shape input",
        dir_name="style",
        options=[
            "Triangle",
            "Rectangle",
            "Roundrectangle",
            "Barrel",
            "Diamond",
            "Pentagon",
            "Star",
            "Tag",
            "Vee",
            "Ellipse",
        ],
        prefix="NodeShape",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#input-node-color",
        dir_name="style",
        options=["pink", "sky blue", "rgb(186,44,162)", "#def229"],
        prefix="NodeColor",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#input-node-border-width",
        dir_name="style",
        options=["2"],
        save=False,
    )

    create_input_and_save(
        dash_duo,
        css_selector="#input-node-border-color",
        dir_name="style",
        options=["pink", "sky blue", "rgb(186,44,162)", "#def229"],
        prefix="BorderColor",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#input-node-border-width",
        dir_name="style",
        options=["5", "2"],
        prefix="NodeBorderWidth",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#dropdown-node-border-style input",
        dir_name="style",
        options=[
            "Dashed",
            "Dotted",
            "Double",
            "Solid",
        ],
        prefix="NodeBorderStyle",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#input-node-padding",
        dir_name="style",
        options=["5px"],
        prefix="NodePadding",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#dropdown-node-padding-relative-to input",
        dir_name="style",
        options=["Width", "Height", "Average", "Min", "Max"],
        prefix="NodePaddingRelativeTo",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#input-edge-line-width",
        dir_name="style",
        options=["10", "1", "3"],
        prefix="LineWidth",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#dropdown-edge-curve-style input",
        dir_name="style",
        options=["Haystack", "Segments", "Unbundled-bezier", "Bezier"],
        prefix="EdgeCurveStyle",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#input-edge-line-color",
        dir_name="style",
        options=["pink", "sky blue", "rgb(186,44,162)", "#def229"],
        prefix="EdgeColor",
    )

    # Modify Edge Styles
    click_button_and_save(
        dash_duo,
        name_to_xpaths={
            "EdgeStyleSolid": '//*[@id="radio-edge-line-style"]/label[1]',
            "EdgeStyleDotted": '//*[@id="radio-edge-line-style"]/label[2]',
            "EdgeStyleDashed": '//*[@id="radio-edge-line-style"]/label[3]',
        },
        dir_name="style",
    )

    # Set "Use Edge Arrow" to "Yes"
    click_button_and_save(
        dash_duo,
        name_to_xpaths={"EdgeArrow": '//*[@id="radio-use-edge-arrow"]/label[1]'},
        dir_name="style",
        save=False,
    )

    create_input_and_save(
        dash_duo,
        css_selector="#dropdown-source-arrow-shape input",
        dir_name="style",
        options=["Circle", "Vee", "Tee", "Diamond", "Triangle"],
        prefix="EdgeArrowShape",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#input-source-arrow-color",
        dir_name="style",
        options=["pink", "sky blue", "rgb(186,44,162)", "#def229"],
        prefix="EdgeArrowColor",
    )

    click_button_and_save(
        dash_duo,
        name_to_xpaths={
            "EdgeArrowFilled": ('//*[@id="radio-source-arrow-fill"]/' "label[1]"),
            "EdgeArrowHollow": ('//*[@id="radio-source-arrow-fill"]/' "label[2]"),
        },
        dir_name="style",
    )

    create_input_and_save(
        dash_duo,
        css_selector="#input-arrow-scale",
        dir_name="style",
        options=["3", "2", "1"],
        prefix="EdgeArrowScale",
    )


def test_cycb002_callbacks(dash_duo):
    app = importlib.import_module("usage-context-menu").app
    dash_duo.start_server(app)
    dash_duo.wait_for_element_by_id("cytoscape", 20)

    def test_context_menu_after_cb(dash_duo, options, css_selector="#dropdown input"):
        elem = dash_duo.find_element(css_selector)
        for option in options:
            elem.send_keys(Keys.CONTROL + "a")
            elem.send_keys(option)
            elem.send_keys(Keys.RETURN)
            css_selector = f"button#{option}"
            try:
                dash_duo.find_element(css_selector)
                assert True
            except Exception:
                assert False

    test_context_menu_after_cb(
        dash_duo,
        options=["add-node", "remove", "add-edge"],
    )
