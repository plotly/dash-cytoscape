import os
import importlib
import time
import json

from .IntegrationTests import IntegrationTests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class Tests(IntegrationTests):
    def test_interactions(self):
        app = importlib.import_module('usage-events').app
        self.startServer(app)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "cytoscape")))

        actions = ActionChains(self.driver)

        def save_screenshot(dir_name, name):
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
                name + '.png'
            ))

        def perform_dragging(x, y, delta_x, delta_y, elem, dir_name='interactions'):
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
                self.driver.find_element_by_tag_name('body'), x, y
            )
            actions.drag_and_drop_by_offset(source=None, xoffset=delta_x, yoffset=delta_y)
            actions.click()
            actions.perform()
            time.sleep(1)

            elem_json = json.loads(elem.text)
            new_pos = elem_json.get('renderedPosition')
            clicked_label = elem_json.get('data', {}).get('label')

            diff_x = round(new_pos['x'] - x)
            diff_y = round(new_pos['y'] - y)

            save_screenshot(
                dir_name,
                'Dragged{}By{}x{}y'.format(clicked_label.replace(' ', ''), diff_x, diff_y)
            )

            return diff_x, diff_y

        def perform_clicking(x, y, elem, dir_name='interactions'):
            """
            :param x: The position on the screen where we want to click
            :param y: The position on the screen where we want to click
            :param elem: The element object from where we retrieve the JSON
            :param dir_name: The directory in which we store our screenshots
            :return: The label of element most recently clicked, if any
            """
            actions.reset_actions()
            actions.move_to_element_with_offset(
                self.driver.find_element_by_tag_name('body'), x, y
            )
            actions.click()
            actions.perform()

            time.sleep(1)
            clicked_label = json.loads(elem.text).get('data', {}).get('label')

            save_screenshot(dir_name, 'Clicked' + clicked_label.replace(' ', ''))

            return clicked_label

        def perform_mouseover(x, y, elem, dir_name='interactions'):
            actions.reset_actions()
            actions.move_to_element_with_offset(
                self.driver.find_element_by_tag_name('body'), x - 100, y
            )
            actions.move_by_offset(100, 0)
            actions.perform()
            time.sleep(1)

            mouseover_label = json.loads(elem.text).get('label')

            save_screenshot(dir_name, 'Mouseover' + mouseover_label.replace(' ', ''))

            return mouseover_label

        drag_error = "Unable to drag Cytoscape nodes properly"
        click_error = "Unable to click Cytoscape nodes properly"
        mouseover_error = "Unable to mouseover Cytoscape nodes properly"

        init_pos = {
            'Node 1': (80.94611044209678, 333.54879281525285),
            'Node 2': (375.64032747402433, 628.2430098471805),
            'Node 3': (277.40892179671516, 514.2945792615018 - 20),
            'Node 4': (768.5659501832611, 333.54879281525285),
            'Node 5': (473.8717331513335, 431.780198492562),
            'Node 6': (277.40892179671516, 530.0116041698712)
        }
        init_x, init_y = init_pos['Node 1']
        # Select the JSON output element
        elem_tap = self.driver.find_element_by_css_selector('pre#tap-node-json-output')

        # # Test dragging the nodes around
        offset_x, offset_y = perform_dragging(init_x, init_y, 0, 0, elem_tap)
        init_x += offset_x
        init_y += offset_y

        assert perform_dragging(init_x, init_y, 150, 0, elem_tap) == (150, 0), drag_error
        assert perform_dragging(init_x+150, init_y, 0, 150, elem_tap) == (0, 150), drag_error
        assert perform_dragging(init_x+150, init_y+150, -150, -150, elem_tap) == (-150, -150), \
            drag_error

        # Test clicking the nodes
        for i in range(1, 7):
            label = 'Node {}'.format(i)
            assert perform_clicking(*init_pos[label], elem_tap) == label, click_error

        # Open the Mouseover JSON tab
        actions.move_to_element(
            self.driver.find_element_by_css_selector('#tabs > div:nth-child(3)'))
        actions.click().perform()
        time.sleep(1)

        # Select the JSON output element
        elem_mouseover = self.driver.find_element_by_css_selector(
            'pre#mouseover-node-data-json-output')

        # Test hovering the nodes
        for i in range(1, 7):
            label = 'Node {}'.format(i)
            assert perform_mouseover(*init_pos[label], elem_mouseover) == label, mouseover_error
