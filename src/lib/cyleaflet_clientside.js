import proj4 from 'proj4'


if (!window.dash_clientside) {
    window.dash_clientside = {};
}

// Proj4 coordinate conversion object
// object with 2 methods: `forward` converts from lat/lon to x/y,
// and `inverse` converts from x/y to lat/lon.
//  - EPSG:4326 is the 'standard' lat/lon coordinate system,
//  - EPSG:3857 is the 'Web Mercator' projection used by many
//    online mapping serveces including Leaflet
var _proj4js_converter = proj4('EPSG:4326', 'EPSG:3857');

function lonLatToXY(lon, lat) {
    var xy = _proj4js_converter.forward([lon, lat]);
    var x = xy[0];
    var y = -xy[1];
    return [x, y];
}

function xYToLonLat(x, y) {
    var lonlat = _proj4js_converter.inverse([x, -y]);
    var lon = lonlat[0];
    var lat = lonlat[1];
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
