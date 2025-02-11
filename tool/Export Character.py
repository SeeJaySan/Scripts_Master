import maya.cmds as mc
import maya.mel as mel
import os

exportMeshes = []
exportSkeleton = []

def main(*args):
    CharacterExport()
    
# Get meshes to be exported
def GetExportMeshes():
    # List all transform nodes in the scene
    transform_nodes = mc.ls(type='transform')

    # Check if any of the transform nodes is named 'Export_Meshes'
    if 'ExportMeshes' in transform_nodes:
        mc.select('ExportMeshes')
        mc.SelectHierarchy()  # Select all nodes in the hierarchy
        exportMeshes = mc.ls(sl=True)
        exportMeshes.remove("ExportMeshes")
        return exportMeshes
    else:
        print("No transform node named 'ExportMeshes' found.")
        return []

# Get skeleton to be exported
def GetExportSkeleton():
    # List all joint nodes in the scene
    joint_nodes = mc.ls(type='transform')

    # Check if any of the joint nodes is named 'Skeleton'
    if 'Skeleton' in joint_nodes:
        mc.select('Skeleton')
        mc.SelectHierarchy()  # Select all nodes in the hierarchy
        exportSkeleton = mc.ls(sl=True)
        exportSkeleton.remove("Skeleton")
        return exportSkeleton
    else:
        print("No joint node named 'Skeleton' found.")
        return []
    
def CharacterExport():
    
    # Run the functions and store the results in exportMeshes and exportSkeleton
    exportMeshes = GetExportMeshes()
    exportSkeleton = GetExportSkeleton()
    
    # Select all nodes and print them
    mc.select("RIG")
    this = mc.SelectHierarchy()
    all_nodes = mc.ls( sl=True)
    print (all_nodes)
    # Print the skeleton and mesh lists
    print("Exported Skeleton: ", exportSkeleton)
    print("Exported Meshes: ", exportMeshes)
    
    # Combine the exported meshes and skeletons into a single list to remove from all_nodes
    combined_exported = exportMeshes + exportSkeleton
    
    # Use list comprehension to filter out the combined exported nodes from all_nodes
    newList = [node for node in all_nodes if node not in combined_exported]
    
    # Print the final filtered list
    print("Filtered List (without exported meshes and skeletons):", newList)
    
    # Select the filtered nodes
    mc.select(exportMeshes, "root")
    mc.parent(w = 1)
    #mc.delete(newList)
    
    
    # exporting
    mel.eval("FBXExportBakeComplexAnimation -v 1")
    mel.eval("FBXExportUpAxis z")
    
    scene = mc.file(q=True, sn=True)
    folder_path = os.path.dirname(scene)
    print(scene)
    print(folder_path)
    
    newName = scene.replace(".ma", ".fbx")
    
    mc.file(newName,f=True,options="v=0;",typ="FBX export",pr=True,es=True)
    
    
    mc.file(scene, f = True, o = True, s = False) # forcing the file to open will cause it not to save. Be careful
