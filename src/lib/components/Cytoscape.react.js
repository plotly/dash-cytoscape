/**
 * JavaScript Requirements: cytoscape, cytoscape-svg
 * React.js requirements: react-cytoscapejs
 */
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import CytoscapeComponent from 'react-cytoscapejs';
import _ from 'lodash';

import CyResponsive from '../cyResponsive.js';

/**
A Component Library for Dash aimed at facilitating network visualization in
Python, wrapped around [Cytoscape.js](http://js.cytoscape.org/).
 */
class Cytoscape extends Component {
    constructor(props) {
        super(props);

        this.handleCy = this.handleCy.bind(this);
        this._handleCyCalled = false;
        this.handleImageGeneration = this.handleImageGeneration.bind(this)
        this.cyResponsiveClass = false;
    }

    generateNode(event) {
        const ele = event.target;

        const isParent = ele.isParent(),
            isChildless = ele.isChildless(),
            isChild = ele.isChild(),
            isOrphan = ele.isOrphan(),
            renderedPosition = ele.renderedPosition(),
            relativePosition = ele.relativePosition(),
            parent = ele.parent(),
            style = ele.style();

        // Trim down the element objects to only the data contained
        const edgesData = ele.connectedEdges().map(ele => {
                return ele.data()
            }),
            childrenData = ele.children().map(ele => {
                return ele.data()
            }),
            ancestorsData = ele.ancestors().map(ele => {
                return ele.data()
            }),
            descendantsData = ele.descendants().map(ele => {
                return ele.data()
            }),
            siblingsData = ele.siblings().map(ele => {
                return ele.data()
            });

        const {timeStamp} = event;
        const {
            classes,
            data,
            grabbable,
            group,
            locked,
            position,
            selected,
            selectable
        } = ele.json();

        let parentData;
        if (parent) {
            parentData = parent.data();
        } else {
            parentData = null;
        }

        const nodeObject = {
            // Nodes attributes
            edgesData,
            renderedPosition,
            timeStamp,
            // From ele.json()
            classes,
            data,
            grabbable,
            group,
            locked,
            position,
            selectable,
            selected,
            // Compound Nodes additional attributes
            ancestorsData,
            childrenData,
            descendantsData,
            parentData,
            siblingsData,
            isParent,
            isChildless,
            isChild,
            isOrphan,
            relativePosition,
            // Styling
            style
        };
        return nodeObject;
    }


    generateEdge(event) {
        const ele = event.target;

        const midpoint = ele.midpoint(),
            isLoop = ele.isLoop(),
            isSimple = ele.isSimple(),
            sourceData = ele.source().data(),
            sourceEndpoint = ele.sourceEndpoint(),
            style = ele.style(),
            targetData = ele.target().data(),
            targetEndpoint = ele.targetEndpoint();

        const {timeStamp} = event;
        const {
            classes,
            data,
            grabbable,
            group,
            locked,
            selectable,
            selected,
        } = ele.json();

        const edgeObject = {
            // Edges attributes
            isLoop,
            isSimple,
            midpoint,
            sourceData,
            sourceEndpoint,
            targetData,
            targetEndpoint,
            timeStamp,
            // From ele.json()
            classes,
            data,
            grabbable,
            group,
            locked,
            selectable,
            selected,
            // Styling
            style
        };

        return edgeObject;
    }

