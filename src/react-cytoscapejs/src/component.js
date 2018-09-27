import React from 'react';
import ReactDOM from 'react-dom';
import { types } from './types';
import { defaults } from './defaults';
import Cytoscape from 'cytoscape';
import { patch } from './patch';

/**
 * The `CytoscapeComponent` is a React component that allows for the declarative creation
 * and modification of a Cytoscape instance, a graph visualisation.
 */
export default class CytoscapeComponent extends React.Component {
  static get propTypes() {
    return types;
  }

  static get defaultProps() {
    return defaults;
  }

  constructor(props) {
    super(props);
  }

  componentDidMount() {
    const container = ReactDOM.findDOMNode(this);
    const { global } = this.props;
    const cy = (this._cy = new Cytoscape({ container }));

    if (global) {
      window[global] = cy;
    }

    this.updateCytoscape(null, this.props);
  }

  updateCytoscape(prevProps, newProps) {
    const cy = this._cy;
    const { diff, toJson, get, forEach } = newProps;

    // batch for peformance
    cy.batch(() => {
      patch(cy, prevProps, newProps, diff, toJson, get, forEach);
    });

    if (newProps.cy != null) {
      newProps.cy(cy);
    }
  }

  componentDidUpdate(prevProps) {
    this.updateCytoscape(prevProps, this.props);
  }

  componentWillUnmount() {
    this._cy.destroy();
  }

  render() {
    const { id, className, style } = this.props;

    return React.createElement('div', {
      id,
      className,
      style
    });
  }
}
