# original demo: http://js.cytoscape.org/demos/images-breadthfirst-layout/
#
# note: click animation is not implemented

library(dash)
library(dashCytoscape)
library(jsonlite)

app <- Dash$new()

# define data
elements <- list(
  list('data' = list('id' = 'cat')),
  list('data' = list('id' = 'bird')),
  list('data' = list('id' = 'ladybug')),
  list('data' = list('id' = 'aphid')),
  list('data' = list('id' = 'rose')),
  list('data' = list('id' = 'grasshopper')),
  list('data' = list('id' = 'plant')),
  list('data' = list('id' = 'wheat')),
  list('data' = list('source' = 'cat', 'target' = 'bird')),
  list('data' = list('source' = 'bird', 'target' = 'ladybug')),
  list('data' = list('source' = 'bird', 'target' = 'grasshopper')),
  list('data' = list('source' = 'grasshopper', 'target' = 'plant')),
  list('data' = list('source' = 'grasshopper', 'target' = 'wheat')),
  list('data' = list('source' = 'ladybug', 'target' = 'aphid')),
  list('data' = list('source' = 'aphid', 'target' = 'rose'))
)

# define stylesheet
stylesheet <- list(
  list(
    'selector' = 'node',
    'style' = list(
      'height' = 80,
      'width' = 80,
      'background-fit' = 'cover',
      'border-color' = '#000',
      'border-width' = 3,
      'border-opacity' = 0.5
    )
  ),
  list(
    'selector' = 'edge',
    'style' = list(
      'curve-style' = 'bezier',
      'width' = 6,
      'target-arrow-shape' = 'triangle',
      'line-color' = '#ffaaaa',
      'target-arrow-color' = '#ffaaaa'
    )
  ),
  list(
    'selector' = '#bird',
    'style' = list(
      'background-image' = 'https://farm8.staticflickr.com/7272/7633179468_3e19e45a0c_b.jpg'
    )
  ),
  list(
    'selector' = '#cat',
    'style' = list(
      'background-image' = 'https://farm2.staticflickr.com/1261/1413379559_412a540d29_b.jpg'
    )
  ),
  list(
    'selector' = '#ladybug',
    'style' = list(
      'background-image' = 'https://farm4.staticflickr.com/3063/2751740612_af11fb090b_b.jpg'
    )
  ),
  list(
    'selector' = '#aphid',
    'style' = list(
      'background-image' = 'https://farm9.staticflickr.com/8316/8003798443_32d01257c8_b.jpg'
    )
  ),
  list(
    'selector' = '#rose',
    'style' = list(
      'background-image' = 'https://farm6.staticflickr.com/5109/5817854163_eaccd688f5_b.jpg'
    )
  ),
  list(
    'selector' = '#grasshopper',
    'style' = list(
      'background-image' = 'https://farm7.staticflickr.com/6098/6224655456_f4c3c98589_b.jpg'
    )
  ),
  list(
    'selector' = '#plant',
    'style' = list(
      'background-image' = 'https://farm1.staticflickr.com/231/524893064_f49a4d1d10_z.jpg'
    )
  ),
  list(
    'selector' = '#wheat',
    'style' = list(
      'background-image' = 'https://farm3.staticflickr.com/2660/3715569167_7e978e8319_b.jpg'
    )
  )
)

# define app layout
app$layout(
  htmlDiv(
    list(
      cytoCytoscape(
        id = 'cytoscape',
        elements = elements,
        stylesheet = stylesheet,
        layout = list(
          'name' = 'breadthfirst',
          'directed' = TRUE,
          'padding' = 10
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
