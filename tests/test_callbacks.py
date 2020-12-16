import os
import importlib

from .IntegrationTests import IntegrationTests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Tests(IntegrationTests):
    def test_callbacks(self):
        app = importlib.import_module('usage-advanced').app
        self.startServer(app)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "cytoscape"))
        )

        def create_input_and_save(css_selector,
                                  dir_name,
                                  options,
                                  prefix=None,
                                  name_map=None,
                                  save=True):
            elem = self.driver.find_element_by_css_selector(css_selector)

            directory_path = os.path.join(
                os.path.dirname(__file__),
                'screenshots',
                dir_name
            )

            # Create directory if it doesn't already exist
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            if prefix and not name_map:
                name_map = {
                    option: prefix + option
                    for option in options
                }

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
                    name = name.replace('(', '_').replace(')', '').replace(',', '_')
                    name = name.replace('#', '_hex_').replace(' ', '')

                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.ID, "cytoscape"))
                    )

                    path = os.path.join(
                        os.path.dirname(__file__),
                        'screenshots',
                        dir_name,
                        name + '.png'
                    )

                    self.driver.save_screenshot(path)

        def click_button_and_save(name_to_xpaths, dir_name, save=True):
            for name, xpath in name_to_xpaths.items():
                button = self.driver.find_element(By.XPATH, xpath)
                button.click()

                if save:
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.ID, "cytoscape"))
                    )

                    path = os.path.join(
                        os.path.dirname(__file__),
                        'screenshots',
                        dir_name,
                        name + '.png'
                    )

                    self.driver.save_screenshot(path)

        create_input_and_save(
            css_selector='input#dropdown-select-element-list',
            dir_name='elements',
            options=['Basic', 'Compound', 'Gene', 'Wineandcheese']
        )

        create_input_and_save(
            css_selector='input#dropdown-layout',
            dir_name='layouts',
            options=[
                'Preset',
                'Grid',
                'Circle',
                'Concentric',
                'Breadthfirst',
                'Cose'
            ]
        )

        # Reset the input to what it was at the beginning
        create_input_and_save(
            css_selector='input#dropdown-select-element-list',
            dir_name='elements',
            options=['Basic'],
            save=False
        )
        create_input_and_save(
            css_selector='input#dropdown-layout',
            dir_name='layouts',
            options=['Circle'],
            save=False
        )

        # Input Different types of Node Content
        create_input_and_save(
            css_selector='input#input-node-content',
            dir_name='style',
            options=[
                'Hello',
                'data(id)'
            ],
            name_map={
                'Hello': 'NodeDisplayContentStatic',
                'data(id)': 'NodeDisplayID'
            }
        )

        # Input Different node widths
        create_input_and_save(
            css_selector='input#input-node-width',
            dir_name='style',
            options=[
                '30',
                '50'
            ],
            prefix='NodeWidth'
        )

        # Input Different node heights
        create_input_and_save(
            css_selector='input#input-node-height',
            dir_name='style',
            options=[
                '40',
                '60'
            ],
            prefix='NodeHeight'
        )

        # Input different node shapes
        create_input_and_save(
            css_selector='input#dropdown-node-shape',
            dir_name='style',
            options=[
                'Triangle',
                'Rectangle',
                'Roundrectangle',
                'Barrel',
                'Diamond',
                'Pentagon',
                'Star',
                'Tag',
                'Vee',
                'Ellipse'
            ],
            prefix='NodeShape'
        )

        create_input_and_save(
            css_selector='input#input-node-color',
            dir_name='style',
            options=[
                'pink',
                'sky blue',
                'rgb(186,44,162)',
                '#def229'
            ],
            prefix='NodeColor'
        )

        create_input_and_save(
            css_selector='input#input-node-border-width',
            dir_name='style',
            options=['2'],
            save=False
        )

        create_input_and_save(
            css_selector='input#input-node-border-color',
            dir_name='style',
            options=[
                'pink',
                'sky blue',
                'rgb(186,44,162)',
                '#def229'
            ],
            prefix='BorderColor'
        )

        create_input_and_save(
            css_selector='input#input-node-border-width',
            dir_name='style',
            options=['5', '2'],
            prefix='NodeBorderWidth'
        )

        create_input_and_save(
            css_selector='input#dropdown-node-border-style',
            dir_name='style',
            options=[
                'Dashed',
                'Dotted',
                'Double',
                'Solid',
            ],
            prefix='NodeBorderStyle'
        )

        create_input_and_save(
            css_selector='input#input-node-padding',
            dir_name='style',
            options=['5px'],
            prefix='NodePadding'
        )

        create_input_and_save(
            css_selector='input#dropdown-node-padding-relative-to',
            dir_name='style',
            options=['Width', 'Height', 'Average', 'Min', 'Max'],
            prefix='NodePaddingRelativeTo'
        )

        create_input_and_save(
            css_selector='input#input-edge-line-width',
            dir_name='style',
            options=['10', '1', '3'],
            prefix='LineWidth'
        )

        create_input_and_save(
            css_selector='input#dropdown-edge-curve-style',
            dir_name='style',
            options=['Haystack', 'Segments', 'Unbundled-bezier', 'Bezier'],
            prefix='EdgeCurveStyle'
        )

        create_input_and_save(
            css_selector='input#input-edge-line-color',
            dir_name='style',
            options=[
                'pink',
                'sky blue',
                'rgb(186,44,162)',
                '#def229'
            ],
            prefix='EdgeColor'
        )

        # Modify Edge Styles
        click_button_and_save(
            name_to_xpaths={
                'EdgeStyleSolid': '//*[@id="radio-edge-line-style"]/label[1]',
                'EdgeStyleDotted': '//*[@id="radio-edge-line-style"]/label[2]',
                'EdgeStyleDashed': '//*[@id="radio-edge-line-style"]/label[3]',
            },
            dir_name='style'
        )

        # Set "Use Edge Arrow" to "Yes"
        click_button_and_save(
            name_to_xpaths={
                'EdgeArrow': '//*[@id="radio-use-edge-arrow"]/label[1]'},
            dir_name='style',
            save=False
        )

        create_input_and_save(
            css_selector='input#dropdown-source-arrow-shape',
            dir_name='style',
            options=[
                'Circle',
                'Vee',
                'Tee',
                'Diamond',
                'Triangle'
            ],
            prefix='EdgeArrowShape'
        )

        create_input_and_save(
            css_selector='input#input-source-arrow-color',
            dir_name='style',
            options=[
                'pink',
                'sky blue',
                'rgb(186,44,162)',
                '#def229'
            ],
            prefix='EdgeArrowColor'
        )

        click_button_and_save(
            name_to_xpaths={
                'EdgeArrowFilled': ('//*[@id="radio-source-arrow-fill"]/'
                                    'label[1]'),
                'EdgeArrowHollow': ('//*[@id="radio-source-arrow-fill"]/'
                                    'label[2]')
            },
            dir_name='style'
        )

        create_input_and_save(
            css_selector='input#input-arrow-scale',
            dir_name='style',
            options=[
                '3',
                '2',
                '1'
            ],
            prefix='EdgeArrowScale'
        )
