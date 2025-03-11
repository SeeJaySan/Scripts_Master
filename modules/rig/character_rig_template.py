import maya.cmds as cmds

def main(*args):
    CharacterTemplate()

def CharacterTemplate():
    # Create the top-level node
    rig_node = cmds.createNode('transform', name='RIG')

    # Create 'Meshes' and 'Skeleton' nodes under 'RIG'
    meshes_node = cmds.createNode('transform', name='Meshes', parent=rig_node)
    cmds.createNode('transform', name='Skeleton', parent=rig_node)

    # Create 'ExportMeshes' and 'bak' nodes under 'Meshes'
    cmds.createNode('transform', name='ExportMeshes', parent=meshes_node)
    cmds.createNode('transform', name='bak', parent=meshes_node)

    # Print the created hierarchy for verification
    print("Hierarchy created:")
    print(cmds.ls(rig_node, dag=True))