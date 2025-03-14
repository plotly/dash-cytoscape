"""
Original Demo: http://js.cytoscape.org/demos/concentric-layout/

Note: This example is broken because layout takes a function as input, i.e.
```
  layout: {
    name: 'concentric',
    concentric: function( node ){
      return node.degree();
    },
    levelWidth: function( nodes ){
      return 2;
    }
  },
```

"""
import json

import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


# Load Data
with open("data/concentric-layout/data.json", "r", encoding="utf-8") as f:
    elements = json.loads(f.read())

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            layout={
                "name": "concentric",
            },
            stylesheet=[
                {
                    "selector": "node",
                    "style": {"height": 20, "width": 20, "background-color": "#30c9bc"},
                },
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "haystack",
                        "haystack-radius": 0,
                        "width": 5,
                        "opacity": 0.5,
                        "line-color": "#a8eae5",
                    },
                },
            ],
            style={
                "width": "100%",
                "height": "100%",
                "position": "absolute",
                "left": 0,
                "top": 0,
                "z-index": 999,
            },
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
