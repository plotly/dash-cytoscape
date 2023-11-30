/**
 * JavaScript Requirements: cytoscape, cytoscape-svg
 * React.js requirements: react-cytoscapejs
 */
import '/src/assets/contextmenu.css';
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import CytoscapeComponent from 'react-cytoscapejs';
import _ from 'lodash';
import {v4 as uuidv4} from 'uuid';
import CyResponsive from '../cyResponsive.js';

// Polyfill so that context menu extension works in Safari
import '@ungap/custom-elements';

const cytoscape = require('cytoscape');
const contextMenus = require('cytoscape-context-menus');

// register extension
contextMenus(cytoscape);
/**
 * A Component Library for Dash aimed at facilitating network visualization in
 * Python, wrapped around [Cytoscape.js](http://js.cytoscape.org/).
 */
class Cytoscape extends Component {
    constructor(props) {
        super(props);

        this.handleCy = this.handleCy.bind(this);
        this._handleCyCalled = false;
        this.handleImageGeneration = this.handleImageGeneration.bind(this);
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
        const edgesData = ele.connectedEdges().map((ele) => {
            return ele.data();
        });
        const childrenData = ele.children().map((ele) => {
            return ele.data();
        });
        const ancestorsData = ele.ancestors().map((ele) => {
            return ele.data();
        });
        const descendantsData = ele.descendants().map((ele) => {
            return ele.data();
        });
        const siblingsData = ele.siblings().map((ele) => {
            return ele.data();
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
            selectable,
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
            style,
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
        const {classes, data, grabbable, group, locked, selectable, selected} =
            ele.json();

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
            style,
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
            const {autoRefreshLayout, layout} = this.props;

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
            const nodeData = selectedNodes.map((el) => el.data());

            this.props.setProps({
                selectedNodeData: nodeData,
            });
        }, SELECT_THRESHOLD);

        const sendSelectedEdgesData = _.debounce(() => {
            const edgeData = selectedEdges.map((el) => el.data());

            this.props.setProps({
                selectedEdgeData: edgeData,
            });
        }, SELECT_THRESHOLD);

        // /////////////////////////////////////// EVENTS //////////////////////////////////////////

        cy.on('tap', 'node', (event) => {
            const nodeObject = this.generateNode(event);

            this.props.setProps({
                tapNode: nodeObject,
                tapNodeData: Object.assign({}, nodeObject.data, {
                    timeStamp: nodeObject.timeStamp,
                }),
            });
        });

        cy.on('tap', 'edge', (event) => {
            const edgeObject = this.generateEdge(event);

            this.props.setProps({
                tapEdge: edgeObject,
                tapEdgeData: Object.assign({}, edgeObject.data, {
                    timeStamp: edgeObject.timeStamp,
                }),
            });
        });

        cy.on('mouseover', 'node', (event) => {
            this.props.setProps({
                mouseoverNodeData: Object.assign({}, event.target.data(), {
                    timeStamp: event.timeStamp,
                }),
            });
        });

        cy.on('mouseover', 'edge', (event) => {
            this.props.setProps({
                mouseoverEdgeData: Object.assign({}, event.target.data(), {
                    timeStamp: event.timeStamp,
                }),
            });
        });

        cy.on('mouseout', 'node', (_) => {
            if (this.props.clearOnUnhover === true) {
                this.props.setProps({mouseoverNodeData: null});
            }
        });

        cy.on('mouseout', 'edge', (_) => {
            if (this.props.clearOnUnhover === true) {
                this.props.setProps({
                    mouseoverEdgeData: null,
                });
            }
        });

        cy.on('select', 'node', (event) => {
            const ele = event.target;

            selectedNodes.merge(ele);
            sendSelectedNodesData();
        });

        cy.on('unselect remove', 'node', (event) => {
            const ele = event.target;

            selectedNodes.unmerge(ele);
            sendSelectedNodesData();
        });

        cy.on('select', 'edge', (event) => {
            const ele = event.target;

            selectedEdges.merge(ele);
            sendSelectedEdgesData();
        });

        cy.on('unselect remove', 'edge', (event) => {
            const ele = event.target;

            selectedEdges.unmerge(ele);
            sendSelectedEdgesData();
        });

        cy.on('add remove', () => {
            refreshLayout();
        });

        cy.on('dragfree add remove', (_) => {
            this.props.setProps({
                elements: cy.elements('').map((item) => {
                    if (item.json().group === 'nodes') {
                        return {
                            data: item.json().data,
                            position: item.json().position,
                        };
                    }
                    return {
                        data: item.json().data,
                        position: void 0,
                    };
                }),
            });
        });

        this.createMenuItems = (ctxMenu) => {
            const updateContextMenuData = (newContext) => {
                this.props.setProps({contextMenuData: newContext});
            };
            const contextMenuDefaultFunctions = {
                remove: function (event) {
                    const target = event.target || event.cyTarget;
                    target.remove();
                },
                add_node: function (event) {
                    const pos = event.position || event.cyPosition;
                    cy.add({
                        data: {
                            group: 'nodes',
                        },
                        position: {
                            x: pos.x,
                            y: pos.y,
                        },
                    });
                },
                add_edge: function () {
                    const selectedNodeIds = selectedNodes.map((node) =>
                        node.id()
                    );
                    if (selectedNodes.length === 0) {
                        console.error(
                            'Error: No nodes selected, cannot add edge'
                        );
                    } else if (selectedNodes.length === 1) {
                        cy.add({
                            data: {
                                id: uuidv4(),
                                group: 'edges',
                                source: selectedNodeIds[0],
                                target: selectedNodeIds[0],
                            },
                        });
                    } else if (selectedNodes.length === 2) {
                        cy.add({
                            data: {
                                id: uuidv4(),
                                group: 'edges',
                                source: selectedNodeIds[0],
                                target: selectedNodeIds[1],
                            },
                        });
                    } else {
                        console.error(
                            'Error: more than 2 nodes selected, cannot add edge'
                        );
                    }
                },
            };
            const newMenuItems = [];
            for (const item of ctxMenu) {
                let onClickFunction;
                // return data so a user can define a custom on click function in Python
                // if onClick or on onClickCustom are not specified
                onClickFunction = function (event) {
                    updateContextMenuData({
                        menuItemId: item.id,
                        x: event.position.x,
                        y: event.position.y,
                        timeStamp: event.timeStamp,
                        elementId: event.target.data().id,
                        edgeSource: event.target.data().source,
                        edgeTarget: event.target.data().target,
                    });
                };
                // use default javascript function as onClickFunction
                if (Object.prototype.hasOwnProperty.call(item, 'onClick')) {
                    if (
                        Object.prototype.hasOwnProperty.call(
                            contextMenuDefaultFunctions,
                            item.onClick
                        )
                    ) {
                        onClickFunction =
                            contextMenuDefaultFunctions[item.onClick];
                    } else {
                        console.error(
                            `onClick function ${item.onClick} is not defined`
                        );
                    }
                }
                // use user-defined Javascript function in a namespace under assets/ as onClickFunction
                else if (
                    Object.prototype.hasOwnProperty.call(item, 'onClickCustom')
                ) {
                    if (
                        Object.prototype.hasOwnProperty.call(
                            window,
                            'dashCytoscapeFunctions'
                        ) &&
                        Object.prototype.hasOwnProperty.call(
                            window.dashCytoscapeFunctions,
                            item.onClickCustom
                        )
                    ) {
                        onClickFunction =
                            window.dashCytoscapeFunctions[item.onClickCustom];
                    } else {
                        console.error(
                            `onClickCustom function ${item.onClickCustom} is not defined`
                        );
                    }
                }
                const new_item = {
                    id: item.id,
                    content: item.label,
                    tooltipText: item.tooltipText,
                    selector: '',
                    onClickFunction: onClickFunction,
                    coreAsWell: false,
                };
                if (Object.prototype.hasOwnProperty.call(item, 'availableOn')) {
                    for (const selector of item.availableOn) {
                        if (selector === 'edge') {
                            if (new_item.selector.length > 0) {
                                new_item.selector = new_item.selector + ', ';
                            }
                            new_item.selector = new_item.selector + 'edge';
                        } else if (selector === 'node') {
                            if (new_item.selector.length > 0) {
                                new_item.selector = new_item.selector + ', ';
                            }
                            new_item.selector = new_item.selector + 'node';
                        } else if (selector === 'canvas') {
                            new_item.coreAsWell = true;
                        } else {
                            console.error(
                                `Error: selector ${selector} is not available. Choose one of 'node', 'edge' or 'canvas'.`
                            );
                        }
                    }
                }
                newMenuItems.push(new_item);
            }
            return newMenuItems;
        };

        this.cyResponsiveClass = new CyResponsive(cy);
        this.cyResponsiveClass.toggle(this.props.responsive);
    }

