could you make a Dash app that is similar to our editor in http://plot.ly/create/?

basically:
- The Graph on the left side of the screen
- On the right side of the screen, a control panel
- In that control panel, enumerate through:
-  the `style` properties here: http://js.cytoscape.org/#style
-  `layout` properties here: http://js.cytoscape.org/#layouts
- `instantiation` properies here: http://js.cytoscape.org/#core/initialisation
- the `elements` properties here: http://js.cytoscape.org/#notation/elements-json

it’ll eventually serve as our documentation
sort of like “interactive documentation”

and then we can even have an output tab that prints out the input arguments as JSON

we could have them as JSON imports in some type of top-level dropdown
similar to here: https://plotly.github.io/react-chart-editor/
(the “Select mock” dropdown at the bottom of the page)

so, i’d start with just a few properties from each section (`layouts`, `style`, `elements`) and create a simple app and put that in a PR
and then I can review your structure
and then we can go at it and fill the rest of the stuff out

we can also use that app as our test suite - we’ll select different options and take screenshots

let’s first start to explore the API and make sure that editing these things work
and by exploring the API, I mean doing so through a sample app
i.e. spend 3-5 days on that
and then once that is de-risked, we’ll start looking into the event system