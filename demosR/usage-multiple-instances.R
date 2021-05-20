# original demo: http://js.cytoscape.org/demos/multiple-instances/

library(dash)
library(dashCytoscape)
library(jsonlite)

app <- Dash$new()

# define data
elements <- list(
  list('data' = list('id' = 'a', 'foo' = 3, 'bar' = 5, 'baz' = 7)),
  list('data' = list('id' = 'b', 'foo' = 6, 'bar' = 1, 'baz' = 3)),
  list('data' = list('id' = 'c', 'foo' = 2, 'bar' = 3, 'baz' = 6)),
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
        id = 'cytoscape-top',
        elements = elements,
        layout = list(
          'name' = 'circle',
          'padding' = 10
        ),
        stylesheet = list(
          list(
            'selector' = 'node',
            'style' = list(
              'background-color' = '#B3767E',
              'width' = 'mapData(baz, 0, 10, 10, 40)',
              'height' = 'mapData(baz, 0, 10, 10, 40)',
              'content' = 'data(id)'
            )
          ),
          list(
            'selector' = 'edge',
            'style' = list(
              'line-color' = '#F2B1BA',
              'target-arrow-color' = '#F2B1BA',
              'width' = 2,
              'target-arrow-shape' = 'circle',
              'opacity' = 0.8
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
          'height' = '50%',
          'position' = 'absolute',
          'background-color' = '#FAEDEF',
          'left' = 0,
          'top' = 0
        )
      ),
      cytoCytoscape(
        id = 'cytoscape-bottom',
        elements = elements,
        layout = list(
          'name' = 'breadthfirst',
          'directed' = TRUE,
          'padding' = 10
        ),
        stylesheet = list(
          list(
            'selector' = 'node',
            'style' = list(
              'background-color' = '#6272A3',
              'shape' = 'rectangle',
              'width' = 'mapData(foo, 0, 10, 10, 30)',
              'height' = 'mapData(bar, 0, 10, 10, 50)',
              'content' = 'data(id)'
            )
          ),
          list(
            'selector' = 'edge',
            'style' = list(
              'width' = 'mapData(weight, 0, 10, 3, 9)',
              'line-color' = '#B1C1F2',
              'target-arrow-color' = '#B1C1F2',
              'target-arrow-shape' = 'triangle',
              'opacity' = 0.8
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
          'height' = '50%',
          'position' = 'absolute',
          'background-color' = '#EDF1FA',
          'left' = 0,
          'top' = '50%',
          'border-top' = '1px solid #ccc'
        )
      )
    )
  )
)

app$run_server(debug = TRUE)