    handleCy(cy) {
        // If the cy pointer has not been modified, and handleCy has already
        // been called before, than we don't run this function.
        if (cy === this._cy && this._handleCyCalled) {
            return;
        }
        this._cy = cy;
        window.cy = cy;
        this._handleCyCalled = true;

        // ///////////////////////////////////// CONSTANTS /////////////////////////////////////////
        const SELECT_THRESHOLD = 100;

        const selectedNodes = cy.collection();
        const selectedEdges = cy.collection();

        // ///////////////////////////////////// FUNCTIONS /////////////////////////////////////////
        const refreshLayout = _.debounce(() => {
            /**
             * Refresh Layout if needed
             */
            const {
                autoRefreshLayout,
                layout
            } = this.props;

            if (autoRefreshLayout) {
                cy.layout(layout).run();
            }
        }, SELECT_THRESHOLD);

        const sendSelectedNodesData = _.debounce(() => {
            /**
             This function is repetitively called every time a node is selected
             or unselected, but keeps being debounced if it is called again
             within 100 ms (given by SELECT_THRESHOLD). Effectively, it only
             runs when all the nodes have been correctly selected/unselected and
             added/removed from the selectedNodes collection, and then updates
             the selectedNodeData prop.
             */
            const nodeData = selectedNodes.map(el => el.data());

            if (typeof this.props.setProps === 'function') {
                this.props.setProps({
                    selectedNodeData: nodeData
                })
            }
        }, SELECT_THRESHOLD);

        const sendSelectedEdgesData = _.debounce(() => {
            const edgeData = selectedEdges.map(el => el.data());

            if (typeof this.props.setProps === 'function') {
                this.props.setProps({
                    selectedEdgeData: edgeData
                })
            }
        }, SELECT_THRESHOLD);

        // /////////////////////////////////////// EVENTS //////////////////////////////////////////
        cy.on('tap', 'node', event => {
            const nodeObject = this.generateNode(event);

            if (typeof this.props.setProps === 'function') {
                this.props.setProps({
                    tapNode: nodeObject,
                    tapNodeData: nodeObject.data
                });
            }
        });

        cy.on('tap', 'edge', event => {
            const edgeObject = this.generateEdge(event);

            if (typeof this.props.setProps === 'function') {
                this.props.setProps({
                    tapEdge: edgeObject,
                    tapEdgeData: edgeObject.data
                });
            }
        });

        cy.on('mouseover', 'node', event => {
            if (typeof this.props.setProps === 'function') {
                this.props.setProps({
                    mouseoverNodeData: event.target.data()
                })
            }
        });

        cy.on('mouseover', 'edge', event => {
            if (typeof this.props.setProps === 'function') {
                this.props.setProps({
                    mouseoverEdgeData: event.target.data()
                })
            }
        });

        cy.on('select', 'node', event => {
            const ele = event.target;

            selectedNodes.merge(ele);
            sendSelectedNodesData();
        });

        cy.on('unselect remove', 'node', event => {
            const ele = event.target;

            selectedNodes.unmerge(ele);
            sendSelectedNodesData();
        });

        cy.on('select', 'edge', event => {
            const ele = event.target;

            selectedEdges.merge(ele);
            sendSelectedEdgesData();
        });

        cy.on('unselect remove', 'edge', event => {
            const ele = event.target;

            selectedEdges.unmerge(ele);
            sendSelectedEdgesData();
        });

        cy.on('add remove', () => {
            refreshLayout();
        });

        this.cyResponsiveClass = new CyResponsive(cy);
        this.cyResponsiveClass.toggle(this.props.responsive);
    }
    
