# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Cytoscape(Component):
    """A Cytoscape component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- className (string; optional): Html Class of the component
- style (dict; optional): Add inline styles to the root element
- elements (list; optional): The flat list of Cytoscape elements to be included in the graph, each
represented as non-stringified JSON.
- stylesheet (list; optional): The Cytoscape stylesheet as non-stringified JSON. N.b. the prop key is
stylesheet rather than style, the key used by Cytoscape itself, so as
to not conflict with the HTML style attribute.
- layout (dict; optional): The function of a layout is to set the positions on the nodes in the
graph.
- pan (dict; optional): The initial panning position of the graph. Make sure to disable viewport
manipulation options, such as fit, in your layout so that it is not
overridden when the layout is applied.
- zoom (number; optional): The initial zoom level of the graph. Make sure to disable viewport
manipulation options, such as fit, in your layout so that it is not
overridden when the layout is applied. You can set options.minZoom and
options.maxZoom to set restrictions on the zoom level.
- panningEnabled (boolean; optional): Whether panning the graph is enabled, both by user events and programmatically.
- userPanningEnabled (boolean; optional): Whether user events (e.g. dragging the graph background) are allowed to pan the graph. Programmatic changes to pan are unaffected by this option.
- minZoom (number; optional): A minimum bound on the zoom level of the graph. The viewport can not be scaled smaller than this zoom level.
- maxZoom (number; optional): A maximum bound on the zoom level of the graph. The viewport can not be
scaled larger than this zoom level.
- zoomingEnabled (boolean; optional): Whether zooming the graph is enabled, both by user events and programmatically.
- userZoomingEnabled (boolean; optional): Whether user events (e.g. dragging the graph background) are allowed to pan the graph. Programmatic changes to pan are unaffected by this option.
- boxSelectionEnabled (boolean; optional): Whether box selection (i.e. drag a box overlay around, and release it to select) is enabled. If enabled, the user must taphold to pan the graph.
- autoungrabify (boolean; optional): Whether nodes should be ungrabified (not grabbable by user) by default (if true, overrides individual node state).
- autolock (boolean; optional): Whether nodes should be locked (not draggable at all) by default (if true, overrides individual node state).
- autounselectify (boolean; optional): Whether nodes should be unselectified (immutable selection state) by default (if true, overrides individual element state).
- autoRefreshLayout (boolean; optional): Whether the layout should be refreshed when elements are added or removed
- tapNode (dict; optional): The trimmed node object returned when you tap a node
- tapNodeData (dict; optional): The data property of the node object returned when you tap a node
- tapEdge (dict; optional): The trimmed edge object returned when you tap a node
- tapEdgeData (dict; optional): The data property of the edge object returned when you tap a node
- mouseoverNodeData (dict; optional): The data property of the edge object returned when you hover over a node
- mouseoverEdgeData (dict; optional): The data property of the edge object returned when you hover over an edge
- selectedNodeData (list; optional): The array of node data currently selected by taps and boxes
- selectedEdgeData (list; optional): The array of edge data currently selected by taps and boxes

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, elements=Component.UNDEFINED, stylesheet=Component.UNDEFINED, layout=Component.UNDEFINED, pan=Component.UNDEFINED, zoom=Component.UNDEFINED, panningEnabled=Component.UNDEFINED, userPanningEnabled=Component.UNDEFINED, minZoom=Component.UNDEFINED, maxZoom=Component.UNDEFINED, zoomingEnabled=Component.UNDEFINED, userZoomingEnabled=Component.UNDEFINED, boxSelectionEnabled=Component.UNDEFINED, autoungrabify=Component.UNDEFINED, autolock=Component.UNDEFINED, autounselectify=Component.UNDEFINED, autoRefreshLayout=Component.UNDEFINED, tapNode=Component.UNDEFINED, tapNodeData=Component.UNDEFINED, tapEdge=Component.UNDEFINED, tapEdgeData=Component.UNDEFINED, mouseoverNodeData=Component.UNDEFINED, mouseoverEdgeData=Component.UNDEFINED, selectedNodeData=Component.UNDEFINED, selectedEdgeData=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'style', 'elements', 'stylesheet', 'layout', 'pan', 'zoom', 'panningEnabled', 'userPanningEnabled', 'minZoom', 'maxZoom', 'zoomingEnabled', 'userZoomingEnabled', 'boxSelectionEnabled', 'autoungrabify', 'autolock', 'autounselectify', 'autoRefreshLayout', 'tapNode', 'tapNodeData', 'tapEdge', 'tapEdgeData', 'mouseoverNodeData', 'mouseoverEdgeData', 'selectedNodeData', 'selectedEdgeData']
        self._type = 'Cytoscape'
        self._namespace = 'dash_cytoscape'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'className', 'style', 'elements', 'stylesheet', 'layout', 'pan', 'zoom', 'panningEnabled', 'userPanningEnabled', 'minZoom', 'maxZoom', 'zoomingEnabled', 'userZoomingEnabled', 'boxSelectionEnabled', 'autoungrabify', 'autolock', 'autounselectify', 'autoRefreshLayout', 'tapNode', 'tapNodeData', 'tapEdge', 'tapEdgeData', 'mouseoverNodeData', 'mouseoverEdgeData', 'selectedNodeData', 'selectedEdgeData']
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

    def __repr__(self):
        if(any(getattr(self, c, None) is not None
               for c in self._prop_names
               if c is not self._prop_names[0])
           or any(getattr(self, c, None) is not None
                  for c in self.__dict__.keys()
                  if any(c.startswith(wc_attr)
                  for wc_attr in self._valid_wildcard_attributes))):
            props_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self._prop_names
                                      if getattr(self, c, None) is not None])
            wilds_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self.__dict__.keys()
                                      if any([c.startswith(wc_attr)
                                      for wc_attr in
                                      self._valid_wildcard_attributes])])
            return ('Cytoscape(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Cytoscape(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
