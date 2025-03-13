import dash

from demos.editor.callbacks import assign_callbacks
from demos.editor.layout import layout as cytoscape_layout

app = dash.Dash(__name__)
server = app.server

app.layout = cytoscape_layout
assign_callbacks()


if __name__ == "__main__":
    app.run(debug=True)
