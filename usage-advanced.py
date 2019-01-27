import dash

from demos.editor.callbacks import assign_callbacks
from demos.editor.layout import layout as cytoscape_layout

app = dash.Dash(__name__)
server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True


app.layout = cytoscape_layout
assign_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)
