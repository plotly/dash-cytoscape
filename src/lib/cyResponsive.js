export default class cyResponsive {
    constructor(cy) {
        this.shouldResize = false;

        this.cy = cy;
        this.curr = {};
        this.prev = {};

        this.marginPercentage = {};

        // constants
        this.containedZoomMargin = 0.05;

        this.toggle = this.toggle.bind(this);
        this.getViewport = this.getViewport.bind(this);
        this.updateViewport = this.updateViewport.bind(this);
        this._xConstrainedZoom = this._xConstrainedZoom.bind(this);
        this._xChangeMargin = this._xChangeMargin.bind(this);
        this._yConstrainedZoom = this._yConstrainedZoom.bind(this);
        this._yChangeMargin = this._yChangeMargin.bind(this);
        this.resize = this.resize.bind(this);
    }

    toggle(state = !this.shouldResize) {
        const cy = this.cy;

        if (state !== this.shouldResize) {
            if (state) {
                cy.on('render', this.updateViewport);
                cy.on('resize', this.resize);

                this.updateViewport(cy);
            } else {
                cy.removeListener('render', this.updateViewport);
                cy.removeListener('resize', this.resize);
            }

            this.shouldResize = state;
        }
    }

    getViewport() {
        const cy = this.cy;
        return {
            position: cy.pan(),
            zoom: cy.zoom(),
            renderedBB: Object.assign({}, cy.elements().renderedBoundingBox()),
            height: cy.height(),
            width: cy.width(),
        };
    }

    updateViewport() {
        const cy = this.cy;
        this.prev = this.getViewport(cy);
    }

    _xConstrainedZoom(level) {
        const {curr, prev, marginPercentage} = this;

        // Look at constrained dimension
        // calculate the new position needed to maintain same left/right margin percentages
        // with new zoom
        const newRenderedBBX1 = marginPercentage.left * curr.width;

        curr.position.x =
            newRenderedBBX1 + (prev.position.x - prev.renderedBB.x1);

        // Look at unconstrained dimension
        // get midpoint
        const midpoint = curr.renderedBB.y1 + curr.renderedBB.h / 2;
        // get new height of graph
        const newHeight = (curr.renderedBB.h / prev.zoom) * level;
        // get new top margin
        let newRenderedBBY1 = midpoint - newHeight / 2;
        // compensate for any change in height between prev and curr
        newRenderedBBY1 = newRenderedBBY1 + (curr.height - prev.height) / 2;

        curr.position.y =
            newRenderedBBY1 + (prev.position.y - prev.renderedBB.y1);
    }

    _xChangeMargin(width) {
        const {curr, prev} = this;

        // get initial centroid percentage from the BB left boundary
        const xCentroidPos = prev.renderedBB.x1 + prev.renderedBB.w / 2;
        const xCentroidPosPer = xCentroidPos / prev.width;

        // calculate new x1 position using new width;
        const newXCentroidPos = xCentroidPosPer * width;

        // Find displacement in x required to bring to new position
        curr.position.x = curr.position.x + (newXCentroidPos - xCentroidPos);
    }

    _yConstrainedZoom(level) {
        // same as this._xConstrainedZoom except x and y switched where applicable
        const {curr, prev, marginPercentage} = this;

        const newRenderedBBY1 = marginPercentage.top * curr.height;
        curr.position.y =
            newRenderedBBY1 + (prev.position.y - prev.renderedBB.y1);

        const midpoint = curr.renderedBB.x1 + curr.renderedBB.w / 2;
        const newWidth = (curr.renderedBB.w / prev.zoom) * level;
        let newRenderedBBX1 = midpoint - newWidth / 2;
        newRenderedBBX1 = newRenderedBBX1 + (curr.width - prev.width) / 2;

        curr.position.x =
            newRenderedBBX1 + (prev.position.x - prev.renderedBB.x1);
    }

    _yChangeMargin() {
        // same as _xChangeMargin except x and y switched where applicable
        const {curr, prev} = this;

        const yCentroidPos = prev.renderedBB.y1 + prev.renderedBB.h / 2;
        const yCentroidPosPer = yCentroidPos / prev.height;

        const newYCentroidPos = yCentroidPosPer * curr.height;

        curr.position.y = curr.position.y + (newYCentroidPos - yCentroidPos);
    }

    resize() {
        const cy = this.cy;
        this.curr = this.getViewport(cy);

        const {curr, prev} = this;

        // Is the figure fully contained in the viewport?
        const fullyContained =
            prev.renderedBB.x1 >= 0 &&
            prev.renderedBB.y1 >= 0 &&
            prev.renderedBB.x2 <= prev.width &&
            prev.renderedBB.y2 <= prev.height;

        // Calculate margin percentages based on prev vals
        this.marginPercentage = {
            left: prev.renderedBB.x1 / prev.width,
            // right: ( prev.width - prev.renderedBB.x2 ) / prev.width,
            top: prev.renderedBB.y1 / prev.height,
            // bottom: ( prev.height - prev.renderedBB.y2 ) / prev.height,
        };

        // Find constrained dimension
        // Find which dimension has changed the most as a percentage of the currrent dimensions
        const xConstrained =
            Math.abs(1 - curr.width / prev.width) >
            Math.abs(1 - curr.height / prev.height);

        // define output variables
        if (xConstrained) {
            // calculate zoom so that the width remains same
            const targetZoom = (prev.zoom / prev.width) * curr.width;
            if (fullyContained) {
                const maxContainedZoom =
                    Math.min(
                        ((curr.renderedBB.y1 + curr.renderedBB.h / 2) *
                            prev.zoom *
                            2) /
                            curr.renderedBB.h,
                        (-(
                            curr.renderedBB.y1 +
                            curr.renderedBB.h / 2 -
                            prev.height
                        ) *
                            prev.zoom *
                            2) /
                            curr.renderedBB.h
                    ) - this.containedZoomMargin;
                const maxContainedWidth =
                    (prev.width / prev.zoom) * maxContainedZoom;

                // Setup state machine and required variables
                let currrentState = curr.zoom < maxContainedZoom ? -1 : 1;
                const targetState = targetZoom < maxContainedZoom ? -1 : 1;
                while (Math.abs(currrentState) <= 1) {
                    // set an intermediate target zoom if a transition through the maxContained level is needed
                    if (currrentState === -1) {
                        const intermediateTargetZoom =
                            targetState === 1 ? maxContainedZoom : targetZoom;
                        this._xConstrainedZoom(intermediateTargetZoom);
                        curr.zoom = intermediateTargetZoom;
                        if (targetState === 1) {
                            this.prev.position = this.curr.position;
                            this.prev.width = maxContainedWidth;
                        }
                    } else {
                        const intermediateTargetWidth =
                            targetState === -1 ? maxContainedWidth : curr.width;
                        this._xChangeMargin(intermediateTargetWidth);
                        if (targetState === -1) {
                            this.prev.position = this.curr.position;
                            this.prev.width = maxContainedWidth;
                        }
                    }

                    currrentState += 2 * targetState;
                }
            } else {
                curr.zoom = targetZoom;
                this._xConstrainedZoom(curr.zoom);
            }
        } else {
            // calculate zoom so that the width remains same
            const targetZoom = (prev.zoom / prev.height) * curr.height;
            if (fullyContained) {
                const maxContainedZoom =
                    Math.min(
                        ((curr.renderedBB.x1 + curr.renderedBB.w / 2) *
                            prev.zoom *
                            2) /
                            curr.renderedBB.w,
                        (-(
                            curr.renderedBB.x1 +
                            curr.renderedBB.w / 2 -
                            prev.width
                        ) *
                            prev.zoom *
                            2) /
                            curr.renderedBB.w
                    ) - this.containedZoomMargin;
                const maxContainedHeight =
                    (prev.height / prev.zoom) * maxContainedZoom;

                // Setup state machine and required variables
                let currrentState = curr.zoom < maxContainedZoom ? -1 : 1;
                const targetState = targetZoom < maxContainedZoom ? -1 : 1;
                while (Math.abs(currrentState) <= 1) {
                    // set an intermediate target zoom if a transition through the maxContained level is needed
                    if (currrentState === -1) {
                        const intermediateTargetZoom =
                            targetState === 1 ? maxContainedZoom : targetZoom;
                        this._yConstrainedZoom(intermediateTargetZoom);
                        curr.zoom = intermediateTargetZoom;
                        if (targetState === 1) {
                            this.prev.position = this.curr.position;
                            this.prev.height = maxContainedHeight;
                        }
                    } else {
                        const intermediateTargetHeight =
                            targetState === -1
                                ? maxContainedHeight
                                : curr.height;
                        this._yChangeMargin(intermediateTargetHeight);
                        if (targetState === -1) {
                            this.prev.position = this.curr.position;
                            this.prev.height = maxContainedHeight;
                        }
                    }

                    currrentState += 2 * targetState;
                }
            } else {
                curr.zoom = targetZoom;
                this._yConstrainedZoom(curr.zoom);
            }
        }

        cy.zoom({level: curr.zoom});
        cy.pan(curr.position);
        this.prev = this.curr;

        return curr;
    }
}
