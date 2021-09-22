export default class cyLeaflet {
    constructor(cy) {
        this.updateCtxmenu = this.update.bind(this);
        this.initializeLeaflet = this.initializeLeaflet.bind(this);

        this.cy = cy;
        this.setProps = null;
        this.leafletContainer = null;
        this.leafletInstance = null;
        this.leafletHash = '';
    }

    update(props) {
        const {setProps, leaflet} = props;
        this.setProps = setProps;
        if(typeof leaflet !== 'object' || !this.cy || !this.cy.leaflet) {
            return;
        }

        const leafletHashNew = JSON.stringify(leaflet);
        if(leafletHashNew !== this.leafletHash) {
            this.initializeLeaflet();
            this.addLeafletTiles(props);
            this.leafletHash = leafletHashNew;
        }
    }

    initializeLeaflet() {
        if(this.leafletInstance) {
            this.leafletInstance.destroy();

        }

        if(!this.leafletContainer) {
            this.leafletContainer = document.createElement('div');
            this.leafletContainer.setAttribute('class', 'cy-leaflet-container');
            this.leafletContainer.setAttribute('style', 'right: 0; bottom: 0; position: absolute; left: 0px; top: 0px; z-index: 0;');
            this.cy.container().style.zIndex = 1;
            this.cy.container().parentNode.appendChild(this.leafletContainer);
        }
    }

    addLeafletTiles(props) {
        this.leafletInstance = this.cy.leaflet({
            container: this.leafletContainer,
            latitude: 'lat',
            longitude: 'lon',
        });

        this.leafletInstance.map.removeLayer(this.leafletInstance.defaultTileLayer);

        this.leafletInstance.L.tileLayer(
            props.leaflet.tileUrl || 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png',
            {
                attribution: props.leaflet.attribution,
                maxZoom: props.leaflet.maxZoom,
            },
        ).addTo(this.leafletInstance.map);
    }
}