window.dashCytoscapeComponentFunctions = {}

window.dashCytoscapeComponentFunctions.add_2_nodes = function (event) {
    var pos = event.position || event.cyPosition;
    cy.add({
        data: {
            group: 'nodes',
            id: Date.now(),
            // label: "Test Label"
        },
        position: {
            x: pos.x,
            y: pos.y
        }
    });
    cy.add({
        data: {
            group: 'nodes',
            id: `${Date.now()}_2`,
            // label: "Test Label 2"
        },
        position: {
            x: pos.x + 50,
            y: pos.y + 50
        }
    });

};