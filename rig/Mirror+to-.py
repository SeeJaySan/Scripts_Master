import maya.cmds as cmds
import os

# Get the current file path of the Maya scene
file_path = cmds.file(query=True, sceneName=True)
directory = os.path.dirname(file_path)
directorySourceimages = directory.replace('scenes', 'sourceimages')
directorySourceimagesTmp = directory.replace('scenes', 'sourceimages/tmp')

# Function to store and reset joint rotations
def store_and_reset_joint_rotations():
    """
    Stores the current joint rotations and resets all joints (except omitted ones) to their preferred angles.
    
    Returns:
        dict: A dictionary containing joint names as keys and their rotation values as dictionaries.
    """
    joint_rotations = {}
    joints = cmds.ls(type='joint')
    omit_joints = {"pelvis", "root"}  # Joints to omit from the operation

    for joint in joints:
        if joint in omit_joints:
            continue

        # Store the joint's current rotation values
        rotation = cmds.getAttr(f"{joint}.rotate")[0]
        joint_rotations[joint] = {'x': rotation[0], 'y': rotation[1], 'z': rotation[2]}

        # Reset the joint to its preferred angles
        cmds.joint(joint, e=True, assumePreferredAngles=True)

    return joint_rotations

# Function to reapply joint rotations
def reapply_joint_rotations(joint_rotations):
    """
    Reapplies stored joint rotations to the respective joints.

    Args:
        joint_rotations (dict): A dictionary of joint rotations to reapply.
    """
    for joint, rotation in joint_rotations.items():
        cmds.setAttr(f"{joint}.rotate", rotation['x'], rotation['y'], rotation['z'])

# Function to mirror a selected mesh
def mirror_selected_mesh(selected_objects):
    """
    Mirrors the selected mesh along the YZ plane while preserving skinCluster weights.

    Args:
        selected_objects (list): A list of selected objects.
    """
    if not selected_objects:
        cmds.warning("No mesh selected. Please select a mesh before running the script.")
        return

    # Ensure only one object is selected
    if len(selected_objects) > 1:
        cmds.warning("Please select only one mesh for mirroring.")
        return

    mesh = selected_objects[0]

    # Find the skinCluster attached to the mesh
    skin_clusters = cmds.ls(cmds.listHistory(mesh), type="skinCluster")
    if not skin_clusters:
        cmds.warning(f"No skinCluster found on {mesh}.")
        return

    skin_cluster = skin_clusters[0]
    
    #backing up skin cluster weights
    if skin_clusters:
        for skin_cluster in skin_clusters:
            cmds.select(skin_cluster)
            export_name = f'{mesh}_skinWeights.json'
            print (directorySourceimagesTmp)
            #export_path = os.path.join(directorySourceimagesTmp, export_name)
            cmds.deformerWeights(export_name, ex=True, df=skin_cluster, fm="JSON", p=directorySourceimagesTmp)

    # Perform the mirroring operation
    cmds.copySkinWeights(ss=skin_cluster, ds=skin_cluster, mirrorMode='YZ', mirrorInverse=False)

# Main function to run the tool
def main(*args):
    # Get the currently selected objects
    selected_objects = cmds.ls(selection=True)

    # Store and reset joint rotations
    joint_rotations = store_and_reset_joint_rotations()

    # Perform the mirroring operation
    mirror_selected_mesh(selected_objects)

    # Reapply the saved joint rotations
    reapply_joint_rotations(joint_rotations)



