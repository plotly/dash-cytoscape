import json

import pprint
import dash
import dash_core_components as dcc
import dash_html_components as html
from colour import Color
from dash.dependencies import Input, Output, State

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
        'target': 'four',
        'label': 'Edge from Node 4 to Node 4'
    }},
    {'data': {
        'source': 'four',
        'target': 'six',
        'label': 'Edge from Node 4 to Node 6'
    }},
    {'data': {
        'source': 'five',
        'target': 'one',
        'label': 'Edge from Node 5 to Node 1'
    }},
]


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_positive(value):
    return min(0, value)


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
    if not value:
        return default
    elif 'px' in value and is_float(value.replace('px', '')):
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
                        min=0,
                        value=25,
                        placeholder='Enter a value in pixel...'
                    ),

                    drc.NamedInput(
                        name='Node Height (px)',
                        id='input-node-height',
                        type='number',
                        min=0,
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
                        min=0,
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
                        min=0,
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Extra width on left side (%)',
                        id='input-node-compound-min-width-bias-left',
                        type='number',
                        min=0,
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Extra width on right side (%)',
                        id='input-node-compound-min-width-bias-right',
                        type='number',
                        min=0,
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Parent Node Min Height (px)',
                        id='input-node-compound-min-height',
                        type='number',
                        min=0,
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Extra height on top side (%)',
                        id='input-node-compound-min-height-bias-top',
                        type='number',
                        min=0,
                        placeholder='Input value in px...',
                        value=0
                    ),
                    drc.NamedInput(
                        name='Extra height on bottom side (%)',
                        id='input-node-compound-min-height-bias-bottom',
                        type='number',
                        min=0,
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
                drc.Card([
                    drc.NamedRadioItems(
                        name='Use Background Image',
                        id='radio-use-background-image',
                        options=drc.DropdownOptionsList('yes', 'no'),
                        value='no'
                    ),

                    drc.NamedInput(
                        name='Image URL/URI',
                        id='input-background-image-url',
                        type='text',
                        placeholder='Input URL/URI...',
                        value='https://farm8.staticflickr.com/7272/7633179468_3e19e45a0c_b.jpg'
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
                        min=0,
                        placeholder='Input value in %...'
                    ),

                    drc.NamedInput(
                        name='Image Height (%)',
                        id='input-background-image-height',
                        type='number',
                        min=0,
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
                ]),

                drc.SectionTitle(
                    title='Pie Chart Background',
                    size=3,
                    color='white'
                ),
                drc.Card([
                    drc.NamedRadioItems(
                        name='Use Pie Chart for Background',
                        id='radio-use-pie-chart',
                        options=drc.DropdownOptionsList('yes', 'no'),
                        value='no'
                    ),
                    drc.NamedDropdown(
                        name='Select Pie Slice to modify',
                        id='dropdown-pie-slice-selected',
                        options=[{
                            'label': f'Slice #{n}',
                            'value': f'div-pie-slice-{n}'
                        } for n in range(1, 17)],
                        value='div-pie-slice-1',
                        clearable=False
                    ),
                    drc.NamedInput(
                        name='Diameter of Pie (%/px)',
                        id='input-pie-size',
                        type='text',
                        placeholder='Input value in % or px...'
                    ),
                    html.Div(
                        id='div-storage-pie-background-color',
                        style={'display': 'none'}
                    ),
                    html.Div(
                        id='div-storage-pie-background-size',
                        style={'display': 'none'}
                    ),
                    html.Div(
                        id='div-storage-pie-background-opacity',
                        style={'display': 'none'}
                    ),
                    *[html.Div(
                        id=f'div-pie-slice-{n}',
                        style={'display': 'block'},
                        children=[
                            drc.NamedInput(
                                name=f'Color of slice #{n}',
                                id=f'input-pie-{n}-background-color',
                                type='text',
                                placeholder='Input Color in Hex...'
                            ),
                            drc.NamedInput(
                                name=f'Size of slice #{n} (%)',
                                id=f'input-pie-{n}-background-size',
                                type='number',
                                min=0,
                                placeholder='Input value in %...'
                            ),
                            drc.NamedSlider(
                                name=f'Opacity of slice #{n}',
                                id=f'slider-pie-{n}-background-opacity',
                                min=0,
                                max=1,
                                marks={0: '0', 1: '1'},
                                step=0.05,
                                value=1
                            )
                        ]
                    ) for n in range(1, 17)]
                ]),

                drc.SectionTitle(
                    title='Edges',
                    size=3,
                    color='white'
                ),

                # TODO: Add options to modify (unbundled) bezier edges, haystack edges
                drc.NamedCard(title='Edge line', size=4, children=[
                    drc.NamedInput(
                        name='Line Width (px)',
                        id='input-edge-line-width',
                        type='number',
                        min=0,
                        placeholder='Input value in px...'
                    ),
                    drc.NamedDropdown(
                        name='Curving Method',
                        id='dropdown-edge-curve-style',
                        value='haystack',
                        clearable=False,
                        searchable=False,
                        options=drc.DropdownOptionsList(
                            'haystack',
                            'bezier',
                            'unbundled-bezier',
                            'segments',
                        )
                    ),
                    drc.NamedInput(
                        name=f'Line Color',
                        id='input-edge-line-color',
                        type='text',
                        placeholder='Input Color in Hex...'
                    ),
                    drc.NamedRadioItems(
                        name='Line Style',
                        id='radio-edge-line-style',
                        value='solid',
                        options=drc.DropdownOptionsList(
                            'solid',
                            'dotted',
                            'dashed'
                        )
                    )
                ]),
                drc.NamedCard(title='Loop edges', size=4, children=[
                    drc.NamedInput(
                        name='Direction of loop (angle degree)',
                        id='input-edge-loop-direction',
                        type='number',
                        value=-45,
                        placeholder='Input value in deg...'
                    ),
                    drc.NamedInput(
                        name='Loop Sweep (angle degree)',
                        id='input-edge-loop-sweep',
                        type='number',
                        value=-90,
                        placeholder='Input value in deg...'
                    )
                ]),
                drc.NamedCard(title='Edge Arrow', size=4, children=[
                    drc.NamedRadioItems(
                        name='Use Edge Arrow',
                        id='radio-use-edge-arrow',
                        options=drc.DropdownOptionsList('yes', 'no'),
                        value='no'
                    ),

                    drc.NamedDropdown(
                        name='Select Arrow Position',
                        id='dropdown-arrow-position',
                        options=[{
                            'label': pos.capitalize(),
                            'value': f'div-arrow-position-{pos}'
                        } for pos in [
                            'source',
                            'mid-source',
                            'target',
                            'mid-target'
                        ]],
                        value='div-arrow-position-source',
                        clearable=False
                    ),

                    *[html.Div(
                        id=f'div-arrow-position-{pos}',
                        style={'display': 'block'},
                        children=[
                            drc.NamedInput(
                                name=f'Arrow Color for {pos}',
                                id=f'input-{pos}-arrow-color',
                                type='text',
                                placeholder='Input Color in Hex...'
                            ),
                            drc.NamedDropdown(
                                name=f'Arrow Shape for {pos}',
                                id=f'dropdown-{pos}-arrow-color',
                                options=drc.DropdownOptionsList(
                                    'triangle',
                                    'triangle-tee',
                                    'triangle-cross',
                                    'triangle-backcurve',
                                    'vee',
                                    'tee',
                                    'square',
                                    'circle',
                                    'diamond',
                                    'none'
                                ),
                                clearable=False,
                                value='triangle'
                            ),
                            drc.NamedRadioItems(
                                name=f'Arrow Fill for {pos}',
                                id=f'radio-{pos}-arrow-color',
                                options=drc.DropdownOptionsList(
                                    'filled',
                                    'hollow'
                                ),
                                value='filled'
                            )
                        ]
                    ) for pos in ['source',
                                  'mid-source',
                                  'target',
                                  'mid-target']],

                    drc.NamedInput(
                        name=f'Scale of Arrow Size',
                        id=f'input-arrow-scale',
                        type='number',
                        min=0,
                        placeholder='Input numerical value...'
                    ),
                ])
            ]
        )
    ])
])

