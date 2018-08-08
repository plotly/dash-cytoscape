/* eslint no-magic-numbers: 0 */
import React from 'react';
import ReactDOM from 'react-dom';
import CytoscapeComponent from '../react-cytoscapejs/src/component.js';

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

    return <CytoscapeComponent
        elements={elements}
        style={{
            width: '1000px',
            height: '600px',
            margin: '50px'
        }}
    />;
  }
}

export default App;
