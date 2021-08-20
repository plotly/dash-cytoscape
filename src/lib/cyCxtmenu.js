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

export default class cyCxtmenu {
    constructor(cy) {
        this.initializeCxtmenu = this.initializeCxtmenu.bind(this);
        this.updateCtxmenu = this.update.bind(this);
        this.addCxtMenuItem = this.addBilkentCxtmenuItem.bind(this);
        this.populateBilkentCxtmenu = this.populateBilkentCxtmenu.bind(this);

        this.cy = cy;
        this.cxtmenuHash = '';
        this.setProps = null;
        this.bilkentInstance = null;
    }

    update(props) {
        const {setProps, cxtmenu} = props;
        this.setProps = setProps;

        if(typeof cxtmenu !== 'object' || !this.cy || !this.cy.contextMenus) {
            return;
        }

        const cxtmenuHashNew = JSON.stringify(cxtmenu);
        if(cxtmenuHashNew !== this.cxtmenuHash) {
            this.initializeCxtmenu();
            this.populateBilkentCxtmenu(cxtmenu);
            this.cxtmenuHash = cxtmenuHashNew;
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

    populateBilkentCxtmenu(cxtmenuList) {
        cxtmenuList.forEach(cxtmenuItem => this.addBilkentCxtmenuItem(cxtmenuItem));
    }

    addBilkentCxtmenuItem(cxtmenuItem) {
        const {id, content, tooltipText, selector, disabled} = cxtmenuItem;

        this.bilkentInstance.appendMenuItem({
            id,
            selector: removeCore(isUndefined(selector, '*')),
            content: isUndefined(content, 'Menu Item'),
            tooltipText: isUndefined(tooltipText, ''),
            disabled: isUndefined(disabled, false),
            coreAsWell: containsCore(isUndefined(selector, '')),
            onClickFunction: e => {
                this.setProps({
                    cxtmenuData: {
                        id,
                        timestamp: e.timeStamp,
                        position: e.position,
                        target: e.target.json(),
                    }
                })
            }
        });
    }
}