    handleImageGeneration(imageType, imageOptions, actionsToPerform, fileName) {

        let options = {}
        if (imageOptions){
            options = imageOptions
        }
        
        let desiredOutput = options.output
        options.output = 'blob'
        
        let downloadImage;
        let storeImage;
        switch (actionsToPerform) {
            case 'store':
                downloadImage = false
                storeImage = true
                break
            case 'download':
                downloadImage = true
                storeImage = false
                break
            case 'both':
                downloadImage = true
                storeImage = true
                break
            default:
                downloadImage = false
                storeImage = true
                break
        }
        
        let output;
        if (imageType === 'png') {
            output = this._cy.png(options)
        }
        if (imageType === 'jpg' || imageType === 'jpeg') {
            output = this._cy.jpg(options)
        }
        // only works when svg is imported (see lib/extra_index.js)
        if (imageType === 'svg') {
            output = this._cy.svg(options) 
        }
        
        /*
         * If output is empty because of bad options or a cytoscape error,
         * skip any download or storage steps.
         */
        if (output && downloadImage) {
            /*
             * Downloading is initiated client-side because the image is generated at
             * the client. This avoids transferring a potentially large image
             * to the server and back again through a callback.
             */
            let fName = fileName
            if (!fileName) {
                fName = 'cyto'
            }

            if (imageType !== 'svg') {
                this.downloadBlob(output, fName + '.' + imageType)
            }
            else {
                const blob = new Blob([output], {type:"image/svg+xml;charset=utf-8"});
                this.downloadBlob(blob, fName + '.' + imageType) 
            }
        }
        

        if (output && storeImage) {
            // Default output type if unspecified 
            if (!desiredOutput) {
                desiredOutput = 'base64uri'
            }
            
            if (!(desiredOutput === 'base64uri' || desiredOutput === 'base64')) {
                return
            }
            
            /*
             * Convert blob to base64uri or base64 string to store the image data.
             * Thank you, base64guru https://base64.guru/developers/javascript/examples/encode-blob
             */
            const reader = new FileReader()
            reader.onload = () => {
                /* FileReader is asynchronous, so the read function is non-blocking.
                 * If this code block is placed after the read command, it
                 * may result in empty output because the blob has not been loaded yet.
                 */
                let callbackData = reader.result
                if (desiredOutput === 'base64') {
                    callbackData = callbackData.replace(/^data:.+;base64,/, '')
                }
                this.props.setProps({'imageData': callbackData})
            }
            reader.readAsDataURL(output);
        }
    }
    
    downloadBlob(blob, fileName) {
        /*
         * Download blob as file by dynamically creating link.
         * Chrome does not open data URLs when JS opens a new tab directed
         * at the data URL, so this is an alternate implementation
         * that doesn't require extra packages. It may not behave in
         * exactly the same way across browsers (might display image in new tab
         * intead of downloading as a file).
         * Thank you, koldev https://jsfiddle.net/koldev/cW7W5/
         */
        const downloadLink = document.createElement("a")
        downloadLink.style = "display: none"
        document.body.appendChild(downloadLink)
        
        const url = window.URL.createObjectURL(blob)
        downloadLink.href = url
        downloadLink.download = fileName
        downloadLink.click()
        window.URL.revokeObjectURL(url)
        
        document.body.removeChild(downloadLink)
    }

