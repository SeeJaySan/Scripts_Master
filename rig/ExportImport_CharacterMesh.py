from PySide2 import QtWidgets
import maya.cmds as cmds
import os
import shutil
import json

def get_texture_path(mesh):
    """Retrieve the texture file path from the material assigned to the mesh."""
    
    # Get the shape node of the mesh
    shapes = cmds.listRelatives(mesh, shapes=True) or []
    if not shapes:
        print(f"[WARNING] No shape found for {mesh}. It may be a group or empty transform.")
        return None
    shape_node = shapes[0]

    # Get the shading group using listSets
    shading_groups = cmds.listSets(object=shape_node, type=1)  # Type=1 ensures it's a shading group
    if not shading_groups:
        print(f"[WARNING] No shading group found for {mesh}. Material might be missing.")
        return None
    shading_group = shading_groups[0]

    # Get the material from the shading group
    materials = cmds.listConnections(f"{shading_group}.surfaceShader") or []
    if not materials:
        print(f"[WARNING] No material found for {mesh}.")
        return None
    material = materials[0]

    # Find file nodes connected to the material
    file_nodes = cmds.listConnections(material, type="file") or []
    if not file_nodes:
        print(f"[WARNING] No file texture node found for {mesh}. It may be using procedural textures.")
        return None

    # Return the first valid texture path
    for file_node in file_nodes:
        if cmds.attributeQuery("fileTextureName", node=file_node, exists=True):
            file_path = cmds.getAttr(f"{file_node}.fileTextureName")
            if file_path:
                print(f"[INFO] Texture path for {mesh}: {file_path}")
                return file_path

    print(f"[WARNING] No valid texture file found for {mesh}")
    return None





def export_selected_meshes():
    """Exports selected meshes as OBJ files and saves a JSON file with texture paths."""
    dir_path = os.path.join(os.path.expanduser("~"), "Desktop", "characterCompilerTest")
    texture_folder = os.path.join(dir_path, "textures")  # Folder for textures
    os.makedirs(texture_folder, exist_ok=True)  # Create the folder if it doesn’t exist

    mesh_data = {}

    selected_transforms = cmds.ls(selection=True, type="transform")
    if not selected_transforms:
        print("No meshes selected!")
        return

    selected_meshes = []
    for transform in selected_transforms:
        shapes = cmds.listRelatives(transform, shapes=True, type="mesh")
        if shapes:
            selected_meshes.append(transform)

    if not selected_meshes:
        print("No valid mesh objects found!")
        return

    for mesh in selected_meshes:
        obj_file = os.path.join(dir_path, f"{mesh}.obj")

        print("Exporting OBJ:", obj_file)

        cmds.select(mesh)
        cmds.file(obj_file, force=True, options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1",
                  type="OBJexport", exportSelected=True)

        texture_path = get_texture_path(mesh)
        
        # Copy texture to the textures folder and update its path
        new_texture_path = None
        if texture_path and os.path.exists(texture_path):
            new_texture_path = os.path.join(texture_folder, os.path.basename(texture_path))
            shutil.copy(texture_path, new_texture_path)  # Copy the texture file

        mesh_data[mesh] = {"texture": new_texture_path}  # Store new relative path

    json_file = os.path.join(dir_path, "mesh_data.json")
    with open(json_file, "w") as file:
        json.dump(mesh_data, file, indent=4)

    print(f"Meshes and textures exported to {dir_path}")

def import_meshes():
    """Imports OBJ files one at a time and re-links textures from the textures folder."""
    dir_path = os.path.join(os.path.expanduser("~"), "Desktop", "characterCompilerTest")
    texture_folder = os.path.join(dir_path, "textures")

    json_file = os.path.join(dir_path, "mesh_data.json")
    if not os.path.exists(json_file):
        print("No mesh_data.json found!")
        return

    with open(json_file, "r") as file:
        mesh_data = json.load(file)

    for mesh, data in mesh_data.items():
        obj_file = os.path.join(dir_path, f"{mesh}.obj")
        if not os.path.exists(obj_file):
            print(f"OBJ file missing for {mesh}, skipping import.")
            continue

        print(f"Importing: {obj_file}")

        before_import = set(cmds.ls(transforms=True))
        cmds.file(obj_file, i=True, renameAll=False, mergeNamespacesOnClash=False)
        after_import = set(cmds.ls(transforms=True))
        imported_objects = list(after_import - before_import)

        print(f"Imported Objects: {imported_objects}")

        imported_mesh = None
        for obj in imported_objects:
            if obj.lower().startswith(mesh.lower()):
                imported_mesh = obj
                break

        if not imported_mesh:
            print(f"Could not find {mesh} after import! Check object names in Maya.")
            continue

        if imported_mesh != mesh:
            cmds.rename(imported_mesh, mesh)
            imported_mesh = mesh

        print(f"Final Imported Mesh Name: {imported_mesh}")

        material_name = f"{mesh}_mat"
        shading_group = f"{material_name}_SG"
        file_node = f"{mesh}_tex"
        place2d_node = f"{mesh}_place2d"

        if not cmds.objExists(material_name):
            material = cmds.shadingNode("standardSurface", asShader=True, name=material_name)
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_group)
            cmds.connectAttr(f"{material}.outColor", f"{shading_group}.surfaceShader", force=True)
        else:
            material = material_name

        cmds.sets(mesh, edit=True, forceElement=shading_group)

        # Re-link the texture from the textures folder
        texture_path = data.get("texture")
        if texture_path and os.path.exists(texture_path):
            if not cmds.objExists(file_node):
                file_texture = cmds.shadingNode("file", asTexture=True, name=file_node)
            else:
                file_texture = file_node

            if not cmds.objExists(place2d_node):
                place2d_texture = cmds.shadingNode("place2dTexture", asUtility=True, name=place2d_node)
            else:
                place2d_texture = place2d_node

            cmds.setAttr(f"{file_texture}.fileTextureName", texture_path, type="string")

            if not cmds.isConnected(f"{file_texture}.outColor", f"{material}.baseColor"):
                cmds.connectAttr(f"{file_texture}.outColor", f"{material}.baseColor", force=True)

            cmds.connectAttr(f"{place2d_texture}.outUV", f"{file_texture}.uvCoord", force=True)
            cmds.connectAttr(f"{place2d_texture}.outUvFilterSize", f"{file_texture}.uvFilterSize", force=True)

            print(f"Texture re-linked: {texture_path} to {mesh}")
        else:
            print(f"Texture file missing for {mesh}, skipping texture assignment.")

    print("Meshes imported and textures re-linked.")

class MeshToolUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mesh Export/Import Tool")
        self.resize(300, 300)  # Set the window size to 300x300

        self.setLayout(QtWidgets.QVBoxLayout())

        self.export_button = QtWidgets.QPushButton("Export Meshes")
        self.import_button = QtWidgets.QPushButton("Import Meshes")

        self.layout().addWidget(self.export_button)
        self.layout().addWidget(self.import_button)

        self.export_button.clicked.connect(export_selected_meshes)
        self.import_button.clicked.connect(import_meshes)

        self.show()
mesh_tool_ui = None

def launch_mesh_ui():
    global mesh_tool_ui
    if mesh_tool_ui and mesh_tool_ui.isVisible():
        mesh_tool_ui.raise_()
        return
    mesh_tool_ui = MeshToolUI()
    mesh_tool_ui.show()

launch_mesh_ui()
