# AUTO GENERATED FILE - DO NOT EDIT

cytoCytoscape <- function(id=NULL, className=NULL, style=NULL, elements=NULL, stylesheet=NULL, layout=NULL, pan=NULL, zoom=NULL, panningEnabled=NULL, userPanningEnabled=NULL, minZoom=NULL, maxZoom=NULL, zoomingEnabled=NULL, userZoomingEnabled=NULL, boxSelectionEnabled=NULL, autoungrabify=NULL, autolock=NULL, autounselectify=NULL, autoRefreshLayout=NULL, tapNode=NULL, tapNodeData=NULL, tapEdge=NULL, tapEdgeData=NULL, mouseoverNodeData=NULL, mouseoverEdgeData=NULL, selectedNodeData=NULL, selectedEdgeData=NULL) {
    
    props <- list(id=id, className=className, style=style, elements=elements, stylesheet=stylesheet, layout=layout, pan=pan, zoom=zoom, panningEnabled=panningEnabled, userPanningEnabled=userPanningEnabled, minZoom=minZoom, maxZoom=maxZoom, zoomingEnabled=zoomingEnabled, userZoomingEnabled=userZoomingEnabled, boxSelectionEnabled=boxSelectionEnabled, autoungrabify=autoungrabify, autolock=autolock, autounselectify=autounselectify, autoRefreshLayout=autoRefreshLayout, tapNode=tapNode, tapNodeData=tapNodeData, tapEdge=tapEdge, tapEdgeData=tapEdgeData, mouseoverNodeData=mouseoverNodeData, mouseoverEdgeData=mouseoverEdgeData, selectedNodeData=selectedNodeData, selectedEdgeData=selectedEdgeData)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Cytoscape',
        namespace = 'dash_cytoscape',
        propNames = c('id', 'className', 'style', 'elements', 'stylesheet', 'layout', 'pan', 'zoom', 'panningEnabled', 'userPanningEnabled', 'minZoom', 'maxZoom', 'zoomingEnabled', 'userZoomingEnabled', 'boxSelectionEnabled', 'autoungrabify', 'autolock', 'autounselectify', 'autoRefreshLayout', 'tapNode', 'tapNodeData', 'tapEdge', 'tapEdgeData', 'mouseoverNodeData', 'mouseoverEdgeData', 'selectedNodeData', 'selectedEdgeData'),
        package = 'dashCytoscape'
        )

    structure(component, class = c('dash_component', 'list'))
}
