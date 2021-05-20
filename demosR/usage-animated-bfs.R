# original demo: http://js.cytoscape.org/demos/animated-bfs/
# code: https://github.com/cytoscape/cytoscape.js/tree/master/documentation/demos/animated-bfs
#
# note: animation not implemented yet, please refer to code.

library(dash)
library(dashCytoscape)
library(jsonlite)

app <- Dash$new()

# define data
elements <- list(
  list('data' = list('id' = 'a')),
  list('data' = list('id' = 'b')),
  list('data' = list('id' = 'c')),
  list('data' = list('id' = 'd')),
  list('data' = list('id' = 'e')),
  list('data' = list('id' = 'a"e', 'weight' = 1, 'source' = 'a', 'target' = 'e')),
  list('data' = list('id' = 'ab', 'weight' = 3, 'source' = 'a', 'target' = 'b')),
  list('data' = list('id' = 'be', 'weight' = 4, 'source' = 'b', 'target' = 'e')),
  list('data' = list('id' = 'bc', 'weight' = 5, 'source' = 'b', 'target' = 'c')),
  list('data' = list('id' = 'ce', 'weight' = 6, 'source' = 'c', 'target' = 'e')),
  list('data' = list('id' = 'cd', 'weight' = 2, 'source' = 'c', 'target' = 'd')),
  list('data' = list('id' = 'de', 'weight' = 7, 'source' = 'd', 'target' = 'e'))
)

# define app layout
app$layout(
  htmlDiv(
    list(
      cytoCytoscape(
        id = 'cytoscape',
        elements = elements,
        layout = list(
          'name' = 'breadthfirst',
          'directed' = TRUE,
          'roots' = '#a',
          'padding' = 10
        ),
        stylesheet = list(
          list(
            'selector' = 'node',
            'style' = list(
              'content' = 'data(id)'
            )
          ), list(
            'selector' = 'edge',
            'style' = list(
              'curve-style' = 'bezier',
              'target-arrow-shape' = 'triangle',
              'width' = 4,
              'line-color' = '#ddd',
              'target-arrow-color' = '#ddd'
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
