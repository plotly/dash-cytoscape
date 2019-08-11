library(dash)
library(dashHtmlComponents)
library(dashCytoscape)
library(XML)

app <- Dash$new()

tree <- xmlToList(xmlParse(file = "demos/data/apaf.xml"))$phylogeny
capture.output(tree, file = "demosR/tree.txt", append = FALSE)

# nodes: 31 terminal, 31 support; 30 nonterminal, 29 support (root has no support)

generate_elements <- function(tree, xlen=30, ylen=30, grabbable=False) {
  organize_tree <- function(tree, terminals=list(), nonterminals=list(), i=list(), t=0, n=0) {

    explore_child <- function(child, id) {
      if (class(child) == "list") {
        if (!is.null(child$name)) {
          t <<- t+1
          id <- paste0(id, "c", i[[length(i)]])
          i[[length(i)]] <<- i[[length(i)]]+1
          terminals[[t]] <<- list(
            id = id,
            tmpID = paste0("t-", t),
            name = child$name,
            branch_length = child$branch_length,
            classes = "terminal"
          )
        } else {
          if (!is.null(child$confidence$text)) {
            n <<- n+1
            id <- paste0(id, "c", i[[length(i)]])
            i[[length(i)]] <<- i[[length(i)]]+1
            nonterminals[[n]] <<- list(
              id = id,
              tmpID = paste0("n-", n),
              confidence = child$confidence$text,
              branch_length = child$branch_length,
              classes = "nonterminal"
            )
          }
          i[[length(i)+1]] <<- 0
          lapply(child, explore_child, id=id)
          i <<- i[-length(i)]
        }
      }
    }
    lapply(tree, explore_child, id="r")

    # CORRECT SO FAR
    # explore_child <- function(child, id) {
    #   if (class(child) == "list") {
    #     #i <<- i+1
    #     #id <- paste0(id, "c", i)
    #     if (!is.null(child$name)) {
    #       t <<- t+1
    #       terminals[[t]] <<- list(
    #         #id = id,
    #         tmpID = paste0("t-", t),
    #         name = child$name,
    #         branch_length = child$branch_length,
    #         classes = "terminal"
    #       )
    #     } else {
    #       if (!is.null(child$confidence$text)) {
    #         n <<- n+1
    #         nonterminals[[n]] <<- list(
    #           #id = id,
    #           tmpID = paste0("n-", n),
    #           confidence = child$confidence$text,
    #           branch_length = child$branch_length,
    #           classes = "nonterminal"
    #         )
    #       }
    #       lapply(child, explore_child, id=id)
    #     }
    #     #i <<- i-1
    #   }
    # }
    # lapply(tree, explore_child, id="r")

    # FAILED ATTEMPT
    # explore_child <- function(child) {
    #   if (class(child) == "list") {
    #     if (!is.null(child$name)) {
    #       return(
    #         list(
    #           id = paste("t-", child$name),
    #           name = child$name,
    #           branch_length = child$branch_length,
    #           classes = "terminal"
    #         )
    #       )
    #     } else if (!is.null(child$confidence$text)) {
    #       return(
    #         list(
    #           id = paste("n-", child$confidence$text),
    #           confidence = child$confidence$text,
    #           branch_length = child$branch_length,
    #           classes = "nonterminal",
    #           child = lapply(child, explore_child)
    #         )
    #       )
    #     } else {
    #       return(lapply(child, explore_child))
    #     }
    #   }
    # }
    # nodes <- lapply(tree, explore_child)

    # print("TERMINALS")
    # str(terminals)
    # print(paste("SIZE", length(terminals)))
    # print("NONTERMINALS")
    # str(nonterminals)
    # print(paste("SIZE", length(nonterminals)))

    return(list(terminals = terminals, nonterminals = nonterminals))
  }

  get_terminals <- function(tree, terminals=list()) {
    get_name <- function(child) {
      if (class(child) == "list") {
        if (!is.null(child$name)) {
          terminals[[length(terminals)+1]] <<- list(
            name = child$name,
            branch_length = child$branch_length
          )
        } else {
          lapply(child, get_name)
        }
      }
    }
    lapply(tree, get_name)
    return(terminals)
  }

  get_col_positions <- function(tree, taxa, column_width=80) {
    # note constants for drawing calculations
    max_label_width <- max(unlist(lapply(taxa, function(taxon) return(nchar(taxon$name)))))
    drawing_width <- column_width - max_label_width - 1

    return(list())
  }

  get_row_positions <- function(tree, taxa) {
    positions <- lapply(1:length(taxa), function(id) return(2*(id-1)))
    names(positions) <- lapply(taxa, function(taxon) return(taxon$name))

    return(list())
  }

  clean_tree <- organize_tree(tree)
  taxa <- get_terminals(tree)
  col_positions <- get_col_positions(tree, taxa)
  row_positions <- get_row_positions(tree, taxa)

  nodes <- list()
  edges <- list()

  # TODO: remove dummy data to not overwrite outputs using functions above
  nodes <- list(1,2,3)
  edges <- list(4,5,6)
  elements <- c(nodes, edges)

  return (elements)
}

elements <- generate_elements(tree)

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
        elements = list(), # TODO: change to 'elements' once defined
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

# app$run_server()
