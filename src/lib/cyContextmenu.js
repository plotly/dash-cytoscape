function isUndefined(value1, value2) {
    return typeof value1 !== 'undefined' ? value1 : value2;
}

function containsCore(selectorStr) {
    return selectorStr.search('core') !== -1 || selectorStr === '*';
}

function removeCore(selectorStr) {
    return selectorStr
        .split(',')
        .map(str => str.trim())
        .filter(str => str !== 'core')
        .join(', ');
}

export default class cyContextmenu {
    constructor(cy) {
        this.initializeCxtmenu = this.initializeCxtmenu.bind(this);
        this.updateCtxmenu = this.update.bind(this);
        this.addCxtMenuItem = this.addBilkentCxtmenuItem.bind(this);
        this.populateBilkentCxtmenu = this.populateBilkentCxtmenu.bind(this);

        this.cy = cy;
        this.contextmenuHash = '';
        this.setProps = null;
        this.bilkentInstance = null;
    }

    update(props) {
        const {setProps, contextmenu} = props;
        this.setProps = setProps;

        if(typeof contextmenu !== 'object' || !this.cy || !this.cy.contextMenus) {
            return;
        }

        const contextmenuHashNew = JSON.stringify(contextmenu);
        if(contextmenuHashNew !== this.contextmenuHash) {
            this.initializeCxtmenu();
            this.populateBilkentCxtmenu(contextmenu);
            this.contextmenuHash = contextmenuHashNew;
        }
    }

    initializeCxtmenu() {
        if(this.bilkentInstance) {
            this.bilkentInstance.destroy();
        }

        this.bilkentInstance = this.cy.contextMenus({
            evtType: 'cxttap',
            menuItems: [],
        });
    }

    populateBilkentCxtmenu(contextmenuList) {
        contextmenuList.forEach(contextmenuItem => this.addBilkentCxtmenuItem(contextmenuItem));
    }

    addBilkentCxtmenuItem(contextmenuItem) {
        const {id, content, tooltipText, selector, disabled} = contextmenuItem;

        this.bilkentInstance.appendMenuItem({
            id,
            selector: removeCore(isUndefined(selector, '*')),
            content: isUndefined(content, 'Menu Item'),
            tooltipText: isUndefined(tooltipText, ''),
            disabled: isUndefined(disabled, false),
            coreAsWell: containsCore(isUndefined(selector, '')),
            onClickFunction: e => {
                const leaf = this.cy.scratch('leaf');
                const contextmenuData = {
                    id,
                    timestamp: e.timeStamp,
                    position: e.position,
                    target: e.target.json(),
                    coordinates: undefined,
                };
                if(leaf) {
                    const ll = leaf.map.containerPointToLatLng(leaf.L.point([e.position.x, e.position.y]));
                    contextmenuData.coordinates = [ll.lat, ll.lng];
                }
                this.setProps({ contextmenuData });
            }
        });
    }
}