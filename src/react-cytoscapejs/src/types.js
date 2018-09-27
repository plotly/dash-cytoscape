import PropTypes from 'prop-types';

const { string, array, object, number, bool, oneOfType, any, func } = PropTypes;

export const types = {
  /**
   * The `id` HTML attribute of the component.
   * */
  id: string,

  /**
   * The `class` HTML attribute of the component.  Use this to set the dimensions of
   * the graph visualisation via a style block in your CSS file.
   */
  className: string,

  /**
   * The `style` HTML attribute of the component.  Use this to set the dimensions of
   * the graph visualisation if you do not use separate CSS files.
   */
  style: oneOfType([string, object]),

  /**
   * The flat list of Cytoscape elements to be included in the graph, each represented
   * as non-stringified JSON.  E.g.:
   *
   * ```
   * elements: [
   *   { data: { id: 'one', label: 'Node 1' }, position: { x: 0, y: 0 } },
   *   { data: { id: 'two', label: 'Node 2' }, position: { x: 100, y: 0 } },
   *   { data: { source: 'one', target: 'two', label: 'Edge from Node1 to Node2' } }
   * ]
   * ```
   *
   * See http://js.cytoscape.org/#notation/elements-json
   * */
  elements: oneOfType([array, any]),

  /**
   * The Cytoscape stylesheet as non-stringified JSON.  E.g.:
   *
   * ```
   * stylesheet: [
   *   {
   *      selector: 'node',
   *      style: {
   *        'width': 30,
   *        'height': 30,
   *        'shape': 'rectangle'
   *      }
   *   }
   * ]
   * ```
   *
   * See http://js.cytoscape.org/#style
   */
  stylesheet: oneOfType([array, any]),

  /**
   * Use a layout to automatically position the nodes in the graph.  E.g.
   *
   * ```
   * layout: { name: 'random' }
   * ```
   *
   * N.b. to use an external layout extension, you must register the extension
   * prior to rendering this component, e.g.:
   *
   * ```
   * import Cytoscape from 'cytoscape';
   * import COSEBilkent from 'cytoscape-cose-bilkent';
   * import React from 'react';
   * import CytoscapeComponent from 'cytoscape-reactjs';
   *
   * Cytoscape.use(COSEBilkent);
   *
   * class MyApp extends React.Component {
   *   render() {
   *     const elements = [
   *       { data: { id: 'one', label: 'Node 1' }, position: { x: 0, y: 0 } },
   *       { data: { id: 'two', label: 'Node 2' }, position: { x: 100, y: 0 } },
   *       { data: { source: 'one', target: 'two', label: 'Edge from Node1 to Node2' } }
   *     ];
   *
   *     const layout = { name: 'cose-bilkent' };
   *
   *     return <CytoscapeComponent elements={elements} layout={layout}>;
   *   }
   * }
   * ```
   *
   * See http://js.cytoscape.org/#layouts
   */
  layout: oneOfType([object, any]),

  /**
   * The panning position of the graph.
   *
   * See http://js.cytoscape.org/#init-opts/pan
   */
  pan: oneOfType([object, any]),

  /**
   * The zoom level of the graph.
   *
   * See http://js.cytoscape.org/#init-opts/zoom
   */
  zoom: number,

  /**
   * Whether the panning position of the graph is mutable overall.
   *
   * See http://js.cytoscape.org/#init-opts/panningEnabled
   */
  panningEnabled: bool,

  /**
   * Whether the panning position of the graph is mutable by user gestures (e.g. swipe).
   *
   * See http://js.cytoscape.org/#init-opts/userPanningEnabled
   */
  userPanningEnabled: bool,

  /**
   * The minimum zoom level of the graph.
   *
   * See http://js.cytoscape.org/#init-opts/minZoom
   */
  minZoom: number,

  /**
   * The maximum zoom level of the graph.
   *
   * See http://js.cytoscape.org/#init-opts/maxZoom
   */
  maxZoom: number,

  /**
   * Whether the zoom level of the graph is mutable overall.
   *
   * See http://js.cytoscape.org/#init-opts/zoomingEnabled
   */
  zoomingEnabled: bool,

  /**
   * Whether the zoom level of the graph is mutable by user gestures (e.g. pinch-to-zoom).
   *
   * See http://js.cytoscape.org/#init-opts/userZoomingEnabled
   */
  userZoomingEnabled: bool,

  /**
   * Whether shift+click-and-drag box selection is enabled.
   *
   * See http://js.cytoscape.org/#init-opts/boxSelectionEnabled
   */
  boxSelectionEnabled: bool,

  /**
   * If true, nodes automatically can not be grabbed regardless of whether
   * each node is marked as grabbable.
   *
   * See http://js.cytoscape.org/#init-opts/autoungrabify
   */
  autoungrabify: bool,

  /**
   * If true, nodes can not be moved at all.
   *
   * See http://js.cytoscape.org/#init-opts/autolock
   */
  autolock: bool,

  /**
   * If true, elements have immutable selection state.
   *
   * See http://js.cytoscape.org/#init-opts/autounselectify
   */
  autounselectify: bool,

  /**
   * `get(object, key)`
   * Get the value of the specified `object` at the `key`, which may be an integer
   * in the case of lists/arrays or strings in the case of maps/objects.
   */
  get: func,

  /**
   * `toJson(object)`
   * Get the deep value of the specified `object` as non-stringified JSON.
   */
  toJson: func,

  /**
   * diff(objectA, objectB)
   * Return whether the two objects have equal value. This is used to determine if
   * and where Cytoscape needs to be patched.
   */
  diff: func,

  /**
   * forEach(list, iterator)
   * Call `iterator` on each element in the `list`, in order.
   */
  forEach: func,

  /**
   * cy(cyRef)
   * The `cy` prop allows for getting a reference to the `cy` Cytoscape object, e.g.:
   *
   * `<CytoscapeComponent cy={cy => (myCyRef = cy)} />`
   */
  cy: func
};
