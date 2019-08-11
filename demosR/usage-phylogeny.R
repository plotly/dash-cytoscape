library(dash)
library(dashHtmlComponents)
library(dashCytoscape)
library(XML)

app <- Dash$new()

result <- xmlParse(file = "demos/data/apaf.xml")
# print(typeof(result))

tree <- xmlToList(result)
# print(typeof(tree))
str(tree)

layout <- list('name' = 'preset')

stylesheet <- list(
  list(
    'selector' = '.nonterminal',
    'style' = list(
      'label' = 'data(confidence)',
      'background-opacity' = 0,
      "text-halign" = "left",
      "text-valign" = "top"
    )
  ),
  list(
    'selector' = '.support',
    'style' = list('background-opacity' = 0)
  ),
  list(
    'selector' = 'edge',
    'style' = list(
      "source-endpoint" = "inside-to-node",
      "target-endpoint" = "inside-to-node"
    )
  ),
  list(
    'selector' = '.terminal',
    'style' = list(
      'label' = 'data(name)',
      'width' = 10,
      'height' = 10,
      "text-valign" = "center",
      "text-halign" = "right",
      'background-color' = '#222222'
    )
  )
)

app$layout(
  htmlDiv(
    list(
      cytoCytoscape(
        id = 'cytoscape',
        elements = list(), # change to 'elements' once defined
        stylesheet = stylesheet,
        layout = layout,
        style = list(
          'height' = '95vh',
          'width' = '100%'
        )
      )
    )
  )
)

app$callback(
  output = list(id = 'cytoscape', property = 'stylesheet'),
  params = list(
    input(id = 'cytoscape', property = 'mouseoverEdgeData')
  ),
  function(data) {
    if (is.null(data)) {
      return(stylesheet)
    }
    return(
      ""
    )
  }
)

#app$run_server()
