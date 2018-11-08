/* eslint no-magic-numbers: 0 */
import React from 'react';
import Cytoscape from '../lib/components/Cytoscape.react.js';


const elements = [
    {
        data: {id: 'one', label: 'Node 1'},
        position: {x: 50, y: 50}
    },
    {
        data: {id: 'two', label: 'Node 2'},
        position: {x: 200, y: 200}
    },
    {
        data: {id: 'three', label: 'Node 3'},
        position: {x: 100, y: 150}
    },
    {
        data: {id: 'four', label: 'Node 4'},
        position: {x: 400, y: 50}
    },
    {
        data: {id: 'five', label: 'Node 5'},
        position: {x: 250, y: 100}
    },
    {
        data: {id: 'six', label: 'Node 6', parent: 'three'},
        position: {x: 150, y: 150}
    },

    {data: {
        source: 'one',
        target: 'two',
        label: 'Edge from Node1 to Node2'
    }},
    {data: {
        source: 'one',
        target: 'five',
        label: 'Edge from Node 1 to Node 5'
    }},
    {data: {
        source: 'two',
        target: 'four',
        label: 'Edge from Node 2 to Node 4'
    }},
    {data: {
        source: 'three',
        target: 'five',
        label: 'Edge from Node 3 to Node 5'
    }},
    {data: {
        source: 'three',
        target: 'two',
        label: 'Edge from Node 3 to Node 2'
    }},
    {data: {
        source: 'four',
        target: 'four',
        label: 'Edge from Node 4 to Node 4'
    }},
    {data: {
        source: 'four',
        target: 'six',
        label: 'Edge from Node 4 to Node 6'
    }},
    {data: {
        source: 'five',
        target: 'one',
        label: 'Edge from Node 5 to Node 1'
    }},
];

class App extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <Cytoscape
            elements={elements}
        />
    }
}

export default App;
