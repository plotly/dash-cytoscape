/**
 * JavaScript Requirements: cytoscape
 * React.js requirements: cytoscape-reactjs
 */
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import CytoscapeComponent from '../../react-cytoscapejs/src/component.js';


export default class Cytoscape extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        const {
            id,
            style,
            className,
            elements,
            stylesheet,
            layout,
            pan,
            zoom,
            panningEnabled,
            userPanningEnabled,
            minZoom,
            maxZoom,
            zoomingEnabled,
            userZoomingEnabled,
            boxSelectionEnabled,
            autoungrabify,
            autolock,
            autounselectify
        } = this.props;

        return (
            <CytoscapeComponent
                id={id}
                className={className}
                style={style}
                elements={elements}
                stylesheet={stylesheet}
                layout={layout}
                pan={pan}
                zoom={zoom}
                panningEnabled={panningEnabled}
                userPanningEnabled={userPanningEnabled}
                minZoom={minZoom}
                maxZoom={maxZoom}
                zoomingEnabled={zoomingEnabled}
                userZoomingEnabled={userZoomingEnabled}
                boxSelectionEnabled={boxSelectionEnabled}
                autoungrabify={autoungrabify}
                autolock={autolock}
                autounselectify={autounselectify}
            />
        )
    }
}


Cytoscape.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string,

    /**
     * Html Class of the component
     */
    className: PropTypes.string,

    /**
     * Add inline styles to the root element
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func,

    // Basic Props
    /**
     * The flat list of Cytoscape elements to be included in the graph, each
     * represented as non-stringified JSON.
     */
    elements: PropTypes.oneOfType([
        PropTypes.object,
        PropTypes.arrayOf(PropTypes.object),
    ]),

    /**
     * The Cytoscape stylesheet as non-stringified JSON. N.b. the prop key is
     * stylesheet rather than style, the key used by Cytoscape itself, so as
     * to not conflict with the HTML style attribute.
     */
    stylesheet: PropTypes.oneOfType([
        PropTypes.object,
        PropTypes.arrayOf(PropTypes.object),
    ]),

    /**
     * The function of a layout is to set the positions on the nodes in the
     * graph. Layouts are extensions of Cytoscape.js such that it is possible
     * for anyone to write a layout without modifying the library itself.
     *
     * To use a layout, input a dictionary with "name" as the key, e.g.
     * ```
     * {"name": layout_name}
     *
     * Several layouts are included with Cytoscape by default, and their
     * options are described with the default values specified in the official
     * documentation
     *
     * null: The null layout puts all nodes at (0, 0). It’s useful for debugging purposes.
     * random:  The random layout puts nodes in random positions within the viewport.
     * preset: The preset layout puts nodes in the positions you specify manually.
     * grid: The grid layout puts nodes in a well-spaced grid.
     * circle: The circle layout puts nodes in a circle.
     * concentric: The concentric layout positions nodes in concentric circles, based on a metric that you specify to segregate the nodes into levels.
     * breadthfirst: The breadthfirst layout puts nodes in a hierarchy, based on a breadthfirst traversal of the graph.
     * cose: The cose (Compound Spring Embedder) layout uses a physics simulation to lay out graphs. It works well with noncompound graphs and it has additional logic to support compound graphs well.
     *
     * The official Cytoscape.js documentation gives an extensive explanation
     * of the layout property, as well as use cases:
     * http://js.cytoscape.org/#layouts
     */
    layout: PropTypes.object,

    // Viewport Manipulation
    /**
     * The initial panning position of the graph. Make sure to disable viewport
     * manipulation options, such as fit, in your layout so that it is not
     * overridden when the layout is applied.
     */
    pan: PropTypes.object,

    /**
     * The initial zoom level of the graph. Make sure to disable viewport
     * manipulation options, such as fit, in your layout so that it is not
     * overridden when the layout is applied. You can set options.minZoom and
     * options.maxZoom to set restrictions on the zoom level.
     */
    zoom: PropTypes.number,

    // Viewport Mutability and gesture Toggling
    /**
     * Whether panning the graph is enabled, both by user events and programmatically.
     */
    panningEnabled: PropTypes.bool,

    /**
     * Whether user events (e.g. dragging the graph background) are allowed to pan the graph. Programmatic changes to pan are unaffected by this option.
     */
    userPanningEnabled: PropTypes.bool,

    /**
     * A minimum bound on the zoom level of the graph. The viewport can not be scaled smaller than this zoom level.
     */
    minZoom: PropTypes.number,

    /**
     * A maximum bound on the zoom level of the graph. The viewport can not be
     * scaled larger than this zoom level.
     */
    maxZoom: PropTypes.number,

    /**
     * Whether zooming the graph is enabled, both by user events and programmatically.
     */
    zoomingEnabled: PropTypes.bool,

    /**
     * Whether user events (e.g. dragging the graph background) are allowed to pan the graph. Programmatic changes to pan are unaffected by this option.
     */
    userZoomingEnabled: PropTypes.bool,

    /**
     * Whether box selection (i.e. drag a box overlay around, and release it to select) is enabled. If enabled, the user must taphold to pan the graph.
     */
    boxSelectionEnabled: PropTypes.bool,

    /**
     * Whether nodes should be ungrabified (not grabbable by user) by default (if true, overrides individual node state).
     */
    autoungrabify: PropTypes.bool,

    /**
     * Whether nodes should be locked (not draggable at all) by default (if true, overrides individual node state).
     */
    autolock: PropTypes.bool,

    /**
     * Whether nodes should be unselectified (immutable selection state) by default (if true, overrides individual element state).
     */
    autounselectify: PropTypes.bool
};

Cytoscape.defaultProps = {
    style: {width: '600px', height: '600px'},
    layout: {name: 'random'}
};