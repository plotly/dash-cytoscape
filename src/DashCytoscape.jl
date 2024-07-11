
module DashCytoscape
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "1.0.2"

include("jl/cyto_cytoscape.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "dash_cytoscape",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "dash_cytoscape.min.js",
    external_url = "https://unpkg.com/dash-cytoscape@1.0.2/dash_cytoscape/dash_cytoscape.min.js",
    dynamic = nothing,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
