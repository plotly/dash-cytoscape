# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Cytoscape(Component):
    """A Cytoscape component.
A Component Library for Dash aimed at facilitating network visualization in
Python, wrapped around [Cytoscape.js](http://js.cytoscape.org/).

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- autoRefreshLayout (boolean; default True):
    Whether the layout should be refreshed when elements are added or
    removed.

- autolock (boolean; default False):
    Whether nodes should be locked (not draggable at all) by default
    (if True, overrides individual node state).

- autoungrabify (boolean; default False):
    Whether nodes should be ungrabified (not grabbable by user) by
    default (if True, overrides individual node state).

- autounselectify (boolean; default False):
    Whether nodes should be unselectified (immutable selection state)
    by default (if True, overrides individual element state).

- boxSelectionEnabled (boolean; default False):
    Whether box selection (i.e. drag a box overlay around, and release
    it to select) is enabled. If enabled, the user must taphold to pan
    the graph.

- className (string; optional):
    Sets the class name of the element (the value of an element's html
    class attribute).

- elements (list of dicts; optional):
    A list of dictionaries representing the elements of the networks.
    Each dictionary describes an element, and specifies its purpose.
    The [official Cytoscape.js
    documentation](https://js.cytoscape.org/#notation/elements-json)
    offers an extensive overview and examples of element declaration.
    Alternatively, a dictionary with the format { 'nodes': [],
    'edges': [] } is allowed at initialization, but arrays remain the
    recommended format.

    `elements` is a list of dicts with keys:

    - classes (string; optional):
        Space separated string of class names of the element. Those
        classes can be selected by a style selector.

    - data (dict; optional):
        Element specific data.

        `data` is a dict with keys:

        - id (string; optional):
            Reference to the element, useful for selectors and edges.
            Randomly assigned if not given.

        - label (string; optional):
            Optional name for the element, useful when `data(label)`
            is given to a style's `content` or `label`. It is only a
            convention.

        - parent (string; optional):
            Only for nodes. Optional reference to another node. Needed
            to create compound nodes.

        - source (string; optional):
            Only for edges. The id of the source node, which is where
            the edge starts.

        - target (string; optional):
            Only for edges. The id of the target node, where the edge
            ends.

    - grabbable (boolean; optional):
        Only for nodes. If the node can be grabbed and moved by the
        user.

    - group (string; optional):
        Either 'nodes' or 'edges'. If not given, it's automatically
        inferred.

    - locked (boolean; optional):
        Only for nodes. If the position is immutable.

    - position (dict; optional):
        Only for nodes. The position of the node.

        `position` is a dict with keys:

        - x (number; optional):
            The x-coordinate of the node.

        - y (number; optional):
            The y-coordinate of the node.

    - selectable (boolean; optional):
        If the element can be selected.

    - selected (boolean; optional):
        If the element is selected upon initialisation.

      Or dict with keys:

    - edges (list; optional)

    - nodes (list; optional)

- generateImage (dict; optional):
    Dictionary specifying options to generate an image of the current
    cytoscape graph. Value is cleared after data is received and image
    is generated. This property will be ignored on the initial
    creation of the cytoscape object and must be invoked through a
    callback after it has been rendered.  If the app does not need the
    image data server side and/or it will only be used to download the
    image, it may be prudent to invoke `'download'` for `action`
    instead of `'store'` to improve performance by preventing transfer
    of data to the server.

    `generateImage` is a dict with keys:

    - action (a value equal to: 'store', 'download', 'both'; optional):
        `'store'`: Stores the image data (only jpg and png are
        supported) in `imageData` and invokes server-side Dash
        callbacks. `'download'`: Downloads the image as a file with
        all data handling done client-side. No `imageData` callbacks
        are fired. `'both'`: Stores image data and downloads image as
        file. The default is `'store'`.

    - filename (string; optional):
        Name for the file to be downloaded. Default: 'cyto'.

    - options (dict; optional):
        Dictionary of options to cy.png() / cy.jpg() or cy.svg() for
        image generation. See https://js.cytoscape.org/#core/export
        for details. For `'output'`, only 'base64' and 'base64uri' are
        supported. Default: `{'output': 'base64uri'}`.

    - type (a value equal to: 'svg', 'png', 'jpg', 'jpeg'; optional):
        File type to output.

- imageData (string; optional):
    String representation of the image requested with generateImage.
    Null if no image was requested yet or the previous request failed.
    Read-only.

- layout (dict; default {name: 'grid'}):
    A dictionary specifying how to set the position of the elements in
    your graph. The `'name'` key is required, and indicates which
    layout (algorithm) to use. The keys accepted by `layout` vary
    depending on the algorithm, but these keys are accepted by all
    layouts: `fit`,  `padding`, `animate`, `animationDuration`,
    `boundingBox`.   The complete list of layouts and their accepted
    options are available on the  [Cytoscape.js
    docs](https://js.cytoscape.org/#layouts) . For the external
    layouts, the options are listed in the \"API\" section of the
    README.  Note that certain keys are not supported in Dash since
    the value is a JavaScript  function or a callback. Please visit
    this [issue](https://github.com/plotly/dash-cytoscape/issues/25)
    for more information.

    `layout` is a dict with keys:

    - animate (boolean; optional):
        Whether to animate change in position when the layout changes.

    - animationDuration (number; optional):
        Duration of animation in milliseconds, if enabled.

    - boundingBox (dict; optional):
        How to constrain the layout in a specific area. Keys accepted
        are either `x1, y1, x2, y2` or `x1, y1, w, h`, all of which
        receive a pixel value.

    - fit (boolean; optional):
        Whether to render the nodes in order to fit the canvas.

    - name (a value equal to: 'random', 'preset', 'circle', 'concentric', 'grid', 'breadthfirst', 'cose', 'close-bilkent', 'cola', 'euler', 'spread', 'dagre', 'klay'; required):
        The layouts available by default are:   `random`: Randomly
        assigns positions.   `preset`: Assigns position based on the
        `position` key in element dictionaries.   `circle`:
        Single-level circle, with optional radius.   `concentric`:
        Multi-level circle, with optional radius.   `grid`: Square
        grid, optionally with numbers of `rows` and `cols`.
        `breadthfirst`: Tree structure built using BFS, with optional
        `roots`.   `cose`: Force-directed physics simulation.  Some
        external layouts are also included. To use them, run
        `dash_cytoscape.load_extra_layouts()` before creating your
        Dash app. Be careful about   using the extra layouts when not
        necessary, since they require supplementary bandwidth   for
        loading, which impacts the startup time of the app.   The
        external layouts are:
        [cose-bilkent](https://github.com/cytoscape/cytoscape.js-cose-bilkent),
        [cola](https://github.com/cytoscape/cytoscape.js-cola),
        [euler](https://github.com/cytoscape/cytoscape.js-dagre),
        [spread](https://github.com/cytoscape/cytoscape.js-spread),
        [dagre](https://github.com/cytoscape/cytoscape.js-dagre),
        [klay](https://github.com/cytoscape/cytoscape.js-klay),.

    - padding (number; optional):
        Padding around the sides of the canvas, if fit is enabled.

- maxZoom (number; default 1e50):
    A maximum bound on the zoom level of the graph. The viewport can
    not be scaled larger than this zoom level.

- minZoom (number; default 1e-50):
    A minimum bound on the zoom level of the graph. The viewport can
    not be scaled smaller than this zoom level.

- mouseoverEdgeData (dict; optional):
    The data dictionary of an edge returned when you hover over it.
    Read-only.

- mouseoverNodeData (dict; optional):
    The data dictionary of a node returned when you hover over it.
    Read-only.

- pan (dict; default {x: 0, y: 0}):
    Dictionary indicating the initial panning position of the graph.
    The following keys are accepted:.

    `pan` is a dict with keys:

    - x (number; optional):
        The x-coordinate of the node.

    - y (number; optional):
        The y-coordinate of the node.

- panningEnabled (boolean; default True):
    Whether panning the graph is enabled (i.e., the position of the
    graph is mutable overall).

- responsive (boolean; default False):
    Toggles intelligent responsive resize of Cytoscape graph with
    viewport size change.

- selectedEdgeData (list; optional):
    The list of data dictionaries of all selected edges (e.g. using
    Shift+Click to select multiple nodes, or Shift+Drag to use box
    selection). Read-only.

- selectedNodeData (list; optional):
    The list of data dictionaries of all selected nodes (e.g. using
    Shift+Click to select multiple nodes, or Shift+Drag to use box
    selection). Read-only.

- style (dict; default {width: '600px', height: '600px'}):
    Add inline styles to the root element.

- stylesheet (list of dicts; optional):
    A list of dictionaries representing the styles of the elements.
    Each dictionary requires the following keys: `selector` and
    `style`.  Both the [selector](https://js.cytoscape.org/#selectors)
    and the [style](https://js.cytoscape.org/#style/node-body) are
    exhaustively documented in the Cytoscape.js docs. Although methods
    such as `cy.elements(...)` and `cy.filter(...)` are not available,
    the selector string syntax stays the same.

    `stylesheet` is a list of dicts with keys:

    - selector (string; required):
        Which elements you are styling. Generally, you select a group
        of elements (node, edges, both), a class (that you declare in
        the element dictionary), or an element by ID.

    - style (dict; required):
        What aspects of the elements you want to modify. This could be
        the size or color of a node, the shape of an edge arrow, or
        many more.

- tapEdge (dict; optional):
    The complete edge dictionary returned when you tap or click it.
    Read-only.

    `tapEdge` is a dict with keys:

    - classes (string; optional):
        General item (for all elements).

    - data (dict; optional):
        General item (for all elements).

    - grabbable (boolean; optional):
        General item (for all elements).

    - group (string; optional):
        General item (for all elements).

    - isLoop (boolean; optional):
        Edge-specific item.

    - isSimple (boolean; optional):
        Edge-specific item.

    - locked (boolean; optional):
        General item (for all elements).

    - midpoint (dict; optional):
        Edge-specific item.

    - selectable (boolean; optional):
        General item (for all elements).

    - selected (boolean; optional):
        General item (for all elements).

    - sourceData (dict; optional):
        Edge-specific item.

    - sourceEndpoint (dict; optional):
        Edge-specific item.

    - style (dict; optional):
        General item (for all elements).

    - targetData (dict; optional):
        Edge-specific item.

    - targetEndpoint (dict; optional):
        Edge-specific item.

    - timeStamp (number; optional):
        Edge-specific item.

- tapEdgeData (dict; optional):
    The data dictionary of an edge returned when you tap or click it.
    Read-only.

- tapNode (dict; optional):
    The complete node dictionary returned when you tap or click it.
    Read-only.

    `tapNode` is a dict with keys:

    - ancestorsData (dict | list; optional):
        Item for compound nodes.

    - childrenData (dict | list; optional):
        Item for compound nodes.

    - classes (string; optional):
        General item (for all elements).

    - data (dict; optional):
        General item (for all elements).

    - descendantsData (dict | list; optional):
        Item for compound nodes.

    - edgesData (list; optional):
        node specific item.

    - grabbable (boolean; optional):
        General item (for all elements).

    - group (string; optional):
        General item (for all elements).

    - isChild (boolean; optional):
        Item for compound nodes.

    - isChildless (boolean; optional):
        Item for compound nodes.

    - isOrphan (boolean; optional):
        Item for compound nodes.

    - isParent (boolean; optional):
        Item for compound nodes.

    - locked (boolean; optional):
        General item (for all elements).

    - parentData (dict | list; optional):
        Item for compound nodes.

    - position (dict; optional):
        General item (for all elements).

    - relativePosition (dict; optional):
        Item for compound nodes.

    - renderedPosition (dict; optional):
        node specific item.

    - selectable (boolean; optional):
        General item (for all elements).

    - selected (boolean; optional):
        General item (for all elements).

    - siblingsData (dict | list; optional):
        Item for compound nodes.

    - style (dict; optional):
        General item (for all elements).

    - timeStamp (number; optional):
        node specific item.

- tapNodeData (dict; optional):
    The data dictionary of a node returned when you tap or click it.
    Read-only.

- userPanningEnabled (boolean; default True):
    Whether user events (e.g. dragging the graph background) are
    allowed to pan the graph.

- userZoomingEnabled (boolean; default True):
    Whether user events (e.g. dragging the graph background) are
    allowed to pan the graph.

- zoom (number; default 1):
    The initial zoom level of the graph. You can set `minZoom` and
    `maxZoom` to set restrictions on the zoom level.

- zoomingEnabled (boolean; default True):
    Whether zooming the graph is enabled (i.e., the zoom level of the
    graph is mutable overall)."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, elements=Component.UNDEFINED, stylesheet=Component.UNDEFINED, layout=Component.UNDEFINED, pan=Component.UNDEFINED, zoom=Component.UNDEFINED, panningEnabled=Component.UNDEFINED, userPanningEnabled=Component.UNDEFINED, minZoom=Component.UNDEFINED, maxZoom=Component.UNDEFINED, zoomingEnabled=Component.UNDEFINED, userZoomingEnabled=Component.UNDEFINED, boxSelectionEnabled=Component.UNDEFINED, autoungrabify=Component.UNDEFINED, autolock=Component.UNDEFINED, autounselectify=Component.UNDEFINED, autoRefreshLayout=Component.UNDEFINED, tapNode=Component.UNDEFINED, tapNodeData=Component.UNDEFINED, tapEdge=Component.UNDEFINED, tapEdgeData=Component.UNDEFINED, mouseoverNodeData=Component.UNDEFINED, mouseoverEdgeData=Component.UNDEFINED, selectedNodeData=Component.UNDEFINED, selectedEdgeData=Component.UNDEFINED, generateImage=Component.UNDEFINED, imageData=Component.UNDEFINED, responsive=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'autoRefreshLayout', 'autolock', 'autoungrabify', 'autounselectify', 'boxSelectionEnabled', 'className', 'elements', 'generateImage', 'imageData', 'layout', 'maxZoom', 'minZoom', 'mouseoverEdgeData', 'mouseoverNodeData', 'pan', 'panningEnabled', 'responsive', 'selectedEdgeData', 'selectedNodeData', 'style', 'stylesheet', 'tapEdge', 'tapEdgeData', 'tapNode', 'tapNodeData', 'userPanningEnabled', 'userZoomingEnabled', 'zoom', 'zoomingEnabled']
        self._type = 'Cytoscape'
        self._namespace = 'dash_cytoscape'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'autoRefreshLayout', 'autolock', 'autoungrabify', 'autounselectify', 'boxSelectionEnabled', 'className', 'elements', 'generateImage', 'imageData', 'layout', 'maxZoom', 'minZoom', 'mouseoverEdgeData', 'mouseoverNodeData', 'pan', 'panningEnabled', 'responsive', 'selectedEdgeData', 'selectedNodeData', 'style', 'stylesheet', 'tapEdge', 'tapEdgeData', 'tapNode', 'tapNodeData', 'userPanningEnabled', 'userZoomingEnabled', 'zoom', 'zoomingEnabled']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Cytoscape, self).__init__(**args)
