# original demo: http://js.cytoscape.org/demos/compound-nodes/
#

library(dash)
library(dashCytoscape)

app <- Dash$new()

# define data
elements <- list(
  list('data' = list('id' = 'a', 'parent' = 'b'), 'position' = list('x' = 215, 'y' = 85)),
  list('data' = list('id' = 'b')),
  list('data' = list('id' = 'c', 'parent' = 'b'), 'position' = list('x' = 300, 'y' = 85)),
  list('data' = list('id' = 'd'), 'position' = list('x' = 215, 'y' = 175)),
  list('data' = list('id' = 'e')),
  list('data' = list('id' = 'f', 'parent' = 'e'), 'position' = list('x' = 300, 'y' = 175)),
  list('data' = list('id' = 'ad', 'source' = 'a', 'target' = 'd')),
  list('data' = list('id' = 'eb', 'source' = 'e', 'target' = 'b'))
)

# define app layout
app$layout(
  htmlDiv(
    list(
      cytoCytoscape(
        id = 'cytoscape',
        elements = elements,
        boxSelectionEnabled = FALSE,
        autounselectify = TRUE,
        layout = list(
          'name' = 'preset',
          'padding' = 5
        ),
        stylesheet = list(
          list(
            'selector' = 'node',
            'style' = list(
              'content' = 'data(id)',
              'text-valign' = 'center',
              'text-halign' = 'center'
            )
          ),
          list(
            'selector' = '$node > node',
            'style' = list(
              'padding-top' = '10px',
              'padding-left' = '10px',
              'padding-bottom' = '10px',
              'padding-right' = '10px',
              'text-valign' = 'top',
              'text-halign' = 'center',
              'background-color' = '#bbb'
            )
          ),
          list(
            'selector' = ':selected',
            'style' = list(
              'background-color' = 'black',
              'line-color' = 'black',
              'target-arrow-color' = 'black',
              'source-arrow-color' = 'black'
            )
          ),
          list(
            'selector' = 'edge',
            'style' = list(
              'target-arrow-shape' = 'triangle'
            )
          )
        ),
        style = list(
          'width' = '100%',
          'height' = '100%',
          'position' = 'absolute',
          'left' = 0,
          'top' = 0
        )
      )
    )
  )
)

app$run_server(debug = TRUE)
