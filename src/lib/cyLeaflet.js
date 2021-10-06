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
        this.leafletContainerUpdateInterval = null;
    }

    update(props) {
        const {setProps, leaflet} = props;
        this.setProps = setProps;
        if(typeof leaflet !== 'object' || !this.cy || !this.cy.leaflet) {
            return;
        }

        const leafletHashNew = JSON.stringify(leaflet);
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
            const defaultTileSize = 256;

            L.tileLayer(tileUrl, {
                attribution,
                maxZoom,
                zoomOffset: zoomOffset ? zoomOffset : 0,
                tileSize: tileSize ? tileSize : defaultTileSize,
            }).addTo(map);
        } 
        // otherwise use ext default

    }
}
