# original demo: http://js.cytoscape.org/demos/circle-layout/

library(dash)
library(dashCytoscape)
library(jsonlite)

app <- Dash$new()

# load data
elements <- fromJSON("demos/data/circle-layout/data.json")

# define app layout
app$layout(
  htmlDiv(
    list(
      cytoCytoscape(
        id = 'cytoscape',
        elements = elements,
        layout = list('name' = 'circle'),
        stylesheet = list(
          list(
            'selector' = 'node',
            'style' = list(
              'height' = 20,
              'width' = 20,
              'background-color' = '#e8e406'
            )
          ),
          list(
            'selector' = 'edge',
            'style' = list(
              'curve-style' = 'haystack',
              'haystack-radius' = 0,
              'width' = 5,
              'opacity' = 0.5,
              'line-color' = '#f2f08c'
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