    handleImageGeneration(imageType, imageOptions, actionsToPerform, fileName) {
        let options = {};
        if (imageOptions) {
            options = imageOptions;
        }

        let desiredOutput = options.output;
        options.output = 'blob';

        let downloadImage;
        let storeImage;
        switch (actionsToPerform) {
            case 'store':
                downloadImage = false;
                storeImage = true;
                break;
            case 'download':
                downloadImage = true;
                storeImage = false;
                break;
            case 'both':
                downloadImage = true;
                storeImage = true;
                break;
            default:
                downloadImage = false;
                storeImage = true;
                break;
        }

        let output;
        if (imageType === 'png') {
            output = this._cy.png(options);
        }
        if (imageType === 'jpg' || imageType === 'jpeg') {
            output = this._cy.jpg(options);
        }
        // only works when svg is imported (see lib/extra_index.js)
        if (imageType === 'svg') {
            output = this._cy.svg(options);
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
            let fName = fileName;
            if (!fileName) {
                fName = 'cyto';
            }

            if (imageType !== 'svg') {
                this.downloadBlob(output, fName + '.' + imageType);
            } else {
                const blob = new Blob([output], {
                    type: 'image/svg+xml;charset=utf-8',
                });
                this.downloadBlob(blob, fName + '.' + imageType);
            }
        }

        if (output && storeImage) {
            // Default output type if unspecified
            if (!desiredOutput) {
                desiredOutput = 'base64uri';
            }

            if (
                !(desiredOutput === 'base64uri' || desiredOutput === 'base64')
            ) {
                return;
            }

            /*
             * Convert blob to base64uri or base64 string to store the image data.
             * Thank you, base64guru https://base64.guru/developers/javascript/examples/encode-blob
             */
            const reader = new FileReader();
            reader.onload = () => {
                /* FileReader is asynchronous, so the read function is non-blocking.
                 * If this code block is placed after the read command, it
                 * may result in empty output because the blob has not been loaded yet.
                 */
                let callbackData = reader.result;
                if (desiredOutput === 'base64') {
                    callbackData = callbackData.replace(/^data:.+;base64,/, '');
                }
                this.props.setProps({imageData: callbackData});
            };
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
        const downloadLink = document.createElement('a');
        downloadLink.style = 'display: none';
        document.body.appendChild(downloadLink);

        const url = window.URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = fileName;
        downloadLink.click();
        window.URL.revokeObjectURL(url);

        document.body.removeChild(downloadLink);
    }

    updateContextMenu(contextMenu) {
        this._cy.contextMenus({
            menuItems: this.createMenuItems(contextMenu),
            menuItemClasses: ['custom-menu-item'],
        });
    }
    componentDidUpdate(prevProps) {
        const {contextMenu} = this.props;
        if (!_.isEqual(prevProps.contextMenu, contextMenu) && this._cy) {
            this.updateContextMenu(contextMenu);
        }
    }
    componentDidMount() {
        const {contextMenu} = this.props;
        if (this._cy && contextMenu.length > 0) {
            this.updateContextMenu(contextMenu);
        }
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
            contextMenu,
            contextMenuData,
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
            responsive,
        } = this.props;

        if (Object.keys(generateImage).length > 0) {
            // If no cytoscape object has been created yet, an image cannot be generated,
            // so generateImage will be ignored and cleared.
            this.props.setProps({generateImage: {}});
            if (this._cy) {
                this.handleImageGeneration(
                    generateImage.type,
                    generateImage.options,
                    generateImage.action,
                    generateImage.filename
                );
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
                contextMenu={contextMenu}
                contextMenuData={contextMenuData}
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
        );
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
     * A list of dictionaries representing the elements of the networks. Each dictionary describes an element, and
     * specifies its purpose. The [official Cytoscape.js documentation](https://js.cytoscape.org/#notation/elements-json)
     * offers an extensive overview and examples of element declaration.
     * Alternatively, a dictionary with the format { 'nodes': [], 'edges': [] } is allowed at initialization,
     * but arrays remain the recommended format.
     */
    elements: PropTypes.oneOfType([
        PropTypes.arrayOf(
            PropTypes.shape({
                /**
                 * Either 'nodes' or 'edges'. If not given, it's automatically inferred.
                 */
                group: PropTypes.string,
                /** Element specific data.*/
                data: PropTypes.shape({
                    /**  Reference to the element, useful for selectors and edges. Randomly assigned if not given.*/
                    id: PropTypes.string,
                    /**
                     * Optional name for the element, useful when `data(label)` is given to a style's `content`
                     * or `label`. It is only a convention. */
                    label: PropTypes.string,
                    /** Only for nodes. Optional reference to another node. Needed to create compound nodes. */
                    parent: PropTypes.string,
                    /** Only for edges. The id of the source node, which is where the edge starts. */
                    source: PropTypes.string,
                    /** Only for edges. The id of the target node, where the edge ends. */
                    target: PropTypes.string,
                }),
                /** Only for nodes. The position of the node. */
                position: PropTypes.shape({
                    /** The x-coordinate of the node. */
                    x: PropTypes.number,
                    /** The y-coordinate of the node. */
                    y: PropTypes.number,
                }),
                /** If the element is selected upon initialisation. */
                selected: PropTypes.bool,
                /** If the element can be selected. */
                selectable: PropTypes.bool,
                /** Only for nodes. If the position is immutable. */
                locked: PropTypes.bool,
                /** Only for nodes. If the node can be grabbed and moved by the user. */
                grabbable: PropTypes.bool,
                /**
                 * Space separated string of class names of the element. Those classes can be selected
                 * by a style selector.
                 */
                classes: PropTypes.string,
            })
        ),
        PropTypes.exact({
            nodes: PropTypes.array,
            edges: PropTypes.array,
        }),
    ]),

    /**
     * A list of dictionaries representing the styles of the elements.
     * Each dictionary requires the following keys: `selector` and `style`.
     *
     * Both the [selector](https://js.cytoscape.org/#selectors) and
     * the [style](https://js.cytoscape.org/#style/node-body) are
     * exhaustively documented in the Cytoscape.js docs. Although methods such
     * as `cy.elements(...)` and `cy.filter(...)` are not available, the selector
     * string syntax stays the same.
     */
    stylesheet: PropTypes.arrayOf(
        PropTypes.exact({
            /**
             * Which elements you are styling. Generally, you select a group of elements (node, edges, both),
             * a class (that you declare in the element dictionary), or an element by ID.
             */
            selector: PropTypes.string.isRequired,
            /**
             * What aspects of the elements you want to modify. This could be the size or
             * color of a node, the shape of an edge arrow, or many more.
             */
            style: PropTypes.object.isRequired,
        })
    ),

    /**
     * A dictionary specifying how to set the position of the elements in your
     * graph. The `'name'` key is required, and indicates which layout (algorithm) to
     * use. The keys accepted by `layout` vary depending on the algorithm, but these
     * keys are accepted by all layouts: `fit`,  `padding`, `animate`, `animationDuration`,
     * `boundingBox`.
     *
     *  The complete list of layouts and their accepted options are available on the
     *  [Cytoscape.js docs](https://js.cytoscape.org/#layouts) . For the external layouts,
     * the options are listed in the "API" section of the  README.
     *  Note that certain keys are not supported in Dash since the value is a JavaScript
     *  function or a callback. Please visit this
     * [issue](https://github.com/plotly/dash-cytoscape/issues/25) for more information.
     */
    layout: PropTypes.shape({
        /**
         * The layouts available by default are:
         *   `random`: Randomly assigns positions.
         *   `preset`: Assigns position based on the `position` key in element dictionaries.
         *   `circle`: Single-level circle, with optional radius.
         *   `concentric`: Multi-level circle, with optional radius.
         *   `grid`: Square grid, optionally with numbers of `rows` and `cols`.
         *   `breadthfirst`: Tree structure built using BFS, with optional `roots`.
         *   `cose`: Force-directed physics simulation.
         *
         * Some external layouts are also included. To use them, run
         *   `dash_cytoscape.load_extra_layouts()` before creating your Dash app. Be careful about
         *   using the extra layouts when not necessary, since they require supplementary bandwidth
         *   for loading, which impacts the startup time of the app.
         *   The external layouts are:
         *   [cose-bilkent](https://github.com/cytoscape/cytoscape.js-cose-bilkent),
         *   [fcose](https://github.com/iVis-at-Bilkent/cytoscape.js-fcose),
         *   [cola](https://github.com/cytoscape/cytoscape.js-cola),
         *   [euler](https://github.com/cytoscape/cytoscape.js-dagre),
         *   [spread](https://github.com/cytoscape/cytoscape.js-spread),
         *   [dagre](https://github.com/cytoscape/cytoscape.js-dagre),
         *   [klay](https://github.com/cytoscape/cytoscape.js-klay),
         */
        name: PropTypes.oneOf([
            'random',
            'preset',
            'circle',
            'concentric',
            'grid',
            'breadthfirst',
            'cose',
            'cose-bilkent',
            'fcose',
            'cola',
            'euler',
            'spread',
            'dagre',
            'klay',
        ]).isRequired,
        /**  Whether to render the nodes in order to fit the canvas. */
        fit: PropTypes.bool,
        /** Padding around the sides of the canvas, if fit is enabled. */
        padding: PropTypes.number,
        /** Whether to animate change in position when the layout changes. */
        animate: PropTypes.bool,
        /** Duration of animation in milliseconds, if enabled. */
        animationDuration: PropTypes.number,
        /**
         * How to constrain the layout in a specific area. Keys accepted are either
         * `x1, y1, x2, y2` or `x1, y1, w, h`, all of which receive a pixel value.
         */
        boundingBox: PropTypes.object,
    }),
    /**
     * Define a custom context menu. The behaviour of each menu item can be defined in 1 of 3 ways.
     * 1. By passing a string to onClick that refers to one of the built-in Javascript functions.
     * 2. By passing a string to onClickCustom that refers to one of the user-defined functions in a namespace.
     * 3. By omitting both of these properties; this will update the contextMenuData property and trigger a Dash callback.
     */
    contextMenu: PropTypes.arrayOf(
        PropTypes.exact({
            /** ID of the menu item in the context menu */
            id: PropTypes.string.isRequired,
            /** The label on the context menu item*/
            label: PropTypes.string.isRequired,
            /** The tooltip text when hovering on top of a context menu item */
            tooltipText: PropTypes.string,
            /** A list containing either 'node', 'edge',and/or 'canvas'. This will determine where the context
             *  menu item will show up.
             */
            availableOn: PropTypes.array,
            /** Specify which built-in JavaScript function to use as behaviour for the context
             * menu item. One of 'remove', 'add_node', or 'add_edge'
             */
            onClick: PropTypes.string,
            /** Specify which user-defined Javascript function to use in the dashCytoscapeFunctions
             * namespace as behaviour for the context menu item
             */
            onClickCustom: PropTypes.string,
        })
    ),
    /**
     * Retrieve relevant data when a context menu item is clicked.  Read-only.
     */
    contextMenuData: PropTypes.exact({
        /** ID of the menu item in the context menu */
        menuItemId: PropTypes.string,
        /** x-position of the context click */
        x: PropTypes.number,
        /** y-position of the context click */
        y: PropTypes.number,
        /** Timestamp of context click*/
        timeStamp: PropTypes.number,
        /** Element ID on context click if the context click was on an element.
         * If context click was on white space, this property is not returned
         */
        elementId: PropTypes.string,
        /** Node ID of the edge source if the clicked element is an edge,
         * or else this property is not returned*/
        edgeSource: PropTypes.string,
        /** Node ID of the edge target if the clicked element is an edge,
         * or else this property is not returned*/
        edgeTarget: PropTypes.string,
    }),
    // Viewport Manipulation

    /**
     * Dictionary indicating the initial panning position of the graph. The
     * following keys are accepted:
     */
    pan: PropTypes.exact({
        /** The x-coordinate of the node */
        x: PropTypes.number,
        /** The y-coordinate of the node  */
        y: PropTypes.number,
    }),

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
     */
    tapNode: PropTypes.exact({
        /** node specific item */
        edgesData: PropTypes.array,
        /** node specific item */
        renderedPosition: PropTypes.object,
        /** node specific item */
        timeStamp: PropTypes.number,
        /** General item (for all elements) */
        classes: PropTypes.string,
        /** General item (for all elements) */
        data: PropTypes.object,
        /** General item (for all elements) */
        grabbable: PropTypes.bool,
        /** General item (for all elements) */
        group: PropTypes.string,
        /** General item (for all elements) */
        locked: PropTypes.bool,
        /** General item (for all elements) */
        position: PropTypes.object,
        /** General item (for all elements) */
        selectable: PropTypes.bool,
        /** General item (for all elements) */
        selected: PropTypes.bool,
        /** General item (for all elements) */
        style: PropTypes.object,
        /** Item for compound nodes */
        ancestorsData: PropTypes.oneOfType([PropTypes.object, PropTypes.array]),
        /** Item for compound nodes */
        childrenData: PropTypes.oneOfType([PropTypes.object, PropTypes.array]),
        /** Item for compound nodes */
        descendantsData: PropTypes.oneOfType([
            PropTypes.object,
            PropTypes.array,
        ]),
        /** Item for compound nodes */
        parentData: PropTypes.oneOfType([PropTypes.object, PropTypes.array]),
        /** Item for compound nodes */
        siblingsData: PropTypes.oneOfType([PropTypes.object, PropTypes.array]),
        /** Item for compound nodes */
        isParent: PropTypes.bool,
        /** Item for compound nodes */
        isChildless: PropTypes.bool,
        /** Item for compound nodes */
        isChild: PropTypes.bool,
        /** Item for compound nodes */
        isOrphan: PropTypes.bool,
        /** Item for compound nodes */
        relativePosition: PropTypes.object,
    }),

    /**
     * The data dictionary of a node returned when you tap or click it. Read-only.
     */
    tapNodeData: PropTypes.object,

    /**
     * The complete edge dictionary returned when you tap or click it. Read-only.
     */
    tapEdge: PropTypes.exact({
        /** Edge-specific item */
        isLoop: PropTypes.bool,
        /** Edge-specific item */
        isSimple: PropTypes.bool,
        /** Edge-specific item */
        midpoint: PropTypes.object,
        /** Edge-specific item */
        sourceData: PropTypes.object,
        /** Edge-specific item */
        sourceEndpoint: PropTypes.object,
        /** Edge-specific item */
        targetData: PropTypes.object,
        /** Edge-specific item */
        targetEndpoint: PropTypes.object,
        /** Edge-specific item */
        timeStamp: PropTypes.number,
        /** General item (for all elements) */
        classes: PropTypes.string,
        /** General item (for all elements) */
        data: PropTypes.object,
        /** General item (for all elements) */
        grabbable: PropTypes.bool,
        /** General item (for all elements) */
        group: PropTypes.string,
        /** General item (for all elements) */
        locked: PropTypes.bool,
        /** General item (for all elements) */
        selectable: PropTypes.bool,
        /** General item (for all elements) */
        selected: PropTypes.bool,
        /** General item (for all elements) */
        style: PropTypes.object,
    }),

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
     * a callback after it has been rendered.
     *
     * If the app does not need the image data server side and/or it will only be used to download
     * the image, it may be prudent to invoke `'download'` for `action` instead of
     * `'store'` to improve performance by preventing transfer of data to the server.
     */
    generateImage: PropTypes.shape({
        /** File type to output  */
        type: PropTypes.oneOf(['svg', 'png', 'jpg', 'jpeg']),
        /** Dictionary of options to cy.png() / cy.jpg() or cy.svg() for image generation.
         * See https://js.cytoscape.org/#core/export for details. For `'output'`, only 'base64'
         * and 'base64uri' are supported. Default: `{'output': 'base64uri'}`.*/
        options: PropTypes.object,
        /**
         * `'store'`: Stores the image data (only jpg and png are supported)
         * in `imageData` and invokes server-side Dash callbacks. `'download'`: Downloads the image
         * as a file with all data handling done client-side. No `imageData` callbacks are fired.
         * `'both'`: Stores image data and downloads image as file. The default is `'store'`
         */
        action: PropTypes.oneOf(['store', 'download', 'both']),
        /** Name for the file to be downloaded. Default: 'cyto'.*/
        filename: PropTypes.string,
    }),

    /**
     * String representation of the image requested with generateImage. Null if no
     * image was requested yet or the previous request failed. Read-only.
     */
    imageData: PropTypes.string,

    /**
     * Toggles intelligent responsive resize of Cytoscape graph with viewport size change
     */
    responsive: PropTypes.bool,

    /**
     * If set to True, mouseoverNodeData and mouseoverEdgeData will be cleared on unhover.
     * If set to False, the value of mouseoverNodeData and mouseoverEdgeData will be the last
     * Node or Edge hovered over
     */
    clearOnUnhover: PropTypes.bool,
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
    clearOnUnhover: false,
    elements: [],
    contextMenu: [],
};

export default Cytoscape;
