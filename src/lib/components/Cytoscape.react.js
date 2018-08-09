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
            elements,
            stylesheet,
            layout
        } = this.props;

        const layout_extension = {name: layout};

        return (
            <CytoscapeComponent
                id={id}
                style={style}
                elements={elements}
                stylesheet={stylesheet}
                layout={layout_extension}
            />
        )
    }
}


Cytoscape.propTypes = {
    /**
     * The ID used to identify this compnent in Dash callbacks
     */
    id: PropTypes.string,

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
    elements: PropTypes.arrayOf(
        PropTypes.object
    ),

    /**
     * The Cytoscape stylesheet as non-stringified JSON. N.b. the prop key is
     * stylesheet rather than style, the key used by Cytoscape itself, so as
     * to not conflict with the HTML style attribute.
     */
    stylesheet: PropTypes.arrayOf(
        PropTypes.object
    ),

    /**
     * Use a layout to automatically position the nodes in the graph. Simply
     * give the string denoting the name of the layout.
     *
     * This prop is rendered when the component is declared, and might not
     * update if you change it with a callback.
     */
    layout: PropTypes.string
};

Cytoscape.defaultProps = {
    style: {width: '600px', height: '600px'},
    layout: 'random'
};