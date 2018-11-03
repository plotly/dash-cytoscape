import dash
from demos.editor.layout import layout as cytoscape_layout

from demos.editor.callbacks import assign_callbacks

app = dash.Dash(__name__)
server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True


app.layout = cytoscape_layout
assign_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)
