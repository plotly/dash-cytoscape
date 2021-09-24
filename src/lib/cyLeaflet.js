export default class cyLeaflet {
    constructor(cy) {
        this.updateCtxmenu = this.update.bind(this);
        this.initializeLeaflet = this.initializeLeaflet.bind(this);
        this.generateContainerStyle = this.generateContainerStyle.bind(this);
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
        if(this.leafletInstance) {
            this.leafletInstance.destroy();
            clearInterval(this.leafletContainerUpdateInterval);
        }
        if(leafletHashNew !== this.leafletHash && leafletHashNew) {
            this.initializeLeaflet();
            this.addLeafletTiles(props);
            this.leafletHash = leafletHashNew;
        }
    }

    generateContainerStyle() {
        if(this.cy) {
            const {top, left, height, width} = this.cy.container().getBoundingClientRect();
            return `position: fixed; z-index: 0; top: ${top}px; left: ${left}px; height: ${height}px; width: ${width}px;`;
        }
        else {
            return '';
        }
    }

    initializeLeaflet() {
        if(!this.leafletContainer) {
            this.leafletContainer = document.createElement('div');
            this.leafletContainer.setAttribute('class', 'cy-leaflet-container');
            this.leafletContainer.setAttribute('style', this.generateContainerStyle());
            this.cy.container().style.zIndex = 1;
            this.cy.container().parentNode.appendChild(this.leafletContainer);

            this.leafletContainerUpdateInterval = setInterval(() => {
                this.leafletContainer.setAttribute('style', this.generateContainerStyle());
            }, 200);
        }
    }

    addLeafletTiles(props) {
        const { map, defaultTileLayer, L } = this.leafletInstance;
        const { tileUrl, attribution, maxZoom, preset, latitudeId, longitudeId } = props.leaflet;

        this.leafletInstance = this.cy.leaflet({
            container: this.leafletContainer,
            latitude: latitudeId || 'lat',
            longitude: longitudeId || 'lon',
        });

        if(preset) {
            map.removeLayer(defaultTileLayer);

            L.tileLayer.provider(preset).addTo(map);
        } else if(tileUrl) {
            map.removeLayer(defaultTileLayer);

            L.tileLayer(tileUrl, { attribution, maxZoom }).addTo(map);
        } 
        // otherwise use ext default

    }
}