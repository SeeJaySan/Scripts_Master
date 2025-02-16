import maya.cmds as cmds
import maya.api.OpenMaya as om


def average_vertex_weights():
    # Get selected vertices
    selection = cmds.ls(selection=True, fl=True)
    if len(selection) != 2:
        cmds.error("Select exactly two vertices.")

    # Get the mesh from the selected vertices
    mesh = selection[0].split(".")[0]

    # Create a selection list and get the DAG path
    sel_list = om.MSelectionList()
    sel_list.add(mesh)
    dag_path = sel_list.getDagPath(0)

    # Create MFnMesh object
    mesh_fn = om.MFnMesh(dag_path)

    # Extract vertex indices
    vertex_indices = [int(sel.split("[")[-1][:-1]) for sel in selection]

    # Find connected vertices for each selected vertex
    connected_vertices = []
    for vertex_index in vertex_indices:
        # Get the vertex iterator
        vertex_iter = om.MItMeshVertex(dag_path)
        vertex_iter.setIndex(vertex_index)

        # Get connected vertices
        connected = vertex_iter.getConnectedVertices()
        connected_vertices.append(list(connected))

    # Find the common vertex that connects the two selected vertices
    common_vertex = set(connected_vertices[0]) & set(connected_vertices[1])

    if not common_vertex:
        cmds.error("No common connecting vertex found.")

    # Take the first (and should be only) common vertex
    common_vertex_index = list(common_vertex)[0]

    # Construct the vertex names
    common_vertex_name = f"{mesh}.vtx[{common_vertex_index}]"

    # Get the current skin cluster
    skin_cluster = cmds.ls(cmds.listHistory(mesh), type="skinCluster")[0]

    # Get the influences (joints) for the skin cluster
    influences = cmds.skinCluster(skin_cluster, query=True, influence=True)

    # Get weights for the first two selected vertices
    weights1 = cmds.skinPercent(skin_cluster, selection[0], query=True, value=True)
    weights2 = cmds.skinPercent(skin_cluster, selection[1], query=True, value=True)

    # Average the weights
    averaged_weights = [(w1 + w2) / 2.0 for w1, w2 in zip(weights1, weights2)]

    # Set the weights using a list of tuples (influence, weight)
    weight_list = list(zip(influences, averaged_weights))

    # Set the weights for the common vertex
    for influence, weight in weight_list:
        cmds.skinPercent(
            skin_cluster, common_vertex_name, transformValue=(influence, weight)
        )

    print(
        f"Averaged weights from {selection[0]} and {selection[1]} onto {common_vertex_name}"
    )
    print("Averaged weights:", dict(zip(influences, averaged_weights)))

    return common_vertex_name


# Run the function
average_vertex_weights()
