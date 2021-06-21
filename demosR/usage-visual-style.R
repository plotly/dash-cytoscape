# original demo: http://js.cytoscape.org/demos/visual-style/
#
# note: animation has not been implemented yet, please refer to code.
library(dash)
library(dashCytoscape)

app <- Dash$new()

# define elements
elements <- list(
  list('data' = list('id' = 'j', 'name' = 'Jerry', 'weight' = 65, 'faveColor' = '#6FB1FC', 'faveShape' = 'triangle')),
  list('data' = list('id' = 'e', 'name' = 'Elaine', 'weight' = 45, 'faveColor' = '#EDA1ED', 'faveShape' = 'ellipse')),
  list('data' = list('id' = 'k', 'name' = 'Kramer', 'weight' = 75, 'faveColor' = '#86B342', 'faveShape' = 'octagon')),
  list('data' = list('id' = 'g', 'name' = 'George', 'weight' = 70, 'faveColor' = '#F5A45D', 'faveShape' = 'rectangle')),
  list('data' = list('source' = 'j', 'target' = 'e', 'faveColor' = '#6FB1FC', 'strength' = 90)),
  list('data' = list('source' = 'j', 'target' = 'k', 'faveColor' = '#6FB1FC', 'strength' = 70)),
  list('data' = list('source' = 'j', 'target' = 'g', 'faveColor' = '#6FB1FC', 'strength' = 80)),
  list('data' = list('source' = 'e', 'target' = 'j', 'faveColor' = '#EDA1ED', 'strength' = 95)),
  list('data' = list('source' = 'e', 'target' = 'k', 'faveColor' = '#EDA1ED', 'strength' = 60), 'classes' = 'questionable'),
  list('data' = list('source' = 'k', 'target' = 'j', 'faveColor' = '#86B342', 'strength' = 100)),
  list('data' = list('source' = 'k', 'target' = 'e', 'faveColor' = '#86B342', 'strength' = 100)),
  list('data' = list('source' = 'k', 'target' = 'g', 'faveColor' = '#86B342', 'strength' = 100)),
  list('data' = list('source' = 'g', 'target' = 'j', 'faveColor' = '#F5A45D', 'strength' = 90))
)

# define app layout
app$layout(
  htmlDiv(
    list(
      cytoCytoscape(
        id = 'cytoscape',
        elements = elements,
        layout = list(
          'name' = 'cose',
          'padding' = 10
        ),
        stylesheet = list(
          list(
            'selector' = 'node',
            'style' = list(
              'shape' = 'data(faveShape)',
              'width' = 'mapData(weight, 40, 80, 20, 60)',
              'content' = 'data(name)',
              'text-valign' = 'center',
              'text-outline-width' = 2,
              'text-outline-color' = 'data(faveColor)',
              'background-color' = 'data(faveColor)',
              'color' = '#fff'
            )
          ),
          list(
            'selector' = 'edge',
            'style' = list(
              'curve-style' = 'bezier',
              'opacity' = 0.666,
              'width' = 'mapData(strength, 70, 100, 2, 6)',
              'target-arrow-shape' = 'triangle',
              'source-arrow-shape' = 'circle',
              'line-color' = 'data(faveColor)',
              'source-arrow-color' = 'data(faveColor)',
              'target-arrow-color' = 'data(faveColor)'
            )
          ),
          list(
            'selector' = ':selected',
            'style' = list(
              'border-width' = 3,
              'border-color' = '#333'
            )
          ),
          list(
            'selector' = 'edge.questionable',
            'style' = list(
              'line-style' = 'dotted',
              'target-arrow-shape' = 'diamond'
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
