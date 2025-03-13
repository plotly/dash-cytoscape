"""
Original Demo: http://js.cytoscape.org/demos/labels/

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


elements = [
    {"data": {"label": "top left"}, "classes": "top-left"},
    {"data": {"label": "top center"}, "classes": "top-center"},
    {"data": {"label": "top right"}, "classes": "top-right"},
    {"data": {"label": "center left"}, "classes": "center-left"},
    {"data": {"label": "center center"}, "classes": "center-center"},
    {"data": {"label": "center right"}, "classes": "center-right"},
    {"data": {"label": "bottom left"}, "classes": "bottom-left"},
    {"data": {"label": "bottom center"}, "classes": "bottom-center"},
    {"data": {"label": "bottom right"}, "classes": "bottom-right"},
    {
        "data": {"label": "multiline manual\nfoo\nbar\nbaz"},
        "classes": "multiline-manual",
    },
    {"data": {"label": "multiline auto foo bar baz"}, "classes": "multiline-auto"},
    {"data": {"label": "outline"}, "classes": "outline"},
    {"data": {"id": "ar-src"}},
    {"data": {"id": "ar-tgt"}},
    {
        "data": {
            "source": "ar-src",
            "target": "ar-tgt",
            "label": "autorotate (move my nodes)",
        },
        "classes": "autorotate",
    },
    {"data": {"label": "background"}, "classes": "background"},
]

with open("labels/cy-style.json", "r", encoding="utf-8") as f:
    stylesheet = json.loads(f.read())

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            boxSelectionEnabled=False,
            autounselectify=True,
            elements=elements,
            layout={"name": "grid", "cols": 3},
            stylesheet=stylesheet,
            style={
                "width": "100%",
                "height": "100%",
                "position": "absolute",
                "left": 0,
                "top": 0,
                "bottom": 0,
                "right": 0,
                "z-index": 999,
            },
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