    render() {
        const {
            // HTML attribute props
            id,
            style,
            className,
            // Common props
            elements,
            stylesheet,
            layout,
            // Viewport Manipulation
            pan,
            zoom,
            // Viewport Mutability and gesture Toggling
            panningEnabled,
            userPanningEnabled,
            minZoom,
            maxZoom,
            zoomingEnabled,
            userZoomingEnabled,
            boxSelectionEnabled,
            autoungrabify,
            autolock,
            autounselectify,
            // Image handling
            generateImage,
            // Responsive graphs
            responsive
        } = this.props;
        
        if (Object.keys(generateImage).length > 0) {
            // If no cytoscape object has been created yet, an image cannot be generated,
            // so generateImage will be ignored and cleared.
            this.props.setProps({'generateImage': {}})
            if (this._cy) {
                this.handleImageGeneration(
                    generateImage.type,
                    generateImage.options,
                    generateImage.action,
                    generateImage.filename
                )
            }
        }

        if (this.cyResponsiveClass) {
            this.cyResponsiveClass.toggle(responsive);
        }

        return (
            <CytoscapeComponent
                id={id}
                cy={this.handleCy}
                className={className}
                style={style}
                elements={CytoscapeComponent.normalizeElements(elements)}
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
    // HTML attribute props

    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Sets the class name of the element (the value of an element's html
     * class attribute).
     */
    className: PropTypes.string,

    /**
     * Add inline styles to the root element.
     */
    style: PropTypes.object,

    // Dash specific props

    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change.
     */
    setProps: PropTypes.func,

    // Common props

    /**
     * A list of dictionaries representing the elements of the networks.
     *     1. Each dictionary describes an element, and specifies its purpose.
     *         - `group` (string): Either 'nodes' or 'edges'. If not given, it's automatically inferred.
     *         - `data` (dictionary): Element specific data.
     *              - `id` (string): Reference to the element, useful for selectors and edges. Randomly assigned if not given.
     *              - `label` (string): Optional name for the element, useful when `data(label)` is given to a style's `content` or `label`. It is only a convention.
     *              - `parent` (string): Only for nodes. Optional reference to another node. Needed to create compound nodes.
     *              - `source` (string): Only for edges. The id of the source node, which is where the edge starts.
     *              - `target` (string): Only for edges. The id of the target node, where the edge ends.
     *         - `position` (dictionary): Only for nodes. The position of the node.
     *              - `x` (number): The x-coordinate of the node.
     *              - `y` (number): The y-coordinate of the node.
     *         - `selected` (boolean): If the element is selected upon initialisation.
     *         - `selectable` (boolean): If the element can be selected.
     *         - `locked` (boolean): Only for nodes. If the position is immutable.
     *         - `grabbable` (boolean): Only for nodes. If the node can be grabbed and moved by the user.
     *         - `classes` (string): Space separated string of class names of the element. Those classes can be selected by a style selector.
     *
     *     2. The [official Cytoscape.js documentation](http://js.cytoscape.org/#notation/elements-json) offers an extensive overview and examples of element declaration.
     * Alternatively, a dictionary with the format { 'nodes': [], 'edges': [] } is allowed at initialization, but arrays remain the recommended format.
     */
    elements: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.object), PropTypes.object]),

    /**
     * A list of dictionaries representing the styles of the elements.
     *     1. Each dictionary requires the following keys:
     *         - `selector` (string): Which elements you are styling. Generally, you select a group of elements (node, edges, both), a class (that you declare in the element dictionary), or an element by ID.
     *         - `style` (dictionary): What aspects of the elements you want to modify. This could be the size or color of a node, the shape of an edge arrow, or many more.
     *
     *     2. Both [the selector string](http://js.cytoscape.org/#selectors) and
     *     [the style dictionary](http://js.cytoscape.org/#style/node-body) are
     *     exhaustively documented in the Cytoscape.js docs. Although methods such
     *     as `cy.elements(...)` and `cy.filter(...)` are not available, the selector
     *     string syntax stays the same.
     */
    stylesheet: PropTypes.arrayOf(PropTypes.object),

    /**
     * A dictionary specifying how to set the position of the elements in your
     * graph. The `'name'` key is required, and indicates which layout (algorithm) to
     * use.
     *     1. The layouts available by default are:
     *         - `random`: Randomly assigns positions
     *         - `preset`: Assigns position based on the `position` key in element dictionaries
     *         - `circle`: Single-level circle, with optional radius
     *         - `concentric`: Multi-level circle, with optional radius
     *         - `grid`: Square grid, optionally with numbers of `rows` and `cols`
     *         - `breadthfirst`: Tree structure built using BFS, with optional `roots`
     *         - `cose`: Force-directed physics simulation
     *
     *     2. Some external layouts are also included. To use them, run
     *     `dash_cytoscape.load_extra_layouts()` before creating your Dash app. Be careful about
     *     using the extra layouts when not necessary, since they require supplementary bandwidth
     *     for loading, which impacts the startup time of the app.
     *         - `cose-bilkent`: https://github.com/cytoscape/cytoscape.js-cose-bilkent
     *         - `cola`: https://github.com/cytoscape/cytoscape.js-cola
     *         - `euler`: https://github.com/cytoscape/cytoscape.js-dagre
     *         - `spread`: https://github.com/cytoscape/cytoscape.js-spread
     *         - `dagre`: https://github.com/cytoscape/cytoscape.js-dagre
     *         - `klay`: https://github.com/cytoscape/cytoscape.js-klay
     *
     *     3. The keys accepted by `layout` vary depending on the algorithm, but some
     *     keys are accepted by all layouts:
     *         - `fit` (boolean): Whether to render the nodes in order to fit the canvas.
     *         - `padding` (number): Padding around the sides of the canvas, if fit is enabled.
     *         - `animate` (boolean): Whether to animate change in position when the layout changes.
     *         - `animationDuration` (number): Duration of animation in milliseconds, if enabled.
     *         - `boundingBox` (dictionary): How to constrain the layout in a specific area. Keys accepted are either `x1, y1, x2, y2` or `x1, y1, w, h`, all of which receive a pixel value.
     *
     *     4. The complete list of layouts and their accepted options are available
     *     on the [Cytoscape.js docs](http://js.cytoscape.org/#layouts). For the
     *     external layouts, the options are listed in the "API" section of the
     *     README.
     *     Note that certain keys are not supported in Dash since the value is a
     *     JavaScript function or a callback. Please visit [this issue](https://github.com/plotly/dash-cytoscape/issues/25)
     *     for more information.
     */
    layout: PropTypes.object,

    // Viewport Manipulation

    /**
     * Dictionary indicating the initial panning position of the graph. The
     * following keys are accepted:
     *     - `x` (number): The x-coordinate of the position.
     *     - `y` (number): The y-coordinate of the position.
     */
    pan: PropTypes.object,

    /**
     * The initial zoom level of the graph. You can set `minZoom` and
     * `maxZoom` to set restrictions on the zoom level.
     */
    zoom: PropTypes.number,

    // Viewport Mutability and gesture Toggling
    /**
     * Whether panning the graph is enabled (i.e., the position of the graph is
     * mutable overall).
     */
    panningEnabled: PropTypes.bool,

    /**
     * Whether user events (e.g. dragging the graph background) are allowed to
     * pan the graph.
     */
    userPanningEnabled: PropTypes.bool,

    /**
     * A minimum bound on the zoom level of the graph. The viewport can not be
     * scaled smaller than this zoom level.
     */
    minZoom: PropTypes.number,

    /**
     * A maximum bound on the zoom level of the graph. The viewport can not be
     * scaled larger than this zoom level.
     */
    maxZoom: PropTypes.number,

    /**
     * Whether zooming the graph is enabled (i.e., the zoom level of the graph
     * is mutable overall).
     */
    zoomingEnabled: PropTypes.bool,

    /**
     * Whether user events (e.g. dragging the graph background) are allowed
     * to pan the graph.
     */
    userZoomingEnabled: PropTypes.bool,

    /**
     * Whether box selection (i.e. drag a box overlay around, and release it
     * to select) is enabled. If enabled, the user must taphold to pan the graph.
     */
    boxSelectionEnabled: PropTypes.bool,

    /**
     * Whether nodes should be ungrabified (not grabbable by user) by
     * default (if true, overrides individual node state).
     */
    autoungrabify: PropTypes.bool,

    /**
     * Whether nodes should be locked (not draggable at all) by default
     * (if true, overrides individual node state).
     */
    autolock: PropTypes.bool,

    /**
     * Whether nodes should be unselectified (immutable selection state) by
     * default (if true, overrides individual element state).
     */
    autounselectify: PropTypes.bool,

    /**
     * Whether the layout should be refreshed when elements are added or removed.
     */
    autoRefreshLayout: PropTypes.bool,

    // User Events Props

    /**
     * The complete node dictionary returned when you tap or click it. Read-only.
     *
     *     1. Node-specific items:
     *         - `edgesData` (dictionary)
     *         - `renderedPosition` (dictionary)
     *         - `timeStamp` (number)
     *
     *     2. General items (for all elements):
     *         - `classes` (string)
     *         - `data` (dictionary)
     *         - `grabbable` (boolean)
     *         - `group` (string)
     *         - `locked` (boolean)
     *         - `position` (dictionary)
     *         - `selectable` (boolean)
     *         - `selected` (boolean)
     *         - `style` (dictionary)
     *
     *     3. Items for compound nodes:
     *         - `ancestorsData` (dictionary)
     *         - `childrenData` (dictionary)
     *         - `descendantsData` (dictionary)
     *         - `parentData` (dictionary)
     *         - `siblingsData` (dictionary)
     *         - `isParent` (boolean)
     *         - `isChildless` (boolean)
     *         - `isChild` (boolean)
     *         - `isOrphan` (boolean)
     *         - `relativePosition` (dictionary)
     */
    tapNode: PropTypes.object,

    /**
     * The data dictionary of a node returned when you tap or click it. Read-only.
     */
    tapNodeData: PropTypes.object,

    /**
     * The complete edge dictionary returned when you tap or click it. Read-only.
     *
     *     1. Edge-specific items:
     *         - `isLoop` (boolean)
     *         - `isSimple` (boolean)
     *         - `midpoint` (dictionary)
     *         - `sourceData` (dictionary)
     *         - `sourceEndpoint` (dictionary)
     *         - `targetData` (dictionary)
     *         - `targetEndpoint` (dictionary)
     *         - `timeStamp` (number)
     *
     *     2. General items (for all elements):
     *         - `classes` (string)
     *         - `data` (dictionary)
     *         - `grabbable` (boolean)
     *         - `group` (string)
     *         - `locked` (boolean)
     *         - `selectable` (boolean)
     *         - `selected` (boolean)
     *         - `style` (dictionary)
     */
    tapEdge: PropTypes.object,

    /**
     * The data dictionary of an edge returned when you tap or click it. Read-only.
     */
    tapEdgeData: PropTypes.object,

    /**
     * The data dictionary of a node returned when you hover over it. Read-only.
     */
    mouseoverNodeData: PropTypes.object,

    /**
     * The data dictionary of an edge returned when you hover over it. Read-only.
     */
    mouseoverEdgeData: PropTypes.object,

    /**
     * The list of data dictionaries of all selected nodes (e.g. using
     * Shift+Click to select multiple nodes, or Shift+Drag to use box selection). Read-only.
     */
    selectedNodeData: PropTypes.array,

    /**
     * The list of data dictionaries of all selected edges (e.g. using
     * Shift+Click to select multiple nodes, or Shift+Drag to use box selection). Read-only.
     */
    selectedEdgeData: PropTypes.array,
    
    /**
     * Dictionary specifying options to generate an image of the current cytoscape graph.
     * Value is cleared after data is received and image is generated. This property will
     * be ignored on the initial creation of the cytoscape object and must be invoked through
     * a callback after it has been rendered. The `'type'` key is required.
     * The following keys are supported:
     *      - `type` (string): File type to ouput of 'svg, 'png', 'jpg', or 'jpeg' (alias of 'jpg')
     *      - `options` (dictionary, optional): Dictionary of options to cy.png() / cy.jpg() or cy.svg() for
     *          image generation. See http://js.cytoscape.org/#core/export for details.
     *          For `'output'`, only 'base64' and 'base64uri' are supported.
     *          Default: `{'output': 'base64uri'}`.
     *      - `action` (string, optional): Default: `'store'`. Must be one of the following:
     *          - `'store'`: Stores the image data (only jpg and png are supported) in `imageData` and invokes
     *              server-side Dash callbacks.
     *          - `'download'`: Downloads the image as a file with all data handling
     *              done client-side. No `imageData` callbacks are fired.
     *          - `'both'`: Stores image data and downloads image as file.
     *      - `filename` (string, optional): Name for the file to be downloaded. Default: 'cyto'.
     *
     * If the app does not need the image data server side and/or it will only be used to download
     * the image, it may be prudent to invoke `'download'` for `action` instead of
     * `'store'` to improve performance by preventing transfer of data to the server.
     */
    generateImage: PropTypes.object,
    
    /**
     * String representation of the image requested with generateImage. Null if no
     * image was requested yet or the previous request failed. Read-only.
     */
    imageData: PropTypes.string,

    /**
     * Toggles intelligent responsive resize of Cytoscape graph with viewport size change
     */
    responsive: PropTypes.bool
};

Cytoscape.defaultProps = {
    style: {width: '600px', height: '600px'},
    layout: {name: 'grid'},
    pan: {x: 0, y: 0},
    zoom: 1,
    minZoom: 1e-50,
    maxZoom: 1e50,
    zoomingEnabled: true,
    userZoomingEnabled: true,
    panningEnabled: true,
    userPanningEnabled: true,
    boxSelectionEnabled: false,
    autolock: false,
    autoungrabify: false,
    autounselectify: false,
    autoRefreshLayout: true,
    generateImage: {},
    imageData: null,
    responsive: false,
    elements: []
};

export default Cytoscape;
