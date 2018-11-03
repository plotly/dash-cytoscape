# Contributing to Dash Cytoscape

## Getting Started

Refer to the [readme](README.md) for installation and development instructions.

## Coding Style

Please lint any additions to Python code with `pylint` and `flake8`.

## Pull Request Guidelines

Use the [GitHub flow][] when proposing contributions to this repository (i.e. create a feature branch and submit a PR against the master branch).

## Running the Tests

_To be added_


## Making a contribution
_For larger features, your contribution will have a higher likelihood of getting merged if you create an issue to discuss the changes that you'd like to make before you create a pull request._

Create a pull request and tag the Plotly team (`@plotly/dash_bio`) and tag / request review from [@xhlulu](https://github.com/xhlulu).

After a review has been done and your changes have been approved, create a prerelease and comment in the PR. Version numbers should follow [semantic versioning][].

To publish or create a prerelease:

1. Check `MANIFEST.in` has all of the extra files (like CSS)
2. Bump version numbers in `package.json`, update the `CHANGELOG.md`, and make a pull request
3. Once the pull request is merged into master:
4. Build
```npm run build:all```
5. Create distribution tarball
```python setup.py sdist```
6. Copy the tarball into a separate folder and try to install it and run the examples:
```cp dist/dash-cytoscape-0.0.1.tar.gz ../temp
cp usage.py ../temp
cd ../temp
source venv/bin/activate
pip install dash-cytoscape-0.0.1.tar.gz
python usage.py
```
7. If the examples work, then publish:
```npm publish
twine upload dist/dash-cytoscape-0.0.1.tar.gz
```
8. Tag your release with git:
```git tag -a 'v0.0.1' -m 'v0.0.1'
git push origin master --follow-tags
```
9. Verify that the publish worked by installing it:
```cd ../temp
pip install dash-cytoscape==0.0.1
python usage.py
```


Make a post in the [Dash Community Forum][]
    * Title it `":mega: Announcement! New <Your Feature> - Feedback Welcome"`
    * In the description, link to the PR and any relevant issue(s)
    * Pin the topic so that it appears at the top of the forum for two weeks

## [Checklists](http://rs.io/unreasonable-effectiveness-of-checklists/)
**Beginner tip:** _Copy and paste this section as a comment in your PR, then check off the boxes as you go!_
### Pre-Merge checklist
- [ ] If changes are significant, a release candidate has been created and posted to Slack, the Plotly forums, and at the very top of the pull request.
- [ ] Two people have :dancer:'d the pull request. You can be one of these people if you are a Dash core contributor.

### Post-Merge checklist
- [ ] You have tagged the release using `git tag v<version_number>` _(for the contributor merging the PR)_.
- [ ] You have pushed this tag using `git push <tag_name>` _(for the contributor merging the PR)_.
- [ ] You have deleted the branch.

### Pre-Release checklist
- [ ] Everything in the Pre-Merge checklist is completed. (Except the last two if this is a release candidate).
- [ ] `git remote show origin` shows you are in the correct repository.
- [ ] `git branch` shows that you are on the expected branch.
- [ ] `git status` shows that there are no unexpected changes.
- [ ] `dash/version.py` is at the correct version.

### Release Step
- `python setup.py sdist` to build.
- `twine upload dist/<the_version_you_just_built>` to upload to PyPi.

### Post-Release checklist
- [ ] You have closed all issues that this pull request solves, and commented the new version number users should install.
- [ ] If significant enough, you have created an issue about documenting the new feature or change and you have added it to the [Documentation] project.
- [ ] You have created a pull request in [Dash Docs] with the new release of your feature by editing that project's [`requirements.txt` file](https://github.com/plotly/dash-docs/blob/master/requirements.txt) and you have assigned `@chriddyp` to review.

## Financial Contributions

Dash, and many of Plotly's open source products, have been funded through direct sponsorship by companies. [Get in touch] about funding feature additions, consulting, or custom app development.

[Dash Core Components]: https://dash.plot.ly/dash-core-components
[Dash HTML Components]: https://github.com/plotly/dash-html-components
[write your own components]: https://dash.plot.ly/plugins
[Dash Component Biolerplate]: https://github.com/plotly/dash-component-boilerplate
[issues]: https://github.com/plotly/dash-core-components/issues 
[GitHub flow]: https://guides.github.com/introduction/flow/
[eslintrc-react.json]: https://github.com/plotly/dash-components-archetype/blob/master/config/eslint/eslintrc-react.json
[contributors]: https://github.com/plotly/dash-core-components/graphs/contributors
[semantic versioning]: https://semver.org/
[Dash Community Forum]: https://community.plot.ly/c/dash
[Confirmation Modal component]: https://github.com/plotly/dash-core-components/pull/211#issue-195280462
[Confirmation Modal announcement]: https://community.plot.ly/t/announcing-dash-confirmation-modal-feedback-welcome/11627
[Get in touch]: https://plot.ly/products/consulting-and-oem
[Documentation]: https://github.com/orgs/plotly/projects/8
[Dash Docs]: https://github.com/plotly/dash-docs
