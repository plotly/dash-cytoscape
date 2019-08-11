library(dash)
library(dashHtmlComponents)
library(dashCytoscape)
library(XML)
source("demosR/dummyData.R")

app <- Dash$new()

tree <- xmlToList(xmlParse(file = "demos/data/apaf.xml"))$phylogeny
capture.output(tree, file = "demosR/treeR.txt", append = FALSE)

generate_elements <- function(tree, xlen=30, ylen=30, grabbable=FALSE, i=list(), n=1) {
  # there are 31 "terminal" nodes with their respective 31 "support" nodes
  # and 30 "nonterminal" nodes with their respective 29 "support" nodes
  # since the root node does not require a preceding "support" node;
  # each "support" node has the same x position as the parent clade,
  # and the same y position as the child clade; it is used to create
  # the 90 degree angle between the parent and the children;
  # edge config: parent -> support -> child
  nodes <- list()
  edges <- list()

  # append root element
  nodes[[n]] <- list(
    data = list(id = "r"),
    position = list(x = 30, y = 1200),
    classes = "nonterminal",
    grabbable = FALSE
  )

  # append all child nodes/edges and respective support nodes/edges
  explore_child <- function(child, child_id, branch_length) {
    if (class(child) == "list") {
      if (!is.null(child$name)) {
        clade_id <- child_id
        support_id <- paste0(child_id, "s", i[[length(i)]])
        child_id <- paste0(child_id, "c", i[[length(i)]])
        n <<- n+2
        # support node and edge
        nodes[[n-1]] <<- list(
          data = list(id = support_id),
          # TODO: edit (x,y) according to branch_length = child$branch_length
          # position = list(x = 0, y = 0),
          classes = "support",
          grabbable = FALSE
        )
        edges[[n-2]] <<- list(
          data = list(
            source = clade_id,
            target = support_id,
            sourceCladeId = clade_id
          )
        )
        # terminal node and edge
        nodes[[n]] <<- list(
          data = list(id = child_id, name = child$name),
          # TODO: edit (x,y) according to branch_length = child$branch_length
          # position = list(x = 0, y = 0),
          classes = "terminal",
          grabbable = FALSE
        )
        edges[[n-1]] <<- list(
          data = list(
            source = support_id,
            target = child_id,
            length = branch_length,
            sourceCladeId = clade_id
          )
        )
        i[[length(i)]] <<- i[[length(i)]]+1
      } else {
        if (!is.null(child$confidence$text)) {
          clade_id <- child_id
          support_id <- paste0(child_id, "s", i[[length(i)]])
          child_id <- paste0(child_id, "c", i[[length(i)]])
          n <<- n+2
          # support node and edge
          nodes[[n-1]] <<- list(
            data = list(id = support_id),
            # TODO: edit (x,y) according to branch_length = child$branch_length
            # position = list(x = 0, y = 0),
            classes = "support",
            grabbable = FALSE
          )
          edges[[n-2]] <<- list(
            data = list(
              source = clade_id,
              target = support_id,
              sourceCladeId = clade_id
            )
          )
          # nonterminal node and edge
          nodes[[n]] <<- list(
            data = list(id = child_id, confidence = child$confidence$text),
            # TODO: edit (x,y) according to branch_length = child$branch_length
            # position = list(x = 0, y = 0),
            classes = "nonterminal",
            grabbable = FALSE
          )
          edges[[n-1]] <<- list(
            data = list(
              source = support_id,
              target = child_id,
              length = branch_length,
              sourceCladeId = clade_id
            )
          )
          i[[length(i)]] <<- i[[length(i)]]+1
        }
        i[[length(i)+1]] <<- 0
        lapply(child, explore_child, child_id=child_id, branch_length=child$branch_length)
        i <<- i[-length(i)]
      }
    }
  }
  lapply(tree, explore_child, child_id="r", branch_length=0)

  # TODO: remove these draft functions and respective outputs
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

  # TODO: delete test print statements
  # print("NODES")
  # str(nodes)
  # print(paste("SIZE", length(nodes)))
  # print("EDGES")
  # str(edges)
  # print(paste("SIZE", length(edges)))

  # TODO: add remaining attributes for nodes (i.e. position) in function the explore_child
  elements <- c(nodes, edges)

  return(elements)
}

elements <- generate_elements(tree)

# TODO: delete test print statements
# print("ELEMENTS")
# str(elements)
# print(paste("SIZE", length(elements)))

stylesheet <- list(
  list(
    "selector" = "edge",
    "style" = list(
      "source-endpoint" = "inside-to-node",
      "target-endpoint" = "inside-to-node"
    )
  ),
  list(
    "selector" = ".support",
    "style" = list(
      "background-opacity" = 0
    )
  ),
  list(
    "selector" = ".nonterminal",
    "style" = list(
      "label" = "data(confidence)",
      "text-valign" = "top",
      "text-halign" = "left",
      "background-opacity" = 0
    )
  ),
  list(
    "selector" = ".terminal",
    "style" = list(
      "label" = "data(name)",
      "text-valign" = "center",
      "text-halign" = "right",
      "width" = 10,
      "height" = 10,
      "background-color" = "#222222"
    )
  )
)

app$layout(
  htmlDiv(
    list(
      cytoCytoscape(
        id = "cytoscape",
        elements = dummyElements, # TODO: change to "elements" once defined
        stylesheet = stylesheet,
        layout = list(
          "name" = "preset"
        ),
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
  params = list(input(id = "cytoscape", property = "mouseoverEdgeData")),
  function(edgeData) {
    if (is.null(edgeData)) {
      return(stylesheet)
    }
    val <- ifelse(grepl("s", edgeData$source), strsplit(edgeData$source, "s")[[1]], edgeData$source)
    children_style = list(
      list(
        selector = sprintf("edge[source *= '%s']", val),
        style = list(
          'line-color' = 'blue'
        )
      )
    )
    return(c(stylesheet, children_style))
  }
)

app$run_server(port = "8080", debug = TRUE)
