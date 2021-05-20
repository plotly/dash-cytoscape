# original demo: http://js.cytoscape.org/demos/pie-style/

library(dash)
library(dashCytoscape)
library(jsonlite)

app <- Dash$new()

# define data
elements <- list(
  list('data' = list('id' = 'a', 'foo' = 3, 'bar' = 5, 'baz' = 2)),
  list('data' = list('id' = 'b', 'foo' = 6, 'bar' = 1, 'baz' = 3)),
  list('data' = list('id' = 'c', 'foo' = 2, 'bar' = 3, 'baz' = 5)),
  list('data' = list('id' = 'd', 'foo' = 7, 'bar' = 1, 'baz' = 2)),
  list('data' = list('id' = 'e', 'foo' = 2, 'bar' = 3, 'baz' = 5)),
  list('data' = list('id' = 'ae', 'weight' = 1, 'source' = 'a', 'target' = 'e')),
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
          'name' = 'circle',
          'padding' = 10
        ),
        stylesheet = list(
          list(
            'selector' = 'node',
            'style' = list(
              'width' = '60px',
              'height' = '60px',
              'content' = 'data(id)',
              'pie-size' = '80%',
              'pie-1-background-color' = '#E8747C',
              'pie-1-background-size' = 'mapData(foo, 0, 10, 0, 100)',
              'pie-2-background-color' = '#74CBE8',
              'pie-2-background-size' = 'mapData(bar, 0, 10, 0, 100)',
              'pie-3-background-color' = '#74E883',
              'pie-3-background-size' = 'mapData(baz, 0, 10, 0, 100)'
            )
          ),
          list(
            'selector' = 'edge',
            'style' = list(
              'curve-style' = 'bezier',
              'width' = 4,
              'target-arrow-shape' = 'triangle',
              'opacity' = 0.5
            )
          ),
          list(
            'selector' = ':selected',
            'style' = list(
              'background-color' = 'black',
              'line-color' = 'black',
              'target-arrow-color' = 'black',
              'source-arrow-color' = 'black',
              'opacity' = 1
            )
          ),
          list(
            'selector' = '.faded',
            'style' = list(
              'opacity' = 0.25,
              'text-opacity' = 0
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
