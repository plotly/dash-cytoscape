library(dash)
library(dashCytoscape)
library(jsonlite)

app <- Dash$new()

# define elements
basic_elements <- list(
  list(
    'data' = list('id' = 'one', 'label' = 'Node 1'),
    'position' = list('x' = 50, 'y' = 50)
  ),
  list(
    'data' = list('id' = 'two', 'label' = 'Node 2'),
    'position' = list('x' = 200, 'y' = 200)
  ),
  list(
    'data' = list('id' = 'three', 'label' = 'Node 3'),
    'position' = list('x' = 100, 'y' = 150)
  ),
  list(
    'data' = list('id' = 'four', 'label' = 'Node 4'),
    'position' = list('x' = 400, 'y' = 50)
  ),
  list(
    'data' = list('id' = 'five', 'label' = 'Node 5'),
    'position' = list('x' = 250, 'y' = 100)
  ),
  list(
    'data' = list('id' = 'six', 'label' = 'Node 6', 'parent' = 'three'),
    'position' = list('x' = 150, 'y' = 150)
  ),
  list(
    'data' = list(
      'id' = 'one-two',
      'source' = 'one',
      'target' = 'two',
      'label' = 'Edge from Node1 to Node2'
    )
  ),
  list(
    'data' = list(
      'id' = 'one-five',
      'source' = 'one',
      'target' = 'five',
      'label' = 'Edge from Node 1 to Node 5'
    )
  ),
  list(
    'data' = list(
      'id' = 'two-four',
      'source' = 'two',
      'target' = 'four',
      'label' = 'Edge from Node 2 to Node 4'
    )
  ),
  list(
    'data' = list(
      'id' = 'three-five',
      'source' = 'three',
      'target' = 'five',
      'label' = 'Edge from Node 3 to Node 5'
    )
  ),
  list(
    'data' = list(
      'id' = 'three-two',
      'source' = 'three',
      'target' = 'two',
      'label' = 'Edge from Node 3 to Node 2'
    )
  ),
  list(
    'data' = list(
      'id' = 'four-four',
      'source' = 'four',
      'target' = 'four',
      'label' = 'Edge from Node 4 to Node 4'
    )
  ),
  list(
    'data' = list(
      'id' = 'four-six',
      'source' = 'four',
      'target' = 'six',
      'label' = 'Edge from Node 4 to Node 6'
    )
  ),
  list(
    'data' = list(
      'id' = 'five-one',
      'source' = 'five',
      'target' = 'one',
      'label' = 'Edge from Node 5 to Node 1'
    )
  )
)

styles <- list(
  'json-output' = list(
    'overflow-y' = 'scroll',
    'height' = 'calc(50% - 25px)',
    'border' = 'thin lightgrey solid'
  ),
  'tab' = list(
    'height' = 'calc(98vh - 115px)'
  )
)

# define app layout
app$layout(
  htmlDiv(
    list(
      htmlDiv(
        className = 'eight columns',
        children = list(
          cytoCytoscape(
            id = 'cytoscape',
            elements = basic_elements,
            layout = list(
              'name' = 'preset'
            ),
            style = list(
              'height' = '95vh',
              'width' = '100%'
            )
          )
        )
      ),
      htmlDiv(
        className = 'four columns',
        children = list(
          dccTabs(
            id = 'tabs',
            children = list(
              dccTab(
                label = 'Tap Objects',
                children = list(
                  htmlDiv(
                    style = styles[['tab']],
                    children = list(
                      htmlP('Node Object JSON:'),
                      htmlPre(
                        id = 'tap-node-json-output',
                        style = styles[['json-output']]
                      ),
                      htmlP('Edge Object JSON:'),
                      htmlPre(
                        id = 'tap-edge-json-output',
                        style = styles[['json-output']]
                      )
                    )
                  )
                )
              ),
              dccTab(
                label = 'Tap Data',
                children = list(
                  htmlDiv(
                    style = styles[['tab']],
                    children = list(
                      htmlP('Node Data JSON:'),
                      htmlPre(
                        id = 'tap-node-data-json-output',
                        style = styles[['json-output']]
                      ),
                      htmlP('Edge Data JSON:'),
                      htmlPre(
                        id = 'tap-edge-data-json-output',
                        style = styles[['json-output']]
                      )
                    )
                  )
                )
              ),
              dccTab(label = 'Mouseover Data', children = list(
                  htmlDiv(
                    style = styles[['tab']],
                    children = list(
                      htmlP('Node Data JSON:'),
                      htmlPre(
                        id = 'mouseover-node-data-json-output',
                        style = styles[['json-output']]
                      ),
                      htmlP('Edge Data JSON:'),
                      htmlPre(
                        id = 'mouseover-edge-data-json-output',
                        style = styles[['json-output']]
                      )
                    )
                  )
                )
              ),
              dccTab(
                label = 'Selected Data',
                children = list(
                  htmlDiv(
                    style = styles[['tab']],
                    children = list(
                      htmlP('Node Data JSON:'),
                      htmlPre(
                        id = 'selected-node-data-json-output',
                        style = styles[['json-output']]
                      ),
                      htmlP('Edge Data JSON:'),
                      htmlPre(
                        id = 'selected-edge-data-json-output',
                        style = styles[['json-output']]
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
  )
)

# define callbacks
app$callback(
  output = list(id = 'tap-node-json-output', property = 'children'),
  params = list(input(id = 'cytoscape', property = 'tapNode')),
  function(data) {
    return(toJSON(data, pretty = TRUE, null = 'null'))
  }
)
app$callback(
  output = list(id = 'tap-edge-json-output', property = 'children'),
  params = list(input(id = 'cytoscape', property = 'tapEdge')),
  function(data) {
    return(toJSON(data, pretty = TRUE, null = 'null'))
  }
)
app$callback(
  output = list(id = 'tap-node-data-json-output', property = 'children'),
  params = list(input(id = 'cytoscape', property = 'tapNodeData')),
  function(data) {
    return(toJSON(data, pretty = TRUE, null = 'null'))
  }
)
app$callback(
  output = list(id = 'tap-edge-data-json-output', property = 'children'),
  params = list(input(id = 'cytoscape', property = 'tapEdgeData')),
  function(data) {
    return(toJSON(data, pretty = TRUE, null = 'null'))
  }
)
app$callback(
  output = list(id = 'mouseover-node-data-json-output', property = 'children'),
  params = list(input(id = 'cytoscape', property = 'mouseoverNodeData')),
  function(data) {
    return(toJSON(data, pretty = TRUE, null = 'null'))
  }
)
app$callback(
  output = list(id = 'mouseover-edge-data-json-output', property = 'children'),
  params = list(input(id = 'cytoscape', property = 'mouseoverEdgeData')),
  function(data) {
    return(toJSON(data, pretty = TRUE, null = 'null'))
  }
)
app$callback(
  output = list(id = 'selected-node-data-json-output', property = 'children'),
  params = list(input(id = 'cytoscape', property = 'selectedNodeData')),
  function(data) {
    return(toJSON(data, pretty = TRUE, null = 'null'))
  }
)
app$callback(
  output = list(id = 'selected-edge-data-json-output', property = 'children'),
  params = list(input(id = 'cytoscape', property = 'selectedEdgeData')),
  function(data) {
    return(toJSON(data, pretty = TRUE, null = 'null'))
  }
)

app$run_server()
