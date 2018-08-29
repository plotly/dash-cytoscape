import dash

from cytoscape.callbacks import serve_callbacks
from cytoscape.layout import layout as cytoscape_layout

app = dash.Dash(__name__)
server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True


app.layout = cytoscape_layout
serve_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)
