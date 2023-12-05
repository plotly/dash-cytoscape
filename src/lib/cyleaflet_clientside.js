import proj4 from 'proj4'


if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.cyleaflet_utils = {
    // Proj4 coordinate conversion object
    // object with 2 methods: `forward` converts from lat/lon to x/y,
    // and `inverse` converts from x/y to lat/lon.
    //  - EPSG:4326 is the 'standard' lat/lon coordinate system,
    //  - EPSG:3857 is the 'Web Mercator' projection used by many
    //    online mapping serveces including Leaflet
    // Note: proj4.js is imported as an part of `external_scripts`
    // in demos/usage-cy-leaflet-aio-ekl.py
    _proj4js_converter: proj4('EPSG:4326', 'EPSG:3857'),

    lonLatToXY: function (lon, lat) {
        var xy = this._proj4js_converter.forward([lon, lat]);
        var x = xy[0];
        var y = -xy[1];
        return [x, y];
    },

    xYToLonLat: function (x, y) {
        var lonlat = this._proj4js_converter.inverse([x, -y]);
        var lon = lonlat[0];
        var lat = lonlat[1];
        return [lon, lat];
    },

    transformElements: function (elements) {
        return elements.map((e) => {
            if (e.data.hasOwnProperty('lat')) {
                var xy = this.lonLatToXY(e.data.lon, e.data.lat);
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

window.dash_clientside.cyleaflet = {
    updateLeafBoundsAIO: function (cyExtent) {
        if (!cyExtent) {
            return window.dash_clientside.no_update;
        }
        var utils = window.dash_clientside.cyleaflet_utils;

        var lonLatMin = utils.xYToLonLat(cyExtent.x1, cyExtent.y1);
        var lonMin = lonLatMin[0];
        var latMin = lonLatMin[1];

        var lonLatMax = utils.xYToLonLat(cyExtent.x2, cyExtent.y2);
        var lonMax = lonLatMax[0];
        var latMax = lonLatMax[1];

        var bounds = [
            [latMax, lonMin],
            [latMin, lonMax],
        ];
        return {
            bounds: bounds,
            transition: 'panTo',
        };
    },
    transformElements: function (elements) {
        return window.dash_clientside.cyleaflet_utils.transformElements(elements);
    },
};
