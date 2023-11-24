if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.utils = {
    CONVERSION_FACTOR: 100000,

    latToY: function (lat) {
        return -lat * this.CONVERSION_FACTOR;
    },
    yToLat: function (y, averageLat) {
        lat = -y / this.CONVERSION_FACTOR;
        latMod =
            -0.00349674 * lat - 0.00021492 * (lat ^ 2) + 1.00500000974457868175;
        diff = lat - averageLat;
        lat = lat + diff * latMod;

        if (lat > 90) {
            lat = 90;
        } else if (lat < -90) {
            lat = -90;
        }
        return lat;
    },
    lonToX: function (lon) {
        return lon * this.CONVERSION_FACTOR;
    },
    xToLon: function (x, averageLon) {
        lon = x / this.CONVERSION_FACTOR;
        diff = lon - averageLon;
        lon = lon + diff * 1;

        if (lon > 180) {
            lon = 180;
        } else if (lon < -180) {
            lon = -180;
        }
        return lon;
    },
    transformElements: function (elements) {
        return elements.map((e) => {
            if (e.data.hasOwnProperty('lat')) {
                return {
                    data: e.data,
                    position: {
                        y: this.latToY(e.data.lat),
                        x: this.lonToX(e.data.lon),
                    },
                };
            }
            return e;
        });
    },
};

window.dash_clientside.clientside = {
    updateLeafBounds: function (cyExtent) {
        return cyExtent;
    },
    updateLeafBoundsAIO: function (cyExtent, averageCoor) {
        if (!cyExtent) {
            return window.dash_clientside.no_update;
        }
        var utils = window.dash_clientside.utils;
        var bounds = [
            [
                utils.yToLat(cyExtent.y2, averageCoor.averageLat),
                utils.xToLon(cyExtent.x1, averageCoor.averageLon),
            ],
            [
                utils.yToLat(cyExtent.y1, averageCoor.averageLat),
                utils.xToLon(cyExtent.x2, averageCoor.averageLon),
            ],
        ];
        return bounds;
    },
    transformElements: function (elements) {
        return window.dash_clientside.utils.transformElements(elements);
    },
};
