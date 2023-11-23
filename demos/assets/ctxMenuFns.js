window.dashCytoscapeFunctions = Object.assign(
    {},
    window.dashCytoscapeFunctions,
    {
        add_2_nodes: function (event) {
            var pos = event.position || event.cyPosition;
            cy.add({
                data: {
                    group: 'nodes',
                    id: Date.now(),
                },
                position: {
                    x: pos.x,
                    y: pos.y,
                },
            });
            cy.add({
                data: {
                    group: 'nodes',
                    id: `${Date.now()}_2`,
                },
                position: {
                    x: pos.x + 50,
                    y: pos.y + 50,
                },
            });
        },
    }
);
