"""
Original Demo: http://js.cytoscape.org/demos/initialisation/

Note: The click-and-drag functionality is broken in this Dash implementation
because the example requires a function referring to the "cy" property, i.e.
```
cy.on('tap', 'node', function(e){
  var node = e.cyTarget;
  var neighborhood = node.neighborhood().add(node);

  cy.elements().addClass('faded');
  neighborhood.removeClass('faded');
});

cy.on('tap', function(e){
  if( e.cyTarget === cy ){
    cy.elements().removeClass('faded');
  }
});
```
"""
import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


elements = [
    {"data": {"id": "j", "name": "Jerry"}},
    {"data": {"id": "e", "name": "Elaine"}},
    {"data": {"id": "k", "name": "Kramer"}},
    {"data": {"id": "g", "name": "George"}},
    {"data": {"source": "j", "target": "e"}},
    {"data": {"source": "j", "target": "k"}},
    {"data": {"source": "j", "target": "g"}},
    {"data": {"source": "e", "target": "j"}},
    {"data": {"source": "e", "target": "k"}},
    {"data": {"source": "k", "target": "j"}},
    {"data": {"source": "k", "target": "e"}},
    {"data": {"source": "k", "target": "g"}},
    {"data": {"source": "g", "target": "j"}},
]

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            boxSelectionEnabled=False,
            autounselectify=True,
            elements=elements,
            layout={"name": "grid", "padding": 10},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "content": "data(name)",
                        "text-valign": "center",
                        "color": "white",
                        "text-outline-width": 2,
                        "background-color": "#999",
                        "text-outline-color": "#999",
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "bezier",
                        "target-arrow-shape": "triangle",
                        "target-arrow-color": "#ccc",
                        "line-color": "#ccc",
                        "width": 1,
                    },
                },
                {
                    "selector": ":selected",
                    "style": {
                        "background-color": "black",
                        "line-color": "black",
                        "target-arrow-color": "black",
                        "source-arrow-color": "black",
                    },
                },
                {
                    "selector": "edge.questionable",
                    "style": {"line-style": "dotted", "target-arrow-shape": "diamond"},
                },
                {"selector": ".faded", "style": {"opacity": 0.25, "text-opacity": 0}},
            ],
            style={
                "width": "100%",
                "height": "100%",
                "position": "absolute",
                "left": 0,
                "top": 0,
            },
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
