/**
 * JavaScript Requirements: cytoscape
 * React.js requirements: react-cytoscapejs
 */
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import CytoscapeComponent from 'react-cytoscapejs';
import _ from 'lodash';



function objectSubsectionMatch(obj, matchObj) {
    return !Object.keys(matchObj).some(matchKey =>
        typeof matchObj[matchKey] === 'object'
            ? !objectSubsectionMatch(obj[matchKey], matchObj[matchKey])
            : obj[matchKey] !== matchObj[matchKey]
    );
}

function ctxmenuTransformJson(data, shape) {
    // if shape is empty then just return data
    if(typeof shape !== 'object') {
        return data;
    }

    return shape.map(matchItem =>
            typeof matchItem === 'object' ? matchItem : {key: matchItem}
        )
        .reduce((acc, property) => {
            const {key, props, filter} = property;

            if(data[key] === undefined) {
                // do nothing
            }
            if(typeof property.props === 'object') {
                if(data[key].constructor === Array) {
                    acc[key] = data[key].map(arrItem => {
                        if(typeof filter === 'object') {
                            if(objectSubsectionMatch(arrItem, filter)) {
                                return ctxmenuTransformJson(arrItem, props);
                            }
                        }
                        else {
                            return ctxmenuTransformJson(arrItem, props);
                        }
                    })
                        .filter(arrItem =>
                            arrItem !== undefined
                        );
                }
                else {
                    acc[key] = ctxmenuTransformJson(data[key], props);
                }
            }
            else {
                acc[property.key] = data[property.key];
            }

            return acc;
        }, {});
}



/**
A Component Library for Dash aimed at facilitating network visualization in
Python, wrapped around [Cytoscape.js](http://js.cytoscape.org/).
 */
class Cytoscape extends Component {
    constructor(props) {
        super(props);

        this.handleCy = this.handleCy.bind(this);
        this.ctxmenuTranformProps = this.ctxmenuTranformProps.bind(this);
        this.ctxmenuUpdate = this.ctxmenuUpdate.bind(this);

        this._ctxmenuHashtable = {};
        this._handleCyCalled = false;
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
                cy.layout(layout).run()
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

        this.ctxmenuUpdate();
    }

    ctxmenuUpdate() {
        const {ctxmenu} = this.props;

        if(typeof ctxmenu !== 'object' || ctxmenu.length === 0 || !this._cy || !this._cy.cxtmenu) {
            return;
        }

        // take all ctxmenu objects from props and hash them
        // compare props hash to hash list to find new hashes
        let ctxmenuNew = [];
        let ctxmenuHashCurrent = {};
        ctxmenu.map(ctxmenuObj => {
            let ctxmenuHash = JSON.stringify(ctxmenuObj);

            if(!this._ctxmenuHashtable[ctxmenuHash]) {
                ctxmenuNew.push(ctxmenuHash);
            }

            ctxmenuHashCurrent[ctxmenuHash] = true;
        });

        // delete removed ctxmenus
        Object.keys(this._ctxmenuHashtable).map(ctxmenuHash => {
            if(!ctxmenuHashCurrent[ctxmenuHash]) {
                this._ctxmenuHashtable[ctxmenuHash].destroy();
                delete this._ctxmenuHashtable[ctxmenuHash];
            }
        });

        // initialize new ctxmenus and add object from cy to ctxmenu hash table
        ctxmenuNew.map(ctxmenuHash => {
            this._ctxmenuHashtable[ctxmenuHash] = this._cy.cxtmenu(
                this.ctxmenuTranformProps(ctxmenuHash)
            );
        });
    }

    ctxmenuTranformProps(ctxmenuStr) {
        let ctxmenu = JSON.parse(ctxmenuStr);

        for(let i = 0; i < ctxmenu.commands.length; i++) {
            ctxmenu.commands[i].select = ele => {
                if(typeof this.props.setProps === 'function') {
                    this.props.setProps({
                        ctxmenuData: {
                            id: ctxmenu.commands[i].id,
                            data: ctxmenuTransformJson(ele.json(), ctxmenu.commands[i].format),
                            timestamp: Date.now()
                        }
                    });
                }
            }
        }

        return ctxmenu;
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
            autounselectify
        } = this.props;

