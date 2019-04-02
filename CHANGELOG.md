# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
* `demos/usage-dag-edges.py`: Show different types of edges in a DAG
* `demos/usage-elements-extra.py`: Shows how to load external layouts, otherwise same app as `usage-elements.py`.
* `demos/usage-preset-animation.py`: Example of animating nodes using the preset layout.
* `demos/usage-reset-button.py`: Example of resetting the graph position using a button.
* `dash_cytoscape.load_extra_layouts()`: A new function that can be called before initializing the Dash app (`app = dash.Dash(__name__)`) to load the JS bundle containing the external layouts. 
* `webpack.[dev|prod].extra.config.js`: Two new webpack configs for external layouts.
* `src/lib/extra_index.js`: Loads external layouts before exporting the `Cytoscape` class. Needed to generate the new bundles.
* Images of new external layouts.
* `dash_cytoscape/dash_cytoscape_extra.[min|dev].js`: New bundles containing the extra layouts. Those bundles are double in size compared to the default bundles. Therefore, they are only loaded when the user uses `load_extra_layouts()` to limit bandwidth usage and maximize loading speed. Please view [fast3g-cytoscape](demos/images/fast3g-cytoscape.PNG) for an example of the impact on loading time.
* `dash_cytoscape._display_default_values()`: A util function to display the default prop values by reading `metadata.json`. Useful for documentation.

### Changed
* `usage-events.py`: Added IDs for the edges in order to pass Percy tests.
* `src/lib/components/Cytoscape.react.js`: Updated docstring to include information about new external layouts and warning about nodes that can't be modified by a callback. Added more default props for a better expected behavior.
* `package.json`: Added new builds for the extra layouts, modified `npm build:all` to include new builds. Added external layouts as dependencies.
* `README.md`: Moved images, added more images at the end, added useful links.


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
