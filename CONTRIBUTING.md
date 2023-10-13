# Contributing to Dash Cytoscape

Thank you for your interesting in contributing to this open-source project! Make sure that you have read and understood our [code of conduct](CODE_OF_CONDUCT.md).

## Setting up the environment

Please follow the following steps for local testing:

1. Clone the repo

```commandline
git clone https://github.com/plotly/dash-cytoscape.git
```

2. In order to run the Python builds (`npm run build:all`) you need to create a
   venv for this project. Make sure you have `virtualenv` correctly installed and run this:

```commandline
mkdir dash_cytoscape_dev
cd dash_cytoscape_dev
virtualenv venv  # Create a virtual env
source venv/bin/activate  # Activate the venv
pip install -r requirements.txt  # Install the requirements
```

To activate in windows, replace the 4th line with this:

```commandline
venv\Scripts\activate
```

3. Install the JavaScript dependencies and build the code:

```commandline
npm install
npm run build:all
```

#### Package manager

Before v0.2.0, our preferred package manager for this project is Yarn. Starting with v0.2.0, we will be using `npm` in order to create less confusion and ensure a unified package manager with other Dash components. Therefore we use `package-lock.json` rather than `yarn.lock.`. If you are contributing a PR to dash-cytoscape, we encourage you to also use `npm`.

## Coding Style

Please lint any additions to Python and JS code with `pylint`, `flake8`, `black`, `eslint`, and `prettier`:

```commandline
npm run lint:all
```

## Code quality & design

-   Is your code clear? If you had to go back to it in a month, would you be happy to? If someone else had to contribute to it, would they be able to?

    A few suggestions:

    -   Make your variable names descriptive and use the same naming conventions throughout the code.

    -   For more complex pieces of logic, consider putting a comment, and maybe an example.

    -   In the comments, focus on describing _why_ the code does what it does, rather than describing _what_ it does. The reader can most likely read the code, but not necessarily understand why it was necessary.

    -   Don't overdo it in the comments. The code should be clear enough to speak for itself. Stale comments that no longer reflect the intent of the code can hurt code comprehension.

*   Don't repeat yourself. Any time you see that the same piece of logic can be applied in multiple places, factor it out into a function, or variable, and reuse that code.
*   Scan your code for expensive operations (large computations, DOM queries, React re-renders). Have you done your possible to limit their impact? If not, it is going to slow your app down.
*   Can you think of cases where your current code will break? How are you handling errors? Should the user see them as notifications? Should your app try to auto-correct them for them?

## Tests

### Running the tests

Activate your virtualenv:

```commandline
source venv/bin/activate
```

If needed, install the requirements:

```commandline
pip install -r tests/requirements.txt
```