        this.ctxmenuUpdate();

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
     */
    elements: PropTypes.arrayOf(PropTypes.object),

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
     * Property that determines whether a context menu is displayed and how. Requires extra layouts loaded.
     * Context menu is accessed by right clicking or holding down left click on an element with context menu
     * applied. It accepts a list of dictionaries, each of which describe a specific ctxmenu.
     * See ctxmenu documentation on github to find more information.
     *
     * 1. Each dictionary describes the ctxmenu which is applied to one selector.
     *     - `selector` (string): Elements matching this Cytoscape.js selector will trigger cxtmenus.
     *     - `commands` (dictionary): An array of commands to list in the menu or a function that returns the array.
     *         - `id` (string): Id that is returned in the ctxmenu callback to identify specific command triggered. Required.
     *         - `content` (string): HTML/text content to be displayed in the menu. Required.
     *         - `contentStyle` (dictionary): CSS key:value pairs to set the command's css in js if you want.
     *         - `enabled` (bool): Whether the command is selectable.
     *         - `format` (array): Data structure which determines how raw information from cytoscape's json function is filtered
     *     - `menuRadius` (number): The radius of the circular menu in pixels.
     *     - `fillColor` (string): The background colour of the menu.
     *     - `activeFillColor` (string): The colour used to indicate the selected command.
     *     - `activePadding` (number): Additional size in pixels for the active command.
     *     - `indicatorSize` (number): The size in pixels of the pointer to the active command.
     *     - `separatorWidth` (number): Elements matching this Cytoscape.js selector will trigger cxtmenus.
     *     - `spotlightPadding` (number): Extra spacing in pixels between the element and the spotlight.
     *     - `minSpotlightRadius` (number): The minimum radius in pixels of the spotlight.
     *     - `maxSpotlightRadius` (number): The maximum radius in pixels of the spotlight.
     *     - `openMenuEvents` (string): Space-separated cytoscape events that will open the menu; only `cxttapstart` and/or `taphold` work here.
     *     - `itemColor` (string): The colour of text in the command's content.
     *     - `itemTextShadowColor` (string): The text shadow colour of the command's content.
     *     - `zIndex` (number): The z-index of the ui div.
     *     - `atMouse` (bool): Draw menu at mouse position.
     *
     * 2. The format array inside the `commands` dictionary which determines how information is passed back.
     * In the format array, strings can be entered to determine which properties of the cytoscape json object are selected.
     * Alternatively, instead of a string, a dictionary can be used to select properties more specifically. The properties of such an object are outlined below:
     *     - `key` (string): Specifies the property to be selected in the json object.
     *     - `props` (array): This array specifies the properties of the key which are selected.
     *     - `filter` (dictionary): This property is only to be applied where the value of the `key` is an array of objects. This object specifies the properties and values that the object in the array must have to not be removed from the array.
     * For an example of the capabilities of this system, please reference the ctxmenu demo.
     */
    ctxmenu: PropTypes.arrayOf(
        PropTypes.shape({
            selector: PropTypes.string,
            commands: PropTypes.arrayOf(
                PropTypes.shape({
                    id: PropTypes.string.isRequired,
                    content: PropTypes.string.isRequired,
                    contentStyle: PropTypes.object,
                    fillColor: PropTypes.string,
                    enabled: PropTypes.bool,
                    format: PropTypes.array
                })
            ),
            menuRadius: PropTypes.number,
            fillColor: PropTypes.string,
            activeFillColor: PropTypes.string,
            activePadding: PropTypes.number,
            indicatorSize: PropTypes.number,
            separatorWidth: PropTypes.number,
            spotlightPadding: PropTypes.number,
            minSpotlightRadius: PropTypes.number,
            maxSpotlightRadius: PropTypes.number,
            openMenuEvents: PropTypes.string,
            itemColor: PropTypes.string,
            itemTextShadowColor: PropTypes.string,
            zIndex: PropTypes.number,
            atMouse: PropTypes.bool
        })
    ),

    /**
     * The dictionary returned when a ctxmenu option is selected. Read-only.
     *
     *     1. The structure of the dictionary is as follows:
     *         - `id` (string): User supplied string meant to identify the specific ctxmenu option triggered
     *         - `timestamp` (number): Millisecond UNIX timestamp indicating the time the ctxmenu option was selected
     *         - `data` (dictionary): Data dump containing information on element ctxmenu is triggered on. This data is fetched by cytoscape json function.
     */
    ctxmenuData: PropTypes.object
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
    autoRefreshLayout: true
};

export default Cytoscape;