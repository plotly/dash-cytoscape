function objectSubsectionMatch(obj, matchObj) {
    return !Object.keys(matchObj).some(matchKey =>
        typeof matchObj[matchKey] === 'object'
            ? !objectSubsectionMatch(obj[matchKey], matchObj[matchKey])
            : obj[matchKey] !== matchObj[matchKey]
    );
}

function ctxmenuTransformJson(data, shape) {
    // if shape is empty then just return data
    if(typeof shape !== 'object') {
        return data;
    }

    return shape.map(matchItem =>
            typeof matchItem === 'object' ? matchItem : {key: matchItem}
        )
        .reduce((acc, property) => {
            const {key, props, filter} = property;

            if(data[key] === undefined) {
                // do nothing
            }
            if(typeof property.props === 'object') {
                if(data[key].constructor === Array) {
                    acc[key] = data[key].map(arrItem => {
                        if(typeof filter === 'object') {
                            if(objectSubsectionMatch(arrItem, filter)) {
                                return ctxmenuTransformJson(arrItem, props);
                            }
                        }
                        else {
                            return ctxmenuTransformJson(arrItem, props);
                        }
                    })
                        .filter(arrItem =>
                            arrItem !== undefined
                        );
                }
                else {
                    acc[key] = ctxmenuTransformJson(data[key], props);
                }
            }
            else {
                acc[property.key] = data[property.key];
            }

            return acc;
        }, {});
}



export default class cyCtxMenu {

    constructor(cy) {
        this.ctxmenuUpdate = this.ctxmenuUpdate.bind(this);
        this.ctxmenuTranformProps = this.ctxmenuTranformProps.bind(this);

        this.ctxmenuHashtable = {};
        this.cy = cy;
        this.setProps = null;
    }

    ctxmenuUpdate(props) {
        const {ctxmenu, setProps} = props;
        this.setProps = setProps;

        if(typeof ctxmenu !== 'object' || ctxmenu.length === 0 || !this.cy || !this.cy.cxtmenu) {
            return;
        }

        // take all ctxmenu objects from props and hash them
        // compare props hash to hash list to find new hashes
        let ctxmenuNew = [];
        let ctxmenuHashCurrent = {};
        ctxmenu.map(ctxmenuObj => {
            let ctxmenuHash = JSON.stringify(ctxmenuObj);

            if(!this.ctxmenuHashtable[ctxmenuHash]) {
                ctxmenuNew.push(ctxmenuHash);
            }

            ctxmenuHashCurrent[ctxmenuHash] = true;
        });

        // delete removed ctxmenus
        Object.keys(this.ctxmenuHashtable).map(ctxmenuHash => {
            if(!ctxmenuHashCurrent[ctxmenuHash]) {
                this.ctxmenuHashtable[ctxmenuHash].destroy();
                delete this.ctxmenuHashtable[ctxmenuHash];
            }
        });

        // initialize new ctxmenus and add object from cy to ctxmenu hash table
        ctxmenuNew.map(ctxmenuHash => {
            this.ctxmenuHashtable[ctxmenuHash] = this.cy.cxtmenu(
                this.ctxmenuTranformProps(ctxmenuHash)
            );
        });
    }

    ctxmenuTranformProps(ctxmenuStr) {
        let ctxmenu = JSON.parse(ctxmenuStr);

        for(let i = 0; i < ctxmenu.commands.length; i++) {
            ctxmenu.commands[i].select = ele => {
                if(typeof this.setProps === 'function') {
                    this.setProps({
                        ctxmenuData: {
                            id: ctxmenu.commands[i].id,
                            data: ctxmenuTransformJson(ele.json(), ctxmenu.commands[i].format),
                            timestamp: Date.now()
                        }
                    });
                }
            }
        }

        return ctxmenu;
    }
}
