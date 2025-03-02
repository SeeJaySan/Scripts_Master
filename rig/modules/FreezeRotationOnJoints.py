import maya.cmds as cmds

# Get the currently selected objects
selected_objects = cmds.ls(selection=True)

# Check if there is at least one object selected
if selected_objects:
    # Assume the first selected object is the joint to modify
    joint_name = selected_objects[0]

    # Get the current rotation values of the joint
    rotate_x_value = cmds.getAttr(f"{joint_name}.rotateX")
    rotate_y_value = cmds.getAttr(f"{joint_name}.rotateY")
    rotate_z_value = cmds.getAttr(f"{joint_name}.rotateZ")
    
    # Get the current joint orientation values of the joint
    orient_x_value = cmds.getAttr(f"{joint_name}.jointOrientX")
    orient_y_value = cmds.getAttr(f"{joint_name}.jointOrientY")
    orient_z_value = cmds.getAttr(f"{joint_name}.jointOrientZ")

    # Calculate new joint orientation values by adding current rotation to orientation
    new_x_value = rotate_x_value + orient_x_value
    new_y_value = rotate_y_value + orient_y_value
    new_z_value = rotate_z_value + orient_z_value

    # Set the new joint orientation values
    cmds.setAttr(f"{joint_name}.jointOrientX", new_x_value)
    cmds.setAttr(f"{joint_name}.jointOrientY", new_y_value)
    cmds.setAttr(f"{joint_name}.jointOrientZ", new_z_value)
    
    # Reset the joint's rotation values to zero
    cmds.setAttr(f"{joint_name}.rotateX", 0)
    cmds.setAttr(f"{joint_name}.rotateY", 0)
    cmds.setAttr(f"{joint_name}.rotateZ", 0)
    
else:
    # Print a warning message if no object is selected
    print("No objects selected. Please select a joint.")
