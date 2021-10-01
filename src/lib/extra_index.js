/* eslint-disable import/prefer-default-export */
import Cytoscape from './components/Cytoscape.react';
import CytoscapeJS from 'cytoscape';
import coseBilkent from 'cytoscape-cose-bilkent';
import fcose from 'cytoscape-fcose';
import cola from 'cytoscape-cola';
import dagre from 'cytoscape-dagre';
import euler from 'cytoscape-euler';
import klay from 'cytoscape-klay';
import spread from 'cytoscape-spread';
import svg from 'cytoscape-svg';
import contextMenus from 'cytoscape-context-menus';
import 'cytoscape-context-menus/cytoscape-context-menus.css';
import leaflet from 'cytoscape-leaf';
import 'cytoscape-leaf/cytoscape-leaf.css';
import 'leaflet/dist/leaflet.css';

CytoscapeJS.use(coseBilkent);
CytoscapeJS.use(fcose);
CytoscapeJS.use(cola);
CytoscapeJS.use(dagre);
CytoscapeJS.use(euler);
CytoscapeJS.use(klay);
CytoscapeJS.use(spread);
CytoscapeJS.use(svg);
CytoscapeJS.use(contextMenus);
CytoscapeJS.use(leaflet);

export {
    Cytoscape
};
