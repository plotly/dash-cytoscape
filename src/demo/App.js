/* eslint no-magic-numbers: 0 */
/**
 * JavaScript Requirements: cytoscape
 * React.js requirements: cytoscape-reactjs
 */
import React from 'react';
import Cytoscape from '../lib/components/Cytoscape.react.js';

class App extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    const elements = [
       { data: { id: 'one', label: 'Node 1' }, position: { x: 50, y: 50 } },
       { data: { id: 'two', label: 'Node 2' }, position: { x: 200, y: 200 } },
       { data: { source: 'one', target: 'two', label: 'Edge from Node1 to Node2' } }
    ];

    return <Cytoscape
        elements={elements}
    />
  }
}

export default App;