Install ChromeDriver following the instructions [here (Mac)](https://www.kenst.com/2015/03/installing-chromedriver-on-mac-osx/) or [here (Windows)](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/). You must install the version of ChromeDriver that matches your Chrome version.

Run the tests using the following command:

```commandline
pytest --headless
```

Look inside the `tests/screenshots` directory to find the images created by the tests. If you have
Percy configured, run the following test:

```commandline
python -m unittest tests.test_percy_snapshot
```

### Percy

Make sure to configure your Percy environment variables correctly:

```commandline
PERCY_BRANCH=local
PERCY_ENABLED=1
PERCY_TOKEN=***************
```

You can find the token in the [project settings of the Percy project](https://percy.io/plotly/dash-cytoscape/settings). Only members of the Plotly organizations have access to this token.

### About the tests

The tests are broken down in 3 categories:

-   Callbacks: Tests if the `elements`, `stylesheet` and `layout` properties can be updated correctly by other Dash components using callbacks.
-   Interactions: Tests user interactions such as dragging, clicking, and hovering over nodes, as well as the associated event callbacks.
-   Usage: Tests if all of the usage apps render correctly on start. This does not test callbacks.

Those tests are rendered into images located inside `tests/screenshots`, which are then sent to a Percy build using `tests.test_percy_snapshot`, which creates a Dash app that only serves the content of `tests/screenshots` at different routes, which are then captured by the Percy runner.

## Publishing

Create a pull request and tag the Plotly team (`@plotly/dash-core`) and tag / request review from [@xhlulu](https://github.com/xhlulu).

After a review has been done and your changes have been approved, create a prerelease and comment in the PR. Version numbers should follow [semantic versioning][].

To publish or create a prerelease:

1. Check `MANIFEST.in` has all of the extra files (like CSS)
2. Bump version numbers in `package.json`, update the [CHANGELOG](CHANGELOG.md), and make a pull request
3. Once the pull request is merged into master:
4. Build

```
npm run build:all
```

5. Create distribution tarball

```
python setup.py sdist
```

6. Copy the tarball into a separate folder and try to install it and run the examples:

```
cp dist/dash_cytoscape-x.x.x.tar.gz ../temp
cp usage.py ../temp
cd ../temp
source venv/bin/activate
pip install dash_cytoscape-x.x.x.tar.gz
python usage.py
```

7. If the examples work, then publish:

```
npm publish
twine upload dist/dash_cytoscape-x.x.x.tar.gz
```

8. Tag your release with git:

```
git tag -a 'vx.x.x' -m 'vx.x.x'
git push origin master --follow-tags
```

9. Verify that the publish worked by installing it:

```
cd ../temp
pip install dash-cytoscape==x.x.x
python usage.py
```

Make a post in the [Dash Community Forum](https://community.plotly.com/c/dash)

-   Title it `":mega: Announcement! New <Your Feature> - Feedback Welcome"`
-   In the description, link to the PR and any relevant issue(s)
-   Pin the topic so that it appears at the top of the forum for two weeks

## [Checklists](http://rs.io/unreasonable-effectiveness-of-checklists/)

**Beginner tip:** _Copy and paste this section as a comment in your PR, then check off the boxes as you go!_

### Pre-Merge checklist

-   [ ] The project was correctly built with `npm run build:all`.
-   [ ] If there was any conflict, it was solved correctly
-   [ ] All changes were documented in CHANGELOG.md.
-   [ ] All tests on CircleCI have passed.
-   [ ] All Percy visual changes have been approved.
-   [ ] Two people have :dancer:'d the pull request. You can be one of these people if you are a Dash Cytoscape core contributor.

### Merge step

1. Make sure to _Squash and Merge_ your contribution if you have created multiple commits to change a specific feature.
2. Make sure to _Rebase and Merge_ if you added many different features, and need to contribute multiple different commits.

### Post-Merge checklist

-   [ ] You have tagged the release using `git tag v<version_number>` _(for the contributor merging the PR)_.
-   [ ] You have pushed this tag using `git push <tag_name>` _(for the contributor merging the PR)_.
-   [ ] You have deleted the branch.

### Pre-Release checklist

-   [ ] Everything in the Pre-Merge checklist is completed.
-   [ ] `git remote show origin` shows you are in the correct repository.
-   [ ] `git branch` shows that you are on the expected branch.
-   [ ] `git status` shows that there are no unexpected changes.
-   [ ] Both `package.json` and `dash_cytoscape/package.json` versions have been correctly updated.

### Release Step

Complete the "Publishing" section.

### Post-Release checklist

-   [ ] Step 1 and 2 of Post-merge checklist are completed.
-   [ ] You have closed all issues that this pull request solves, and commented the new version number users should install.
-   [ ] If significant enough, you have created an issue about documenting the new feature or change and you have added it to the [Documentation] project.
-   [ ] You have created a pull request in [Dash Docs] with the new release of your feature by editing that project's [`requirements.txt` file](https://github.com/plotly/dash-docs/blob/master/requirements.txt).

## Financial Contributions

Dash, and many of Plotly's open source products, have been funded through direct sponsorship by companies. [Get in touch](https://plotly.com/products/on-premise/) about funding feature additions, consulting, or custom app development.

[Dash Core Components]: https://dash.plotly.com/dash-core-components
[Dash HTML Components]: https://github.com/plotly/dash-html-components
[write your own components]: https://dash.plotly.com/plugins
[Dash Component Biolerplate]: https://github.com/plotly/dash-component-boilerplate
[issues]: https://github.com/plotly/dash-core-components/issues
[GitHub flow]: https://guides.github.com/introduction/flow/
[eslintrc-react.json]: https://github.com/plotly/dash-components-archetype/blob/master/config/eslint/eslintrc-react.json
[contributors]: https://github.com/plotly/dash-core-components/graphs/contributors
[semantic versioning]: https://semver.org/
[Dash Community Forum]: https://community.plotly.com/c/dash
[Confirmation Modal component]: https://github.com/plotly/dash-core-components/pull/211#issue-195280462
[Confirmation Modal announcement]: https://community.plotly.com/t/announcing-dash-confirmation-modal-feedback-welcome/11627
[Get in touch]: https://plotly.com/products/consulting-and-oem
[Documentation]: https://github.com/orgs/plotly/projects/8
[Dash Docs]: https://github.com/plotly/dash-docs
