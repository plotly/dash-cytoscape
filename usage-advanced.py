import dash
import dash_core_components as dcc
import dash_html_components as html
from colour import Color
from dash.dependencies import Input, Output

import dash_reusable_components as drc
import my_dash_component

app = dash.Dash(__name__)
server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

elements = [
    {
        'data': {'id': 'one', 'label': 'Node 1'},
        'position': {'x': 50, 'y': 50}
    },
    {
        'data': {'id': 'two', 'label': 'Node 2'},
        'position': {'x': 200, 'y': 200}
    },
    {
        'data': {'id': 'three', 'label': 'Node 3'},
        'position': {'x': 100, 'y': 150}
    },
    {
        'data': {'id': 'four', 'label': 'Node 4'},
        'position': {'x': 400, 'y': 50}
    },
    {
        'data': {'id': 'five', 'label': 'Node 5'},
        'position': {'x': 250, 'y': 100}
    },
    {
        'data': {'id': 'six', 'label': 'Node 6', 'parent': 'three'},
        'position': {'x': 150, 'y': 150}
    },

    {'data': {
        'source': 'one',
        'target': 'two',
        'label': 'Edge from Node1 to Node2'
    }},
    {'data': {
        'source': 'one',
        'target': 'five',
        'label': 'Edge from Node 1 to Node 5'
    }},
    {'data': {
        'source': 'two',
        'target': 'four',
        'label': 'Edge from Node 2 to Node 4'
    }},
    {'data': {
        'source': 'three',
        'target': 'five',
        'label': 'Edge from Node 3 to Node 5'
    }},
    {'data': {
        'source': 'three',
        'target': 'two',
        'label': 'Edge from Node 3 to Node 2'
    }},
    {'data': {
        'source': 'four',
        'target': 'six',
        'label': 'Edge from Node 4 to Node 6'
    }}
]


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_color(color, default='#999999'):
    '''
    Check if a color is valid, if so returns the color, else return a default color
    :param color: The color to validate
    :param default: The default color
    :return: A string representing a color
    '''
    if not color:
        return default

    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return color
    except:  # The color code was not found
        return default


def validate_px_percentage(value, default='0px'):
    if 'px' in value and is_float(value.replace('px', '')):
        return value
    elif '%' in value and is_float(value.replace('%', '')):
        return value
    else:
        return default


