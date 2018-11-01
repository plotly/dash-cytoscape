import dash_cytoscape
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

try:
    from Bio import Phylo
except ModuleNotFoundError as e:
    print(e, "Please make sure you have biopython installed correctly before running this example.")


def generate_elements(tree):
    elements = []

    def _add_to_elements(clade, clade_id):
        children = clade.clades

        cy_source = {"data": {"id": clade_id}, 'classes': 'nonterminal'}
        elements.append(cy_source)

        if clade.is_terminal():
            cy_source['data']['name'] = clade.name
            cy_source['classes'] = 'terminal'

        for n, child in enumerate(children, 1):
            child_id = len(elements) + n

            cy_edge = {'data': {
                'source': clade_id,
                'target': child_id,
                'length': clade.branch_length
            }}

            if clade.confidence and clade.confidence.value:
                cy_source['data']['confidence'] = clade.confidence.value

            elements.extend([cy_edge])

            _add_to_elements(child, child_id)

    _add_to_elements(tree.clade, 0)

    return elements


# Define elements, stylesheet and layout
tree = Phylo.read('data/apaf.xml', 'phyloxml')
elements = generate_elements(tree)

layout = {
    'name': 'breadthfirst',
    'directed': True
}

stylesheet = [
    {
        'selector': '.nonterminal',
        'style': {
            'label': 'data(confidence)',
            'background-opacity': 0,
            "text-halign": "left",
            "text-valign": "top",
        }
    },
    {
        'selector': 'edge',
        'style': {
            "source-endpoint": "outside-to-node",
        }
    },
    {
        'selector': '.terminal',
        'style': {
            'label': 'data(name)',
            "shape": "roundrectangle",
            "width": 115,
            "height": 25,
            "text-valign": "center",
            'background-color': 'white',
            "border-width": 1.5,
            "border-style": "solid",
            "border-opacity": 1,
        }
    }
]


# Start the app
app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True


app.layout = html.Div([
    dash_cytoscape.Cytoscape(
        id='cytoscape',
        elements=elements,
        stylesheet=stylesheet,
        layout=layout,
        style={
            'height': '95vh',
            'width': '100%'
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
