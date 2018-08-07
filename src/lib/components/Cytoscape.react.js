import React, {Component} from 'react';
import PropTypes from 'prop-types';
import CytoscapeComponent from 'cytoscape-reactjs';


/**
 * ExampleComponent is an example component.
 * It takes a property, `label`, and
 * displays it.
 * It renders an input with the property `value`
 * which is editable by the user.
 */
export default class Cytoscape extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        const {id} = this.props;

        const elements = [
            {data: {id: 'one', label: 'Node 1'}, position: {x: 0, y: 0}},
            {data: {id: 'two', label: 'Node 2'}, position: {x: 100, y: 0}},
            {
                data: {
                    source: 'one',
                    target: 'two',
                    label: 'Edge from Node1 to Node2'
                }
            }
        ];

        return (
            <CytoscapeComponent
                id={id}
                elements={elements}
                style="width: 600px; height: 600px;"
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
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func
};