app.layout = html.Div([
    html.Div(className='row', children=[
        my_dash_component.Cytoscape(
            id='cytoscape',
            className='eight columns',
            layout={'name': 'preset'},
            elements=elements,
            style={
                'height': 'calc(100vh - 16px)'
            }
        ),

        html.Div(
            className='four columns',
            style={
                'overflow-y': 'auto',
                'overflow-x': 'hidden',
                'height': 'calc(100vh - 16px)',
                'float': 'right',
                'background-color': '#222222'
            },
            children=[
                drc.SectionTitle(
                    title='Layout',
                    size=3,
                    color='white'
                ),

                drc.NamedCard(title='Layout', size=4, children=[
                    drc.NamedDropdown(
                        name='Layout',
                        id='dropdown-layout',
                        options=drc.DropdownOptionsList(
                            'null',
                            'random',
                            'preset',
                            'grid',
                            'circle',
                            'concentric',
                            'breadthfirst',
                            'cose'
                        ),
                        value='preset',
                        clearable=False
                    ),
                ]),

                drc.SectionTitle(
                    title='Node body',
                    size=3,
                    color='white'
                ),

                drc.NamedCard(title='Content', size=4, children=[
                    drc.NamedInput(
                        name='Node Display Content',
                        id='input-node-content',
                        type='text',
                        value='data(label)',
                        placeholder='Enter the content you want for node...'
                    )
                ]),
                drc.NamedCard(title='Shape', size=4, children=[
                    drc.NamedInput(
                        name='Node Width (px)',
                        id='input-node-width',
                        type='number',
                        value=25,
                        placeholder='Enter a value in pixel...'
                    ),

                    drc.NamedInput(
                        name='Node Height (px)',
                        id='input-node-height',
                        type='number',
                        value=25,
                        placeholder='Enter a value in pixel...'
                    ),

                    drc.NamedDropdown(
                        name='Node Shape',
                        id='dropdown-node-shape',
                        value='ellipse',
                        clearable=False,
                        options=drc.DropdownOptionsList(
                            'ellipse',
                            'triangle',
                            'rectangle',
                            'roundrectangle',
                            'bottomroundrectangle',
                            'cutrectangle',
                            'barrel',
                            'rhomboid',
                            'diamond',
                            'pentagon',
                            'hexagon',
                            'concavehexagon',
                            'heptagon',
                            'octagon',
                            'star',
                            'tag',
                            'vee',
                            'polygon',
                        )
                    ),

                ]),
                drc.NamedCard(title='Background', size=4, children=[

                    drc.NamedInput(
                        name='Node Color',
                        id='input-node-color',
                        type='text',
                        placeholder='Enter Color in Hex...'
                    ),

                    drc.NamedSlider(
                        name='Node Opacity',
                        id='slider-node-opacity',
                        min=0,
                        max=1,
                        marks={0: '0', 1: '1'},
                        step=0.05,
                        value=1
                    ),

                    drc.NamedSlider(
                        name='Node Blacken',
                        id='slider-node-blacken',
                        min=0,
                        max=1,
                        marks={0: '0', 1: '1'},
                        step=0.05,
                        value=0
                    ),
                ]),
                drc.NamedCard(title='Border', size=4, children=[
                    drc.NamedInput(
                        name='Node Border Width (px)',
                        id='input-node-border-width',
                        type='number',
                        value=0,
                        placeholder='Enter a value in pixel...'
                    ),
                    drc.NamedDropdown(
                        name='Node Border Style',
                        id='dropdown-node-border-style',
                        value='solid',
                        clearable=False,
                        options=drc.DropdownOptionsList(
                            'null',
                            'solid',
                            'dotted',
                            'dashed',
                            'double'
                        )
                    ),
                    drc.NamedInput(
                        name='Node Border Color',
                        id='input-node-border-color',
                        type='text',
                        placeholder='Input Color in Hex...'
                    ),
                    drc.NamedSlider(
                        name='Node Border Opacity',
                        id='slider-node-border-opacity',
                        min=0,
                        max=1,
                        marks={0: '0', 1: '1'},
                        step=0.05,
                        value=1
                    ),
                ]),
                drc.NamedCard(title='Padding', size=4, children=[
                    drc.NamedInput(
                        name='Node Padding',
                        id='input-node-padding',
                        type='text',
                        placeholder='Input value in % or px...',
                        value='0px'
                    ),
                    drc.NamedDropdown(
                        name='Node Padding Relative To',
                        id='dropdown-node-padding-relative-to',
                        value='width',
                        clearable=False,
                        options=drc.DropdownOptionsList(
                            'width',
                            'height',
                            'average',
                            'min',
                            'max'
                        )
                    )
                ]),
                drc.NamedCard(title='Compound parent size', size=4, children=[
                    drc.NamedRadioItems(
                        name='Compound Sizing w.r.t. labels',
                        id='radio-node-compound-sizing',
                        value='include',
                        options=drc.DropdownOptionsList('include', 'exclude')
                    ),
                    drc.NamedInput(
                        name='Parent Node Min Width (px)',
                        id='input-node-compound-min-width',
                        type='number',
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Extra width on left side (%)',
                        id='input-node-compound-min-width-bias-left',
                        type='number',
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Extra width on right side (%)',
                        id='input-node-compound-min-width-bias-right',
                        type='number',
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Parent Node Min Height (px)',
                        id='input-node-compound-min-height',
                        type='number',
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Extra height on top side (%)',
                        id='input-node-compound-min-height-bias-top',
                        type='number',
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Extra height on bottom side (%)',
                        id='input-node-compound-min-height-bias-bottom',
                        type='number',
                        placeholder='Input value in px...',
                        value=0
                    ),
                ]),

                drc.SectionTitle(
                    title='Background image',
                    size=3,
                    color='white'
                ),
                # TODO: testing background, multiple bugs seem to exist
                drc.NamedCard(title='Background Image', size=4, children=[
                    drc.NamedInput(
                        name='Image URL/URI',
                        id='input-background-image-url',
                        type='text',
                        placeholder='Input URL/URI...',
                    ),

                    drc.NamedRadioItems(
                        name='Image Crossorigin',
                        id='radio-background-image-crossorigin',
                        value='anonymous',
                        options=drc.DropdownOptionsList(
                            'anonymous',
                            'use-credentials'
                        )
                    ),

                    drc.NamedSlider(
                        name='Image Opacity',
                        id='slider-background-image-opacity',
                        min=0,
                        max=1,
                        marks={0: '0', 1: '1'},
                        step=0.05,
                        value=1
                    ),

                    drc.NamedInput(
                        name='Image Width (%)',
                        id='input-background-image-width',
                        type='number',
                        placeholder='Input value in %...'
                    ),

                    drc.NamedInput(
                        name='Image Height (%)',
                        id='input-background-image-height',
                        type='number',
                        placeholder='Input value in %...'
                    ),

                    drc.NamedRadioItems(
                        name='Image Fit',
                        id='radio-background-image-fit',
                        value='none',
                        options=drc.DropdownOptionsList(
                            'none',
                            'contain',
                            'cover'
                        )
                    ),

                    drc.NamedInput(
                        name='Image Position x (px/%)',
                        id='input-background-position-x',
                        type='text',
                        placeholder='Input value in % or px...',
                        value='50%'
                    ),
                    drc.NamedInput(
                        name='Image Position y (px/%)',
                        id='input-background-position-y',
                        type='text',
                        placeholder='Input value in % or px...',
                        value='50%'
                    ),
                    drc.NamedRadioItems(
                        name='Image Width Relative To',
                        id='radio-background-width-relative-to',
                        value='include-padding',
                        options=drc.DropdownOptionsList(
                            'inner',
                            'include-padding'
                        )
                    ),
                    drc.NamedRadioItems(
                        name='Image Height Relative To',
                        id='radio-background-height-relative-to',
                        value='include-padding',
                        options=drc.DropdownOptionsList(
                            'inner',
                            'include-padding'
                        )
                    ),
                ])
            ])
    ])
])


