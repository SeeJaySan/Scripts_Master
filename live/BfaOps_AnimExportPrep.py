import maya.cmds as cmds
import maya.mel as mel
import os

def BfaOps_AnimExportPrep():
        
    mel.eval('namespace -mergeNamespaceWithRoot -removeNamespace "SKL_robin";')

    all_ref_paths = cmds.file(q=True, reference=True) or []  # Get a list of all top-level references in the scene.

    for ref_path in all_ref_paths:
        if cmds.referenceQuery(ref_path, isLoaded=True):  # Only import it if it's loaded, otherwise it would throw an error.
            cmds.file(ref_path, importReference=True)  # Import the reference.

            new_ref_paths = cmds.file(q=True, reference=True)  # If the reference had any nested references they will now become top-level references, so recollect them.
            if new_ref_paths:
                for new_ref_path in new_ref_paths:
                    if new_ref_path not in all_ref_paths:  # Only add on ones that we don't already have.
                        all_ref_paths.append(new_ref_path)
    cmds.select('SKL')
    this = cmds.pickWalk(direction = 'DOWN')
    cmds.parent(this, w = 1)

    that = cmds.select('GEO')
    this1 = cmds.listRelatives(c = True)
    cmds.parent(this1, w = 1)

    cmds.select('Root', hi = 1)

