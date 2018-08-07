/* eslint no-magic-numbers: 0 */
import React from 'react';
import ReactDOM from 'react-dom';
import CytoscapeComponent from 'cytoscape-reactjs';

class App extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    const elements = [
       { data: { id: 'one', label: 'Node 1' }, position: { x: 0, y: 0 } },
       { data: { id: 'two', label: 'Node 2' }, position: { x: 100, y: 0 } },
       { data: { source: 'one', target: 'two', label: 'Edge from Node1 to Node2' } }
    ];

    return <CytoscapeComponent elements={elements} style="width: 600px; height: 600px;" />;
  }
};

export default App;
