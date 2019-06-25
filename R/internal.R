.dashCytoscape_js_metadata <- function() {
deps_metadata <- list(`dash_cytoscape` = structure(list(name = "dash_cytoscape",
version = "0.1.1", src = list(href = NULL,
file = "deps"), meta = NULL,
script = 'dash_cytoscape.min.js',
stylesheet = NULL, head = NULL, attachment = NULL, package = "dashCytoscape",
all_files = FALSE), class = "html_dependency"))
return(deps_metadata)
}

dash_assert_valid_wildcards <- function (attrib = list("data", "aria"), ...)
{
    args <- list(...)
    validation_results <- lapply(names(args), function(x) {
        grepl(paste0("^", attrib, "-[a-zA-Z0-9]{1,}$", collapse = "|"),
            x)
    })
    if (FALSE %in% validation_results) {
        stop(sprintf("The following wildcards are not currently valid in Dash: '%s'",
            paste(names(args)[grepl(FALSE, unlist(validation_results))],
                collapse = ", ")), call. = FALSE)
    }
    else {
        return(args)
    }
}
