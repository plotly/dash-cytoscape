# Dash Component Skeleton

This repository contains the minimal set of code required to create your own custom Dash component.

To create your own Dash component:
1. Fork this repo
2. Find-and-replace:
    1. `my_dash_component` with your component library name.
    2. `my-dash-component` with your component library name.
    3. `my-name` with your name and `my-email` with your email address
    4. `my-license` with your license (e.g. `MIT`)
    5. Rename the folder `my_dash_component/` with your component library name
3. Install the dependencies:
```
npm install
```
4. Open up the JavaScript demo environment:
```
npm run start
```
5. Write your component code in `src/lib/components`. There is a sample component called `ExampleComponent.react.js` that you can use for inspiration. The demo app is in `src/demo` and you will import your example component code into your demo app.
6. Test your code in a Python environment:
    1. Build your code
    ```
    npm run build:js-dev
    npm run build:py
    ```
    2. Run and modify the `usage.py` sample dash app:
    ```
    python usage.py
    ```
7. Create a production build and publish:
    1. Build your code:
    ```
    npm run build:js
    npm run build:py
    ```
    2. Create a Python tarball
    ```
    python setup.py sdist
    ```
    This distribution tarball will get generated in the `dist/` folder
    3. Test your tarball by copying it into a new environment and installing it locally:
    ```
    pip install my_dash_component-0.0.1.tar.gz
    ```
    4. If it works, then you can publish the component to NPM and PyPI:
    ```
    npm run publish
    ```
    ```
    twine upload dist/dash_component-0.0.1.tar.gz
    ```
8. Share your component with the community! https://community.plot.ly/c/dash

# More details
- Include CSS files in your distribution folder (`my_dash_component`) and reference them in `MANIFEST.in`
- The `tests` folder contains a sample integration test. This will run a sample Dash app in a browser. Run this with:
    ```
    python -m tests.test_render
    ```
    The Dash team uses these types of integration tests extensively. Browse the Dash component code on GitHub for more examples of testing (e.g. https://github.com/plotly/dash-core-components)
- Publishing your component to NPM will make the JavaScript bundles available on the unpkg CDN. By default, Dash servers the component library's CSS and JS from the remote unpkg CDN, so if you haven't published the component package to NPM you'll need to set the `serve_locally` flags to `True`. We will eventually make `serve_locally=True` the default, [follow our progress in this issue](https://github.com/plotly/dash/issues/284).
- Watch the [component boilerplate repository](https://github.com/plotly/dash-component-boilerplate) to stay informed of changes to our components.


# More Resources
- Learn more about Dash: https://dash.plot.ly
- View the original component boilerplate: https://github.com/plotly/dash-component-boilerplate
