# Dash Cytoscape [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/plotly/dash-cytoscape/blob/master/LICENSE) [![PyPi Version](https://img.shields.io/pypi/v/dash-cytoscape.svg)](https://pypi.org/project/dash-cytoscape/)

A Component Library for Dash aimed at facilitating network visualization in Python, wrapped around [Cytoscape.js](http://js.cytoscape.org/).

Interacting with the stylesheet:
![usage-stylesheet-demo](https://raw.githubusercontent.com/plotly/dash-cytoscape/master/demos/images/usage-stylesheet-demo.gif)

Interacting with the elements:
![usage-elements-demo](https://raw.githubusercontent.com/plotly/dash-cytoscape/master/demos/images/usage-elements-demo.gif)

## Getting Started

### Prerequisites

Make sure that the following python packages are installed:

```
dash==0.35.1
dash-renderer==0.14.3
dash-html-components==0.13.4
dash-core-components==0.42.1
```

Older versions are not necessarily incompatible, but have not been extensively tested.

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


## Documentation

View the [Dash Cytoscape User Guide](https://dash.plot.ly/cytoscape/) to get started now. You can also use the [component reference](https://dash.plot.ly/cytoscape/reference/) to find how to use a certain feature.

To learn more about the core Dash components and how to use callbacks, view the [Dash documentation](https://dash.plot.ly/).

For supplementary information about the underlying Javascript  API, view the [Cytoscape.js documentation](http://js.cytoscape.org/).

## Development

Please follow the following steps for local testing:

1. Clone the repo
```commandline
$ git clone https://github.com/plotly/dash-cytoscape.git
```
2. In order to run the Python builds (`npm run build:py`) you need to create a 
venv for this project. Make sure you have `virtualenv` correctly installed and run this:
```commandline
$ mkdir dash_cytoscape_dev
$ cd dash_cytoscape_dev
$ virtualenv venv  # Create a virtual env
$ source venv/bin/activate  # Activate the venv
```

To activate in windows:
```commandline
> venv\Scripts\activate
```
(and then repeat step 3).

3. Install the JavaScript dependencies and build the code:
```commandline
$ yarn
$ yarn run build:all
```

4. Install the library
```commandline
$ python setup.py install
```



## Notes

#### Package manager
Our preferred package manager for this project is Yarn. Therefore we use `yarn.lock` rather than `package-lock.json`. If you decide to start using npm for package management (which will create package-lock.json) and you commit this project to Dokku, make sure to delete `yarn.lock`.


## License

Dash, Cytoscape.js and Dash Cytoscape are licensed under MIT. Please view [LICENSE](LICENSE) for more details.

## Contact and Support

See https://plot.ly/dash/support for ways to get in touch.

## Acknowledgments

Huge thanks to the Cytoscape Consortium and the Cytoscape.js team for their contribution in making such a complete API for creating interactive networks. This library would not have been possible without their massive work!

The Pull Request and Issue Templates were inspired from the
[]scikit-learn project](https://github.com/scikit-learn/scikit-learn).
