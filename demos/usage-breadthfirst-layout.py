"""
Original Demo: http://js.cytoscape.org/demos/images-breadthfirst-layout/

Note: Click Animation is not implemented.
"""

import dash
from dash import html

import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server


elements = [
    {"data": {"id": "cat"}},
    {"data": {"id": "bird"}},
    {"data": {"id": "ladybug"}},
    {"data": {"id": "aphid"}},
    {"data": {"id": "rose"}},
    {"data": {"id": "grasshopper"}},
    {"data": {"id": "plant"}},
    {"data": {"id": "wheat"}},
    {"data": {"source": "cat", "target": "bird"}},
    {"data": {"source": "bird", "target": "ladybug"}},
    {"data": {"source": "bird", "target": "grasshopper"}},
    {"data": {"source": "grasshopper", "target": "plant"}},
    {"data": {"source": "grasshopper", "target": "wheat"}},
    {"data": {"source": "ladybug", "target": "aphid"}},
    {"data": {"source": "aphid", "target": "rose"}},
]

stylesheet = [
    {
        "selector": "node",
        "style": {
            "height": 80,
            "width": 80,
            "background-fit": "cover",
            "border-color": "#000",
            "border-width": 3,
            "border-opacity": 0.5,
        },
    },
    {
        "selector": "edge",
        "style": {
            "curve-style": "bezier",
            "width": 6,
            "target-arrow-shape": "triangle",
            "line-color": "#ffaaaa",
            "target-arrow-color": "#ffaaaa",
        },
    },
    {
        "selector": "#bird",
        "style": {
            "background-image": "https://farm8.staticflickr.com/7272/7633179468_3e19e45a0c_b.jpg"
        },
    },
    {
        "selector": "#cat",
        "style": {
            "background-image": "https://farm2.staticflickr.com/1261/1413379559_412a540d29_b.jpg"
        },
    },
    {
        "selector": "#ladybug",
        "style": {
            "background-image": "https://farm4.staticflickr.com/3063/2751740612_af11fb090b_b.jpg"
        },
    },
    {
        "selector": "#aphid",
        "style": {
            "background-image": "https://farm9.staticflickr.com/8316/8003798443_32d01257c8_b.jpg"
        },
    },
    {
        "selector": "#rose",
        "style": {
            "background-image": "https://farm6.staticflickr.com/5109/5817854163_eaccd688f5_b.jpg"
        },
    },
    {
        "selector": "#grasshopper",
        "style": {
            "background-image": "https://farm7.staticflickr.com/6098/6224655456_f4c3c98589_b.jpg"
        },
    },
    {
        "selector": "#plant",
        "style": {
            "background-image": "https://farm1.staticflickr.com/231/524893064_f49a4d1d10_z.jpg"
        },
    },
    {
        "selector": "#wheat",
        "style": {
            "background-image": "https://farm3.staticflickr.com/2660/3715569167_7e978e8319_b.jpg"
        },
    },
]

# App
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            stylesheet=stylesheet,
            layout={"name": "breadthfirst", "directed": True, "padding": 10},
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
