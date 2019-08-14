/* eslint-disable import/prefer-default-export */
import Cytoscape from './components/Cytoscape.react';
import CytoscapeJS from 'cytoscape';
import ctxmenu from 'cytoscape-cxtmenu';
import coseBilkent from 'cytoscape-cose-bilkent';
import cola from 'cytoscape-cola';
import dagre from 'cytoscape-dagre';
import euler from 'cytoscape-euler';
import klay from 'cytoscape-klay';
import spread from 'cytoscape-spread';

CytoscapeJS.use(ctxmenu);
CytoscapeJS.use(coseBilkent);
CytoscapeJS.use(cola);
CytoscapeJS.use(dagre);
CytoscapeJS.use(euler);
CytoscapeJS.use(klay);
CytoscapeJS.use(spread);

export {
    Cytoscape
};
