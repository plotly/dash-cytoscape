# Dash Cytoscape [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/plotly/dash-cytoscape/blob/master/LICENSE) [![PyPi Version](https://img.shields.io/pypi/v/dash-cytoscape.svg)](https://pypi.org/project/dash-cytoscape/)

A Dash component library for creating interactive and customizable networks in Python, wrapped around [Cytoscape.js](http://js.cytoscape.org/).

![usage-stylesheet-demo](https://raw.githubusercontent.com/plotly/dash-cytoscape/master/demos/images/usage-stylesheet-demo.gif)

* 🌟 [Medium Article](https://medium.com/@plotlygraphs/introducing-dash-cytoscape-ce96cac824e4)
* 📣 [Community Announcement](https://community.plot.ly/t/announcing-dash-cytoscape/19095)
* 💻 [Github Repository](https://github.com/plotly/dash-cytoscape) 
* 📚 [User Guide](https://dash.plot.ly/cytoscape) 
* 🗺 [Component Reference](https://dash.plot.ly/cytoscape/reference)
* 📺 [Webinar Recording](https://www.youtube.com/watch?v=snXcIsCMQgk)

## Getting Started

### Prerequisites

Make sure that dash and its dependent libraries are correctly installed:
```commandline
pip install dash dash-html-components
```

If you want to install the latest versions, check out the [Dash docs on installation](https://dash.plot.ly/installation).


### Usage

Install the library using pip:

```
pip install dash-cytoscape
```

Create the following example inside an `app.py` file:

```python
import dash
import dash_cytoscape as cyto
import dash_html_components as html

app = dash.Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=[
            {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}},
            {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two','label': 'Node 1 to 2'}}
        ],
        layout={'name': 'preset'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

![basic-usage](https://raw.githubusercontent.com/plotly/dash-cytoscape/master/demos/images/basic-usage.gif)

### External layouts

You can also add external layouts. Use the `cyto.load_extra_layouts()` function to get started:

```python
import dash
import dash_cytoscape as cyto
import dash_html_components as html

cyto.load_extra_layouts()

app = dash.Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(...)
])
```

## Documentation

The [Dash Cytoscape User Guide](https://dash.plot.ly/cytoscape/) contains everything you need to know about the library. It contains useful examples, functioning code, and is fully interactive. You can also use the [component reference](https://dash.plot.ly/cytoscape/reference/) for a complete and concise specification of the API. 

To learn more about the core Dash components and how to use callbacks, view the [Dash documentation](https://dash.plot.ly/).

For supplementary information about the underlying Javascript  API, view the [Cytoscape.js documentation](http://js.cytoscape.org/).

## Contributing

Make sure that you have read and understood our [code of conduct](CODE_OF_CONDUCT.md), then head over to [CONTRIBUTING](CONTRIBUTING.md) to get started. 

## License

Dash, Cytoscape.js and Dash Cytoscape are licensed under MIT. Please view [LICENSE](LICENSE) for more details.

## Contact and Support

See https://plot.ly/dash/support for ways to get in touch.

## Acknowledgments

Huge thanks to the Cytoscape Consortium and the Cytoscape.js team for their contribution in making such a complete API for creating interactive networks. This library would not have been possible without their massive work!

The Pull Request and Issue Templates were inspired from the
[scikit-learn project](https://github.com/scikit-learn/scikit-learn).

## Gallery

Interacting with the [elements](usage-elements.py):
![usage-elements-demo](demos/images/usage-elements-demo.gif)

Using [external layouts](demos/usage-elements-extra.py):
![usage-elements-extra](demos/images/usage-elements-extra.gif)
