# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.4] - 2018-01-19

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
