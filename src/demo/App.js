/* eslint no-magic-numbers: 0 */
import React from 'react';
import Cytoscape from '../lib/components/Cytoscape.react.js';
// Data from this example: https://github.com/cytoscape/cytoscape.js/blob/master/documentation/demos/tokyo-railways/tokyo-railways.js
import data from './data.json'

class App extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <Cytoscape
            elements={data.elements}
        />
    }
}

export default App;