for n in range(1, 17):
    @app.callback(Output(f'div-pie-slice-{n}', 'style'),
                  [Input('dropdown-pie-slice-selected', 'value')],
                  [State(f'div-pie-slice-{n}', 'id')])
    def hide_div_pie_slice(current_slice_selected, div_id):
        if current_slice_selected != div_id:
            return {'display': 'none'}
        else:
            return {'display': 'block'}

for pos in ['source',
            'mid-source',
            'target',
            'mid-target']:
    @app.callback(Output(f'div-arrow-position-{pos}', 'style'),
                  [Input('dropdown-arrow-position', 'value')],
                  [State(f'div-arrow-position-{pos}', 'id')])
    def hide_div_arrow_position(current_pos_selected, div_id):
        if current_pos_selected != div_id:
            return {'display': 'none'}
        else:
            return {'display': 'block'}


@app.callback(Output('div-storage-pie-background-color', 'children'),
              [Input(f'input-pie-{n}-background-color', 'value')
               for n in range(1, 17)])
def update_color_storage(*args):
    args = [validate_color(color) for color in args]
    return json.dumps(
        dict(
            zip(
                [f'pie-{i}-background-color' for i in range(1, 17)],
                args
            )
        )
    )


@app.callback(Output('div-storage-pie-background-size', 'children'),
              [Input(f'input-pie-{n}-background-size', 'value')
               for n in range(1, 17)])
