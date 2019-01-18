from pytest_dash.utils import (
    import_app,
    wait_for_text_to_equal,
    wait_for_element_by_css_selector
)


# Basic test for the component rendering.
def test_render_component(dash_threaded, selenium):
    # Start a dash app contained in `usage.py`
    # dash_threaded is a fixture by pytest-dash
    # It will load a py file containing a Dash instance named `app`
    # and start it in a thread.
    app = import_app('usage')
    dash_threaded(app)

    # Get the generated component input with selenium
    # The html input will be a children of the #input dash component
    my_component = wait_for_element_by_css_selector(selenium, '#input > input')

    assert 'my-value' == my_component.get_attribute('value')

    # Clear the input
    my_component.clear()

    # Send keys to the custom input.
    my_component.send_keys('Hello dash')

    # Wait for the text to equal, if after the timeout (default 10 seconds)
    # the text is not equal it will fail the test.
    wait_for_text_to_equal(selenium, '#output', 'You have entered Hello dash')
