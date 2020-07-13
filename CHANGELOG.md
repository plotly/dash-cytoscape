# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 20120-07-09

### Added
* Contributed initial build of R package.
* Added access to cytoscape.js PNG and JPG image generation API through `generateImage` and
  `imageData` properties (PR [#88](https://github.com/plotly/dash-cytoscape/pull/88)).
* Added ability to download image files generated with `generateImage` client-side without sending 
  data to the server (PR [#88](https://github.com/plotly/dash-cytoscape/pull/88)).
* Used the newly added `generateImage` and `imageData` properties to enable svg generation using [cytoscape-svg](https://github.com/kinimesi/cytoscape-svg).
* Added responsive cytoscape.js graph feature toggled using the `responsive` property (PR [#93](https://github.com/plotly/dash-cytoscape/pull/92)).
* One new demo:
    * `demos/usage-responsive-graph.py`: Example of graph with the ability to toggle the responsive feature on and off.
    * `demos/usage-image-export.py`: Shows how to export images as JPG, PNG or SVG.

### Changed
* Changed the official package manager from `yarn` to `npm`.
* `utils.Tree`: v0.1.1 broke compatibility with Python 2. Therefore, modified code to be compatible
  with Python 2. Added `props` and `edge_props` properties to accept arguments passed directly to
  the node's and edge's dictionaries, respectively (e.g., 'classes', 'positions', etc.).
* Removed `Tree`'s method `add_child`, because it is redundant with `add_children` called with an
  argument of length 1.
* `setup.py`: Remove `dash-html-components` and `dash_renderer` from `install_requires`.
* `usage-events.py`: Fix the size of the cytoscape graph to 500px by 500px.
* Upgrade `react-cytoscape.js` to latest.

### Fixed
* `setup.py`: Use `packages=find_packages(include=[package_name, package_name + ".*"])` so that all 
  subpackages like `utils` will be included when you `pip install dash-cytoscape`.
* Issue where `dash-cytoscape` cannot read property of 'length' of undefined when elements is not specified.
* `tests.test_interactions`.

## [0.1.1] - 2019-04-05

### Fixed
* Error where `dash_cytoscape.utils` cannot be imported.

## [0.1.0] - 2019-04-05

### Added
* Four new demos:
    * `demos/usage-dag-edges.py`: Example of edges in a directed acyclic graph (DAG). It uses the new `dash_cytoscape.utils.Tree` class.
    * `demos/usage-elements-extra.py`: Example of loading external layouts.
    * `demos/usage-preset-animation.py`: Example of animating nodes using the preset layout.
    * `demos/usage-reset-button.py`: Example of resetting the graph position using a button.
    * `demos/usage-remove-selected-elements.py`: Example to show how to remove selected elements with button.
* `dash_cytoscape/dash_cytoscape_extra.[min|dev].js`: New bundles containing the extra layouts. Those bundles are double in size compared to the default bundles. Therefore, they are only loaded when the user uses `load_extra_layouts()` to limit bandwidth usage and maximize loading speed. Please view [fast3g-cytoscape](demos/images/fast3g-cytoscape.PNG) for an example of the impact on loading time.
* `dash_cytoscape._display_default_values()`: A helper function to display the default prop values by reading `metadata.json`. Useful for documentation.
* `dash_cytoscape.load_extra_layouts()`: A function that can be called before initializing the Dash app (`app = dash.Dash(__name__)`) to load the JS bundle containing the external layouts.
* `src/lib/extra_index.js`: Loads external layouts before exporting the `Cytoscape` class. Needed to generate the new bundles.
* `webpack.[dev|prod].extra.config.js`: Two new webpack config files for external layouts.
* Images of new external layouts.
* The ability for the user to feed a dictionary with keys `nodes` and `edges` to the `elements` prop of `Cytoscape`, instead of a list. The values corresponding to these keys will be, respectively, lists of nodes and edges in the graph.


### Changed
* `usage-events.py`: Added IDs for the edges in order to pass Percy tests.
* `src/lib/components/Cytoscape.react.js`: Updated component docstring to include information about new external layouts and a warning about nodes that can't be modified by a callback. Added more default props for a better expected behavior.
* `package.json`: Added new builds for the extra layouts, modified `npm build:all` to include new builds. Added external layouts as dependencies.
* `MANIFEST.in`: Included new `dash_cytoscape.[min|dev].js` files.
* `README.md`: Moved images, added more images at the end, added useful links.


### Fixed
* Removing selected elements will now cause the corresponding JSON data to be cleared. Fixed by [PR #49](https://github.com/plotly/dash-cytoscape/pull/49), fixes [issue #45](https://github.com/plotly/dash-cytoscape/issues/45).


## [0.0.5] - 2019-03-08

### Added
* Two new demos: `usage-grid-social-network.py` and `usage-concentric-social-network.py`
* Add Issue and PR templates for Github (located in `.github`)
* `tests.test_usage`: Tests for rendering usage files.
* `tests.test_callbacks`: Tests for updating `Cytoscape` with callbacks.
* `tests.test_interactions`: Tests for interacting with `Cytoscape`, and evaluating its event callbacks.
* `tests.test_percy_snapshot`: Creates a Percy build using screenshots from other tests.

### Changed
* `usage-*.py`: Modified all the import statements from `import dash_cytoscape` to `import dash_cytoscape as cyto`. Optimized imports. They are now linted with pylint/flake8.
* `demos/usage-*`: Formatted all demo apps in order to respect pylint and flake8.
* `usage-phylogeny.py`: Clear callback conditional statement
* `CONTRIBUTING.md`: changed `dash-cytoscape-0.0.1` to `dash-cytoscape-x.x.x`. Added a **Code quality & design** section. Changed the **Making a contribution** section and updated title to **Publishing**. Updated **Pre-Release checklist**. Added the **Development** section from `README.md` (renamed **Setting up the environment**). Added a **Tests** section.
* `npmignore`: Added `venv` to avoid venvs to be included in the npm distribution package, which makes us a large amount of space and many unnecessary files being distributed.
* `config.yml`: Added steps to run the new tests. Added coverage for Python 3.7. Included `demos` and all usage examples in `pylint` and `flake8`. Increased line limit to 100.
* `README.md`: Moved the **Development** section to `CONTRIBUTING.md`. Modified the dash version in **Prerequisites**.
* `requirements.txt`: Updated the dash version to latest.
* `tests/requiremens.txt`: Updated the dash version to latest.
* `package.json`: Removed `"prepublish": "npm run validate-init"` due to conflict with CircleCI build. This script will be deprecated in favor of the upcoming Dash Component CLI.
* `tests/IntegrationTests.py`: Moved the `percy_snapshot` method to `test_percy_snapshot` in order to avoid duplicate (failing) builds on Percy. Decrease the number of processes to 1.
* `setup.py`: Added classifiers and download_url.

### Removed
* `extract-meta.js`, `extract-meta` - they were moved to the dash component CLI, thus are not needed anymore
* `config.py`, `runtime.txt`, `Procfile`, `index.html` - only needed for hosting `usage-*.py` on DDS, they are now moved to `plotly/dash-cytoscape-demos`.
* `review_checklist.md` -  redundant since all the information is already contained in CONTRIBUTING.md
* `tests.test_render`: Removed unused test


## [0.0.4] - 2019-01-19

### Added
* Homepage URL for PyPi
* Long Description for PyPi

### Changed
* Cytoscape component docstring for thorough and well-formatted references (#26)
* Refactored code base to match the up-to-date version of `dash-component-boilerplate` (#27)

### Fixed
* Console error where `setProps` gets called even when it is undefined (# 28)
* Incorrect setProps assignment that causes `setProps` to not be properly defined when nested in bigger apps (e.g. `dash-docs`) (#28)

## [0.0.3] - 2018-12-29
### Added
* Detailed usage example for rendering Biopython's Phylo object (phylogeny trees)
into a Cytoscape graph, with interactive features such as highlighting.

### Updated
* React-Cytoscapejs version, from 1.0.1 to 1.1.0 

## [0.0.2] - 2018-11-08
### Added
* Author email and improve description
* Data section of demos readme
* Added the components "dash", "dash-html-components", and "dash-renderer" as explicit package requirements.

### Changed
* Move grid layout data file
* Change App.js react demo data to be local
* Installation steps in readme to use yarn


### Updated
* Cytoscape.js version, correct component import

### Fixed
* Correct unpkg link error
* Markdown formatting for CONTRIBUTING.md


## [0.0.1] - 2018-11-03
### Added
- First pre-release version of dash-cytoscape. Still WIP, so prepare to see it break 🔧