@app.callback(Output('input-background-image-height', 'disabled'),
              [Input('radio-background-image-fit', 'value')])
def disable_background_image_height(value):
    return value != 'none'


@app.callback(Output('input-background-image-width', 'disabled'),
              [Input('radio-background-image-fit', 'value')])
def disable_background_image_width(value):
    return value != 'none'


@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value')])
def update_layout(name):
    return {'name': name}


@app.callback(
    Output('cytoscape', 'stylesheet'),
    [Input(component, 'value') for component in [
        'input-node-content',
        'input-node-width',
        'input-node-height',
        'dropdown-node-shape',
        'input-node-color',
        'slider-node-opacity',
        'slider-node-blacken',
        'input-node-border-width',
        'dropdown-node-border-style',
        'input-node-border-color',
        'slider-node-border-opacity',
        'input-node-padding',
        'dropdown-node-padding-relative-to',
        'radio-node-compound-sizing',
        'input-node-compound-min-width',
        'input-node-compound-min-width-bias-left',
        'input-node-compound-min-width-bias-right',
        'input-node-compound-min-height',
        'input-node-compound-min-height-bias-top',
        'input-node-compound-min-height-bias-bottom',
        'input-background-image-url',
        'radio-background-image-crossorigin',
        'slider-background-image-opacity',
        'input-background-image-width',
        'input-background-image-height',
        'radio-background-image-fit',
        'input-background-position-x',
        'input-background-position-y',
        'radio-background-width-relative-to',
'radio-background-height-relative-to',
    ]]
)
def update_stylesheet(node_content,
                      node_width,
                      node_height,
                      node_shape,
                      node_color,
                      node_opacity,
                      node_blacken,
                      node_border_width,
                      node_border_style,
                      node_border_color,
                      node_border_opacity,
                      node_padding,
                      node_padding_relative_to,
                      node_compound_sizing,
                      node_compound_min_width,
                      node_compound_min_width_bias_left,
                      node_compound_min_width_bias_right,
                      node_compound_min_height,
                      node_compound_min_height_bias_top,
                      node_compound_min_height_bias_bottom,
                      background_image_url,
                      background_image_crossorigin,
                      background_image_opacity,
                      background_image_width,
                      background_image_height,
                      background_image_fit,
                      background_position_x,
                      background_position_y,
                      background_width_relative_to,
                      background_height_relative_to):
    def update_style(stylesheet, selector, addition):
        for style in stylesheet:
            if style['selector'] == selector:
                style['style'].update(addition)

    # Validating Input
    node_color = validate_color(node_color)
    node_border_color = validate_color(node_border_color)
    node_padding = validate_px_percentage(node_padding)
    background_position_x = validate_px_percentage(background_position_x)
    background_position_y = validate_px_percentage(background_position_y)

    if not background_image_url:
        background_image_url = 'none'

    stylesheet = [
        {
            'selector': 'node',
            'style': {
                'content': node_content,
                'width': node_width,
                'height': node_height,
                'background-color': node_color,
                'background-blacken': node_blacken,
                'background-opacity': node_opacity,
                'shape': node_shape,
                'border-width': node_border_width,
                'border-style': node_border_style,
                'border-color': node_border_color,
                'border-opacity': node_border_opacity,
                'padding': node_padding,
                'padding-relative-to': node_padding_relative_to,
                'compound-sizing-wrt-labels': node_compound_sizing,
                'min-width': node_compound_min_width,
                'min-width-bias-left': node_compound_min_width_bias_left,
                'min-width-bias-right': node_compound_min_width_bias_right,
                'min-height': node_compound_min_height,
                'min-height-bias-top': node_compound_min_height_bias_top,
                'min-height-bias-bottom': node_compound_min_height_bias_bottom,
                'background-image': background_image_url,
                'background-image-crossorigin': background_image_crossorigin,
                'background-image-opacity': background_image_opacity,
                'background-fit': background_image_fit,
                'background-position-x': background_position_x,
                'background-position-y': background_position_y,
                'background-width-relative-to': background_width_relative_to,
                'background-height-relative-to': background_height_relative_to,
            }
        }
    ]

    # Handles background styles
    if background_image_fit == 'none':
        if background_image_width is None:
            background_image_width = 'auto'

        if background_image_height is None:
            background_image_height = 'auto'

        update_style(
            stylesheet=stylesheet,
            selector='node',
            addition={
                'background-width': background_image_width,
                'background-height': background_image_height
            }
        )

    return stylesheet


if __name__ == '__main__':
    app.run_server(debug=True)
