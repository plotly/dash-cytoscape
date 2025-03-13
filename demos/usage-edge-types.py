"""
Original Demo: http://js.cytoscape.org/demos/edge-types/

Note: This example is broken because layout takes a function as input:
```
  layout: {
    name: 'grid',
    cols: 4,
    sort: function( a, b ){
      if( a.id() < b.id() ){
        return -1;
      } else if( a.id() > b.id() ){
        return 1;
      } else {
        return 0;
      }
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


with open("data/edge-types/data.json", "r", encoding="utf-8") as f:
    elements = json.loads(f.read())

with open("data/edge-types/cy-style.json", "r", encoding="utf-8") as f:
    stylesheet = json.loads(f.read())


# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            boxSelectionEnabled=False,
            autounselectify=True,
            elements=elements,
            layout={"name": "grid", "col": 4},
            stylesheet=stylesheet,
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
