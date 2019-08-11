library(dash)
library(dashHtmlComponents)
library(dashCytoscape)
library(XML)

app <- Dash$new()

tree <- xmlToList(xmlParse(file = "demos/data/apaf.xml"))$phylogeny
capture.output(tree, file = "demosR/tree.txt", append = FALSE)

generate_elements <- function(tree, xlen=30, ylen=30, grabbable=FALSE,
                              nodes=list(), edges=list(), i=list(), n=1) {

  # there are 31 "terminal" nodes with their respective 31 "support" nodes
  # and 30 "nonterminal" nodes with their respective 29 "support" nodes
  # since the root node does not require a preceding "support" node;
  # each "support" node has the same x position as the parent clade,
  # and the same y position as the child clade; it is used to create
  # the 90 degree angle between the parent and the children;
  # edge config: parent -> support -> child

  # append root element
  nodes[[n]] <- list(
    data = list(id = "r"),
    position = list(x = 30, y = 1200),
    classes = "nonterminal",
    grabbable = FALSE
  )
  # function to append all nodes and respective support nodes
  explore_child <- function(child, child_id) {
    if (class(child) == "list") {
      if (!is.null(child$name)) {
        support_id <- paste0(child_id, "s", i[[length(i)]])
        child_id <- paste0(child_id, "c", i[[length(i)]])
        n <<- n+2
        nodes[[n-1]] <<- list(
          data = list(id = support_id),
          # TODO: edit (x,y) according to branch_length = child$branch_length
          # position = list(x = 0, y = 0),
          classes = "support",
          grabbable = FALSE
        )
        nodes[[n]] <<- list(
          data = list(id = child_id, name = child$name),
          # TODO: edit (x,y) according to branch_length = child$branch_length
          # position = list(x = 0, y = 0),
          classes = "terminal",
          grabbable = FALSE
        )
        i[[length(i)]] <<- i[[length(i)]]+1
      } else {
        if (!is.null(child$confidence$text)) {
          support_id <- paste0(child_id, "s", i[[length(i)]])
          child_id <- paste0(child_id, "c", i[[length(i)]])
          n <<- n+2
          nodes[[n-1]] <<- list(
            data = list(id = support_id),
            # TODO: edit (x,y) according to branch_length = child$branch_length
            # position = list(x = 0, y = 0),
            classes = "support",
            grabbable = FALSE
          )
          nodes[[n]] <<- list(
            data = list(id = child_id, confidence = child$confidence$text),
            # TODO: edit (x,y) according to branch_length = child$branch_length
            # position = list(x = 0, y = 0),
            classes = "nonterminal",
            grabbable = FALSE
          )
          i[[length(i)]] <<- i[[length(i)]]+1
        }
        i[[length(i)+1]] <<- 0
        lapply(child, explore_child, child_id=child_id)
        i <<- i[-length(i)]
      }
    }
  }
  lapply(tree, explore_child, child_id="r")

  print("NODES")
  str(nodes)
  print(paste("SIZE", length(nodes)))
  print("EDGES")
  str(edges)
  print(paste("SIZE", length(edges)))

  # TODO: remove dummy data to not overwrite outputs using functions above
  nodes <- list(1,2,3)
  edges <- list(4,5,6)

  elements <- c(nodes, edges)
  return(elements)

  # TODO: remove these drafts
  # get_terminals <- function(tree, terminals=list()) {
  #   get_name <- function(child) {
  #     if (class(child) == "list") {
  #       if (!is.null(child$name)) {
  #         terminals[[length(terminals)+1]] <<- list(
  #           name = child$name,
  #           branch_length = child$branch_length
  #         )
  #       } else {
  #         lapply(child, get_name)
  #       }
  #     }
  #   }
  #   lapply(tree, get_name)
  #   return(terminals)
  # }
  #
  # get_col_positions <- function(tree, taxa, column_width=80) {
  #   # note constants for drawing calculations
  #   max_label_width <- max(unlist(lapply(taxa, function(taxon) return(nchar(taxon$name)))))
  #   drawing_width <- column_width - max_label_width - 1
  #
  #   return(list())
  # }
  #
  # get_row_positions <- function(tree, taxa) {
  #   positions <- lapply(1:length(taxa), function(id) return(2*(id-1)))
  #   names(positions) <- lapply(taxa, function(taxon) return(taxon$name))
  #
  #   return(list())
  # }
  #
  # taxa <- get_terminals(tree)
  # col_positions <- get_col_positions(tree, taxa)
  # row_positions <- get_row_positions(tree, taxa)

}

elements <- generate_elements(tree)

layout <- list("name" = "preset")

stylesheet <- list(
  list(
    "selector" = ".nonterminal",
    "style" = list(
      "label" = "data(confidence)",
      "background-opacity" = 0,
      "text-halign" = "left",
      "text-valign" = "top"
    )
  ),
  list(
    "selector" = ".support",
    "style" = list("background-opacity" = 0)
  ),
  list(
    "selector" = "edge",
    "style" = list(
      "source-endpoint" = "inside-to-node",
      "target-endpoint" = "inside-to-node"
    )
  ),
  list(
    "selector" = ".terminal",
    "style" = list(
      "label" = "data(name)",
      "width" = 10,
      "height" = 10,
      "text-valign" = "center",
      "text-halign" = "right",
      "background-color" = "#222222"
    )
  )
)

app$layout(
  htmlDiv(
    list(
      cytoCytoscape(
        id = "cytoscape",
        elements = list(), # TODO: change to "elements" once defined
        stylesheet = stylesheet,
        layout = layout,
        style = list(
          "height" = "95vh",
          "width" = "100%"
        )
      )
    )
  )
)

app$callback(
  output = list(id = "cytoscape", property = "stylesheet"),
  params = list(
    input(id = "cytoscape", property = "mouseoverEdgeData")
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
