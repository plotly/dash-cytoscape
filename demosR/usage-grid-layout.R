# original demo: http://js.cytoscape.org/demos/grid-layout/

library(dash)
library(dashCytoscape)
library(jsonlite)

app <- Dash$new()

# load data
elements <- fromJSON("demos/data/grid-layout/data.json")

# define app layout
app$layout(
  htmlDiv(
    list(
      cytoCytoscape(
        id = 'cytoscape',
        elements = elements,
        layout = list('name' = 'grid'),
        stylesheet = list(
          list(
            'selector' = 'node',
            'style' = list(
              'height' = 20,
              'width' = 20,
              'background-color' = '#18e018'
            )
          ),
          list(
            'selector' = 'edge',
            'style' = list(
              'curve-style' = 'haystack',
              'haystack-radius' = 0,
              'width' = 5,
              'opacity' = 0.5,
              'line-color' = '#a2efa2'
            )
          )
        ),
        style = list(
          'width' = '100%',
          'height' = '100%',
          'position' = 'absolute',
          'left' = 0,
          'top' = 0,
          'z-index' = 999
        )
      )
    )
  )
)

app$run_server(debug = TRUE)
