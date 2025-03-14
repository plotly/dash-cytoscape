import dash
from dash import Input, Output, dcc, html, callback

import dash_cytoscape as cyto

# enable svg export
cyto.load_extra_layouts()

app = dash.Dash(__name__)
server = app.server

# Object declaration
basic_elements = [
    {"data": {"id": "one", "label": "Node 1"}, "position": {"x": 50, "y": 50}},
    {"data": {"id": "two", "label": "Node 2"}, "position": {"x": 200, "y": 200}},
    {"data": {"id": "three", "label": "Node 3"}, "position": {"x": 100, "y": 150}},
    {"data": {"id": "four", "label": "Node 4"}, "position": {"x": 400, "y": 50}},
    {"data": {"id": "five", "label": "Node 5"}, "position": {"x": 250, "y": 100}},
    {
        "data": {"id": "six", "label": "Node 6", "parent": "three"},
        "position": {"x": 150, "y": 150},
    },
    {
        "data": {
            "id": "one-two",
            "source": "one",
            "target": "two",
            "label": "Edge from Node1 to Node2",
        }
    },
    {
        "data": {
            "id": "one-five",
            "source": "one",
            "target": "five",
            "label": "Edge from Node 1 to Node 5",
        }
    },
    {
        "data": {
            "id": "two-four",
            "source": "two",
            "target": "four",
            "label": "Edge from Node 2 to Node 4",
        }
    },
    {
        "data": {
            "id": "three-five",
            "source": "three",
            "target": "five",
            "label": "Edge from Node 3 to Node 5",
        }
    },
    {
        "data": {
            "id": "three-two",
            "source": "three",
            "target": "two",
            "label": "Edge from Node 3 to Node 2",
        }
    },
    {
        "data": {
            "id": "four-four",
            "source": "four",
            "target": "four",
            "label": "Edge from Node 4 to Node 4",
        }
    },
    {
        "data": {
            "id": "four-six",
            "source": "four",
            "target": "six",
            "label": "Edge from Node 4 to Node 6",
        }
    },
    {
        "data": {
            "id": "five-one",
            "source": "five",
            "target": "one",
            "label": "Edge from Node 5 to Node 1",
        }
    },
]

styles = {
    "output": {
        "overflow-y": "scroll",
        "overflow-wrap": "break-word",
        "height": "calc(100% - 25px)",
        "border": "thin lightgrey solid",
    },
    "tab": {"height": "calc(98vh - 115px)"},
}


app.layout = html.Div(
    [
        html.Div(
            className="eight columns",
            children=[
                cyto.Cytoscape(
                    id="cytoscape",
                    elements=basic_elements,
                    layout={"name": "preset"},
                    style={
                        "height": "95vh",
                        "width": "calc(100% - 500px)",
                        "float": "left",
                    },
                )
            ],
        ),
        html.Div(
            className="four columns",
            children=[
                dcc.Tabs(
                    id="tabs",
                    children=[
                        dcc.Tab(label="generate jpg", value="jpg"),
                        dcc.Tab(label="generate png", value="png"),
                    ],
                ),
                html.Div(
                    style=styles["tab"],
                    children=[
                        html.Div(
                            id="image-text",
                            children="image data will apear hear",
                            style=styles["output"],
                        )
                    ],
                ),
                html.Div("Download graph:"),
                html.Button("as jpg", id="btn-get-jpg"),
                html.Button("as png", id="btn-get-png"),
                html.Button("as svg", id="btn-get-svg"),
            ],
        ),
    ]
)


@callback(
    Output("image-text", "children"),
    Input("cytoscape", "imageData"),
)
def put_image_string(data):
    return data


@callback(
    Output("cytoscape", "generateImage"),
    Input("tabs", "value"),
    Input("btn-get-jpg", "n_clicks"),
    Input("btn-get-png", "n_clicks"),
    Input("btn-get-svg", "n_clicks"),
)
def get_image(tab, get_jpg_clicks, get_png_clicks, get_svg_clicks):
    # File type to ouput of 'svg, 'png', 'jpg', or 'jpeg' (alias of 'jpg')
    ftype = tab

    # 'store': Stores the image data in 'imageData' !only jpg/png are supported
    # 'download'`: Downloads the image as a file with all data handling
    # 'both'`: Stores image data and downloads image as file.
    action = "store"

    ctx = dash.callback_context
    if ctx.triggered:
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if input_id != "tabs":
            action = "download"
            ftype = input_id.split("-")[-1]

            # random print statement needed to pass pylint
            print(get_jpg_clicks, get_png_clicks, get_svg_clicks)

    return {"type": ftype, "action": action}


if __name__ == "__main__":
    app.run(debug=True)
