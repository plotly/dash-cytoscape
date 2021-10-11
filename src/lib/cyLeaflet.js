const DEFAULT_TILE_SIZE = 256;

export default class cyLeaflet {
    constructor(cy) {
        this.updateCtxmenu = this.update.bind(this);
        this.initializeLeaflet = this.initializeLeaflet.bind(this);
        this.addLeafletTiles = this.addLeafletTiles.bind(this);

        this.cy = cy;
        this.setProps = null;
        this.leafletContainer = null;
        this.leafletInstance = null;
        this.leafletHash = '';
        this.leafletViewHash = '';
        this.leafletContainerUpdateInterval = null;
    }

    update(props) {
        const {setProps, leaflet} = props;
        this.setProps = setProps;
        if(typeof leaflet !== 'object' || !this.cy || !this.cy.leaflet) {
            return;
        }

        const leafletHashNew = JSON.stringify(Object.assign(
            {},
            leaflet,
            {view: null}
        ));
        if(leafletHashNew !== this.leafletHash && leafletHashNew) {
            if(this.leafletInstance) {
                this.leafletInstance.destroy();
                this.leafletInstance = null;
            }

            if(this.leafletContainer) {
                this.leafletContainer.remove();
                this.leafletContainer = null;
            }

            this.initializeLeaflet();
            this.addLeafletTiles(props);
            this.leafletHash = leafletHashNew;
        }

        const leafletViewHashNew = JSON.stringify(leaflet.view);
        if(leafletViewHashNew !== this.leafletViewHash && leafletViewHashNew && leaflet.view.length >= 2) {
            this.leafletInstance.map.setView([leaflet.view[0], leaflet.view[1]], leaflet.view[2]);
        }
        this.leafletViewHash = leafletViewHashNew;
    }

    initializeLeaflet() {
        if(!this.leafletContainer) {
            this.leafletContainer = document.createElement('div');
            this.leafletContainer.setAttribute('class', 'cy-leaflet-container');
            this.leafletContainer.setAttribute('style', 'position: absolute; left: 0; top: 0; width: 100%; height: 100%; z-index: 0;');
            this.cy.container().style.zIndex = 1;
            this.cy.container().parentNode.appendChild(this.leafletContainer);
        }
    }

    addLeafletTiles(props) {
        const { tileUrl, attribution, maxZoom, zoomOffset, tileSize, provider, latitudeId, longitudeId } = props.leaflet;
        const { map, defaultTileLayer, L } = this.leafletInstance = this.cy.leaflet({
            container: this.leafletContainer,
            latitude: latitudeId || 'lat',
            longitude: longitudeId || 'lon',
        });

        if(provider) {
            map.removeLayer(defaultTileLayer);

            L.tileLayer.provider(provider).addTo(map);
        } else if(tileUrl) {
            map.removeLayer(defaultTileLayer);

            L.tileLayer(tileUrl, {
                attribution,
                maxZoom,
                zoomOffset: zoomOffset ? zoomOffset : 0,
                tileSize: tileSize ? tileSize : DEFAULT_TILE_SIZE,
            }).addTo(map);
        } 
        // otherwise use ext default
    }
}