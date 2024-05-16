if (!window.dash_clientside) {
    window.dash_clientside = {};
}

// Functions to convert lat/lon used by Leaflet to x/y used by Cytoscape.
//  - EPSG:4326 is the 'standard' (Mercator) grid coordinate system,
//    which maps nicely to Cytoscape's x/y grid
//  - EPSG:3857 is the 'Web Mercator' projection used by many
//    online mapping serveces including Leaflet
// Reference: https://epsg.io/3857

// Conversion factor based on EPSG:3857 bounds
const conversion_factor = 20037508.34;

const double_lon = 360;
const max_lon = 180;
const max_lat = 90;

const leafletZoomMultiplier = 0.418;
const leafletZoomReference = 16;
const defaultLeafletMaxZoom = 18;

// Convert EPSG:4326 to EPSG:3857
// We also flip the sign of the y-value to match Cytoscape's coordinate system
function lonLatToXY(lon, lat) {
    var x = (lon * conversion_factor) / max_lon;
    var y =
        (-Math.log(Math.tan(((max_lat + lat) * Math.PI) / double_lon)) *
            conversion_factor) /
        Math.PI;
    return [x, y];
}

// Convert EPSG:3857 to EPSG:4326
// We also flip the sign of the y-value to match Cytoscape's coordinate system
function xYToLonLat(x, y) {
    var lon = (x * max_lon) / conversion_factor;
    var lat =
        (Math.atan(Math.exp((-y * Math.PI) / conversion_factor)) * double_lon) /
            Math.PI -
        max_lat;
    return [lon, lat];
}

function computeCytoscapeMaxZoom(leafletMaxZoom) {
    return leafletZoomMultiplier * 2 ** (leafletMaxZoom - leafletZoomReference);
}

window.dash_clientside.cyleaflet = {
    updateLeafBounds: function (cyExtentInput, max_zoom, cyExtentStore) {
        var cyExtent = cyExtentInput;
        if (!cyExtent) {
            if (!cyExtentStore) {
                return window.dash_clientside.no_update;
            }
            cyExtent = cyExtentStore;
        }

        var lonLatMin = xYToLonLat(cyExtent.x1, cyExtent.y1);
        var lonMin = lonLatMin[0];
        var latMin = lonLatMin[1];

        var lonLatMax = xYToLonLat(cyExtent.x2, cyExtent.y2);
        var lonMax = lonLatMax[0];
        var latMax = lonLatMax[1];

        var invalidateSize = new Date().getTime();
        var bounds = [
            [latMax, lonMin],
            [latMin, lonMax],
        ];

        // Prevent callback from returning invalid bounds
        // which would cause dash_leaflet to crash
        if (latMin === latMax || lonMin === lonMax) {
            return window.dash_clientside.no_update;
        }

        return [
            invalidateSize,
            {
                bounds: bounds,
                options: {animate: true},
            },
            cyExtent,
        ];
    },
    transformElements: function (elements) {
        return elements.map((e) => {
            if (Object.prototype.hasOwnProperty.call(e.data, 'lat')) {
                var xy = lonLatToXY(e.data.lon, e.data.lat);
                return {
                    data: e.data,
                    position: {
                        y: xy[1],
                        x: xy[0],
                    },
                };
            }
            return e;
        });
    },
    updateLonLat: function (elements) {
        if (elements.length > 0) {
            return elements.map((e) => {
                if (
                    typeof e.position !== 'undefined' &&
                    Object.prototype.hasOwnProperty.call(e.position, 'x') &&
                    e.position.x !== 0 &&
                    e.position.y !== 0
                ) {
                    var lonLat = xYToLonLat(e.position.x, e.position.y);
                    return {
                        position: e.position,
                        data: Object.assign({}, e.data, {
                            lon: lonLat[0],
                            lat: lonLat[1],
                        }),
                    };
                }
                return e;
            });
        }
        return window.dash_clientside.no_update;
    },
    updateCytoMaxZoom: function (children) {
        var tileLayer = children;
        if (children.length >= 1) {
            tileLayer = children.filter((e) => {
                return e.type === 'TileLayer';
            });
            if (tileLayer.length === 1) {
                tileLayer = tileLayer[0];
            }
        }

        var leafletMaxZoom = defaultLeafletMaxZoom;
        if (
            typeof tileLayer.props !== 'undefined' &&
            Object.prototype.hasOwnProperty.call(tileLayer.props, 'maxZoom')
        ) {
            leafletMaxZoom = tileLayer.props.maxZoom;
        }
        return computeCytoscapeMaxZoom(leafletMaxZoom);
    },
};
