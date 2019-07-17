export default class Resize {
    constructor(cy) {
        this.shouldResize = false;

        this.cy = cy;
        this.cur = {};
        this.prev = {};

        this.marginPercentage = {};

        // constants
        this.containedZoomMargin = 0.05;

        this.toggle = this.toggle.bind(this);
        this.getViewport = this.getViewport.bind(this);
        this.updateViewport = this.updateViewport.bind(this);
        this.xConstrainedZoom = this.xConstrainedZoom.bind(this);
        this.xChangeMargin = this.xChangeMargin.bind(this);
        this.yConstrainedZoom = this.yConstrainedZoom.bind(this);
        this.yChangeMargin = this.yChangeMargin.bind(this);
        this.resize = this.resize.bind(this);
    }

    /////////////////////////////////////////////////////////////////

    toggle(state = !this.shouldResize) {
        const cy = this.cy;

        if(state !== this.shouldResize) {
            if(state) {
                cy.on('render', this.updateViewport);
                cy.on('resize', this.resize);
            }
            else {
                cy.removeListener('render', this.updateViewport);
                cy.removeListener('resize', this.resize);
            }

            this.shouldResize = state;
        }
    }

    /////////////////////////////////////////////////////////////////

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

    /////////////////////////////////////////////////////////////////

    xConstrainedZoom(level) {
        const {cur, prev, marginPercentage} = this;

    // Look at constrained dimension
        // calculate the new position needed to maintain same left/right margin percentages
        // with new zoom
        const newRenderedBBX1 = marginPercentage.left * cur.width;

        cur.position.x = newRenderedBBX1 + (prev.position.x - prev.renderedBB.x1);

    // Look at unconstrained dimension
        // get midpoint
        const midpoint = cur.renderedBB.y1 + cur.renderedBB.h / 2;
        // get new height of graph
        const newHeight = cur.renderedBB.h / prev.zoom * level;
        // get new top margin
        const newRenderedBBY1 = midpoint - (newHeight / 2);

        cur.position.y = newRenderedBBY1 + (prev.position.y - prev.renderedBB.y1);
    }

    xChangeMargin(width) {
        const {cur, prev} = this;

        // get initial centroid percentage from the BB left boundary
        const xCentroidPos = prev.renderedBB.x1 + prev.renderedBB.w / 2;
        const xCentroidPosPer = xCentroidPos / prev.width;

        // calculate new x1 position using new width;
        const newXCentroidPos = xCentroidPosPer * width;

        // Find displacement in x required to bring to new position
        cur.position.x = cur.position.x + (newXCentroidPos - xCentroidPos);
    }

    yConstrainedZoom(level) {
        // same as this.xConstrainedZoom except x and y switched where applicable
        const {cur, prev, marginPercentage} = this;

        const newRenderedBBY1 = marginPercentage.top * cur.height;
        cur.position.y = newRenderedBBY1 + (prev.position.y - prev.renderedBB.y1);

        const midpoint = cur.renderedBB.x1 + cur.renderedBB.w / 2;
        const newWidth = cur.renderedBB.w / prev.zoom * level;
        const newRenderedBBX1 = midpoint - (newWidth / 2);
        cur.position.x = newRenderedBBX1 + (prev.position.x - prev.renderedBB.x1);
    }

    yChangeMargin() {
        // same as xChangeMargin except x and y switched where applicable
        const {cur, prev} = this;

        const yCentroidPos = prev.renderedBB.y1 + prev.renderedBB.h / 2;
        const yCentroidPosPer = yCentroidPos / prev.height;

        const newYCentroidPos = yCentroidPosPer * cur.height;

        cur.position.y = cur.position.y + (newYCentroidPos - yCentroidPos);
    }

    /////////////////////////////////////////////////////////////////

    resize() {
        const cy = this.cy;
        this.cur = this.getViewport(cy);

        const {cur, prev} = this;

        // Is the figure fully contained in the viewport?
        const fullyContained = (prev.renderedBB.x1 >= 0)
            && (prev.renderedBB.y1 >= 0)
            && (prev.renderedBB.x2 <= prev.width)
            && (prev.renderedBB.y2 <= prev.height);

        // Calculate margin percentages based on prev vals
        this.marginPercentage = {
            left: prev.renderedBB.x1 / prev.width,
            // right: ( prev.width - prev.renderedBB.x2 ) / prev.width,
            top: prev.renderedBB.y1 / prev.height,
            // bottom: ( prev.height - prev.renderedBB.y2 ) / prev.height,
        };

        // Find constrained dimension
        // Find which dimension has changed the most as a percentage of the current dimensions
        const xConstrained = Math.abs(1 - (cur.width / prev.width))
            > Math.abs(1 - (cur.height / prev.height));

        // define output variables
        if(xConstrained) {
            // calculate zoom so that the width remains same
            const targetZoom = prev.zoom / prev.width * cur.width;
            if(fullyContained) {
                const maxContainedZoom = Math.min(
                    (cur.renderedBB.y1 + (cur.renderedBB.h / 2)) * prev.zoom * 2 / cur.renderedBB.h,
                    - (cur.renderedBB.y1 + (cur.renderedBB.h / 2) - prev.height) * prev.zoom * 2 / cur.renderedBB.h
                ) - this.containedZoomMargin;
                const maxContainedWidth = prev.width / prev.zoom * maxContainedZoom;

                // Setup state machine and required variables
                let currentState = cur.zoom < maxContainedZoom ? -1 : 1;
                const targetState = targetZoom < maxContainedZoom ? -1 : 1;
                while(Math.abs(currentState) <= 1) {
                    // set an intermediate target zoom if a transition through the maxContained level is needed
                    if(currentState === -1) {
                        const intermediateTargetZoom = targetState === 1
                            ? maxContainedZoom
                            : targetZoom;
                        this.xConstrainedZoom(intermediateTargetZoom);
                        cur.zoom = intermediateTargetZoom;
                        if(targetState === 1) {
                            this.prev.position = this.cur.position;
                            this.prev.width = maxContainedWidth;
                        }
                    }
                    else { // if(currentState === 1) {
                        const intermediateTargetWidth = targetState === -1
                            ? maxContainedWidth
                            : cur.width;
                        this.xChangeMargin(intermediateTargetWidth);
                        if(targetState === -1) {
                            this.prev.position = this.cur.position;
                            this.prev.width = maxContainedWidth;
                        }
                    }

                    currentState += 2 * targetState;
                }
            }
            else {
                cur.zoom = targetZoom;
                this.xConstrainedZoom(cur.zoom);
            }
        }
        else { // is y Constrained
            // calculate zoom so that the width remains same
            const targetZoom = prev.zoom / prev.height * cur.height;
            if(fullyContained) {
                const maxContainedZoom = Math.min(
                    (cur.renderedBB.x1 + (cur.renderedBB.w / 2)) * prev.zoom * 2 / cur.renderedBB.w,
                    - (cur.renderedBB.x1 + (cur.renderedBB.w / 2) - prev.width) * prev.zoom * 2 / cur.renderedBB.w
                ) - this.containedZoomMargin;
                const maxContainedHeight = prev.height / prev.zoom * maxContainedZoom;

                // Setup state machine and required variables
                let currentState = cur.zoom < maxContainedZoom ? -1 : 1;
                const targetState = targetZoom < maxContainedZoom ? -1 : 1;
                while(Math.abs(currentState) <= 1) {
                    // set an intermediate target zoom if a transition through the maxContained level is needed
                    if(currentState === -1) {
                        const intermediateTargetZoom = targetState === 1
                            ? maxContainedZoom
                            : targetZoom;
                        this.yConstrainedZoom(intermediateTargetZoom);
                        cur.zoom = intermediateTargetZoom;
                        if(targetState === 1) {
                            this.prev.position = this.cur.position;
                            this.prev.height = maxContainedHeight;
                        }
                    }
                    else { // if(currentState === 1) {
                        const intermediateTargetHeight = targetState === -1
                            ? maxContainedHeight
                            : cur.height;
                        this.yChangeMargin(intermediateTargetHeight);
                        if(targetState === -1) {
                            this.prev.position = this.cur.position;
                            this.prev.height = maxContainedHeight;
                        }
                    }

                    currentState += 2 * targetState;
                }
            }
            else {
                cur.zoom = targetZoom;
                this.yConstrainedZoom(cur.zoom);
            }
        }

        cy.zoom({level: cur.zoom});
        cy.pan(cur.position);
        this.prev = this.cur;

        return cur;
    }
};
