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
var conversion_factor = 20037508.34;

// Convert EPSG:4326 to EPSG:3857
// We also flip the sign of the y-value to match Cytoscape's coordinate system
function lonLatToXY(lon, lat) {
    var x = lon * conversion_factor / 180;
    var y = -Math.log(Math.tan((90 + lat) * Math.PI / 360)) * conversion_factor / Math.PI;
    return [x, y];
}

// Convert EPSG:3857 to EPSG:4326
// We also flip the sign of the y-value to match Cytoscape's coordinate system
function xYToLonLat(x, y) {
    var lon = x * 180 / conversion_factor;
    var lat = Math.atan(Math.exp(-y * Math.PI / conversion_factor)) * 360 / Math.PI - 90;
    return [lon, lat];
}

window.dash_clientside.cyleaflet_utils = {
};

window.dash_clientside.cyleaflet = {
    updateLeafBounds: function (cyExtent) {
        if (!cyExtent) {
            return window.dash_clientside.no_update;
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
                options: { animate: true },
            }
        ];
    },
    transformElements: function (elements) {
        return elements.map((e) => {
            if (e.data.hasOwnProperty('lat')) {
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
};
