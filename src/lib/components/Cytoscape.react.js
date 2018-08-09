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
     *
     * You can find a list of Layout extensions here:
         arbor : The Arbor physics simulation layout. It’s a basic physics layout.

         cola : The Cola.js physics simulation layout. Cola makes beautiful layout results, it animates very smoothly, and it has great options for controlling the layout.

         cose-bilkent : The CoSE layout by Bilkent with enhanced compound node placement. CoSE Bilkent gives near-perfect end results. However, it’s more expensive than the version of CoSE directly included with Cytoscape.js.

         dagre : The Dagre layout for DAGs and trees.

         euler : Euler is a fast, small file-size, high-quality force-directed (physics simulation) layout. It is excellent for non-compound graphs, and it has basic support for compound graphs.

         klay : Klay is a layout that works well for most types of graphs. It gives good results for ordinary graphs, and it handles DAGs and compound graphs very nicely.

         ngraph.forcelayout : A physics simulation layout that works particularly well on planar graphs. It is relatively fast.

         polywas : A layout for GWAS (genome-wide association study) data illustrating inter-locus relationships.

         spread : The speedy Spread physics simulation layout. It tries to use all the viewport space, but it can be configured to produce a tighter result. It uses Fruchterman-Reingold initially, and it uses Gansner and North for the spread phase.

         springy : The Springy physics simulation layout. It’s a basic physics layout.
     */
    layout: PropTypes.string
};

Cytoscape.defaultProps = {
    style: {width: '600px', height: '600px'},
    layout: 'random'
};