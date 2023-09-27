/* eslint-disable import/prefer-default-export */
import Cytoscape from './components/Cytoscape.react';
import CytoscapeJS from 'cytoscape';
import svg from 'cytoscape-svg';

CytoscapeJS.use(svg);

export {Cytoscape};
