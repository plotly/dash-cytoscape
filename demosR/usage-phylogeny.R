library(dash)
library(dashHtmlComponents)
library(dashCytoscape)
# library(XML)
# library(methods)
# library(ape)
# library(rphyloxml)

app <- Dash$new()

# result <- xmlParse(file = "demosR/data/apaf.xml")
# print(result)

# xml_file <- system.file("phyloxml/amphibian_tree_of_life_Frost_DR_2006.xml", package="rphyloxml")
# xml_tree <- read_phyloxml(xml_file)
# print(xml_tree)

layout <- list('name' = 'preset')

stylesheet <- list(
  list(
    'selector' = '.nonterminal',
    'style' = list(
      'label' = 'data(confidence)',
      'background-opacity' = 0,
      "text-halign" = "left",
      "text-valign" = "top",
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
      "target-endpoint" = "inside-to-node",
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
        elements = elements,
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

app$run_server()