def update_size_storage(*args):
    return json.dumps(
        dict(
            zip(
                [f'pie-{i}-background-size' for i in range(1, 17)],
                args
            )
        )
    )


@app.callback(Output('div-storage-pie-background-opacity', 'children'),
              [Input(f'slider-pie-{n}-background-opacity', 'value')
               for n in range(1, 17)])
def update_opacity_storage(*args):
    return json.dumps(
        dict(
            zip(
                [f'pie-{i}-background-opacity' for i in range(1, 17)],
                args
            )
        )
    )


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
        # Node Body
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

        # Background Image
        'radio-use-background-image',
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
        'radio-use-pie-chart',
        'input-pie-size',
    ]] +
    [Input(div, 'children') for div in [
        'div-storage-pie-background-color',
        'div-storage-pie-background-size',
        'div-storage-pie-background-opacity',
    ]] +
    [Input(component, 'value') for component in [
        'input-edge-line-width',
        'dropdown-edge-curve-style',
        'input-edge-line-color',
        'radio-edge-line-style',
        'input-edge-loop-direction',
        'input-edge-loop-sweep'
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
                      use_background_image,
                      background_image_url,
                      background_image_crossorigin,
                      background_image_opacity,
                      background_image_width,
                      background_image_height,
                      background_image_fit,
                      background_position_x,
                      background_position_y,
                      background_width_relative_to,
                      background_height_relative_to,
                      use_pie_chart,
                      pie_size,
                      string_pie_background_color,
                      string_pie_background_size,
                      string_pie_background_opacity,
                      edge_line_width,
                      edge_curve_style,
                      edge_line_color,
                      edge_line_style,
                      edge_loop_direction,
                      edge_loop_sweep):
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
    pie_size = validate_px_percentage(pie_size, default='100%')
    edge_line_color = validate_color(edge_line_color)

    stylesheet = [{
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
        }
    }, {
        'selector': 'edge',
        'style': {
            'width': edge_line_width,
            'curve-style': edge_curve_style,
            'line-color': edge_line_color,
            'line-style': edge_line_style,
            'loop-direction': f'{edge_loop_direction}deg',
            'loop-sweep': f'{edge_loop_sweep}deg'
        }
    }]

    # Adds specified parameters if use background image is set to yes
    if use_background_image == 'yes':
        if not background_image_url:
            background_image_url = 'none'

        update_style(
            stylesheet=stylesheet,
            selector='node',
            addition={
                'background-image': background_image_url,
                'background-image-crossorigin': background_image_crossorigin,
                'background-image-opacity': background_image_opacity,
                'background-fit': background_image_fit,
                'background-position-x': background_position_x,
                'background-position-y': background_position_y,
                'background-width-relative-to': background_width_relative_to,
                'background-height-relative-to': background_height_relative_to,
            }
        )

    # If Background image fit is not set, we switch to using image width
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

    if use_pie_chart == 'yes':
        # Load json data from string format
        pie_background_color = json.loads(string_pie_background_color)
        pie_background_size = json.loads(string_pie_background_size)
        pie_background_opacity = json.loads(string_pie_background_opacity)

        update_style(
            stylesheet=stylesheet,
            selector='node',
            addition={
                'pie-size': pie_size,
                **pie_background_color,
                **pie_background_size,
                **pie_background_opacity
            }
        )

    return stylesheet


if __name__ == '__main__':
    app.run_server(debug=True)
