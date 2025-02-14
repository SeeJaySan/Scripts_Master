from PySide2 import QtWidgets
import maya.cmds as cmds
import os
import shutil
import json
import heapq


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
            cmds.setAttr(f"{material}.specularRoughness", .75)
            
            print(f"Texture re-linked: {texture_path} to {mesh}")
        else:
            print(f"Texture file missing for {mesh}, skipping texture assignment.")

    print("Meshes imported and textures re-linked.")



def export_mesh_weights():
    """Exports skin weights of selected meshes to a JSON file, keeping only the 4 highest influences per vertex."""
    dir_path = os.path.join(os.path.expanduser("~"), "Desktop", "characterCompilerTest")
    os.makedirs(dir_path, exist_ok=True)  # Ensure the directory exists

    weights_data = {}  # Store weights for all selected meshes

    selected_meshes = cmds.ls(selection=True, type="transform")
    if not selected_meshes:
        print("No meshes selected!")
        return

    for mesh in selected_meshes:
        skin_clusters = cmds.ls(cmds.listHistory(mesh), type="skinCluster")
        if not skin_clusters:
            print(f"[WARNING] No skinCluster found for {mesh}, skipping weight export.")
            continue

        skin_cluster = skin_clusters[0]  # Get the first skinCluster found
        influences = cmds.skinCluster(skin_cluster, query=True, influence=True)  # Get all joints affecting mesh
        vertex_count = cmds.polyEvaluate(mesh, vertex=True)  # Number of vertices

        mesh_weights = {}  # Store vertex weights

        for i in range(vertex_count):
            vertex = f"{mesh}.vtx[{i}]"  # Construct vertex name
            weights = cmds.skinPercent(skin_cluster, vertex, query=True, value=True)  # Get joint weights

            # Filter only the highest 4 influences per vertex
            top_influences = heapq.nlargest(4, zip(influences, weights), key=lambda x: x[1])

            # Remove zero-weight influences
            filtered_weights = {joint: weight for joint, weight in top_influences if weight > 0}

            if filtered_weights:
                mesh_weights[i] = filtered_weights  # Store weights per vertex

        # Store weights for this mesh
        weights_data[mesh] = mesh_weights

    # Save weight data to JSON
    weights_file = os.path.join(dir_path, "mesh_weights.json")
    with open(weights_file, "w") as file:
        json.dump(weights_data, file, indent=4)

    print(f"✅ Skin weights exported to {weights_file}")


def import_mesh_weights():
    """Reads the skin weights JSON and applies them to imported meshes manually."""
    dir_path = os.path.join(os.path.expanduser("~"), "Desktop", "characterCompilerTest")
    weights_file = os.path.join(dir_path, "mesh_weights.json")

    if not os.path.exists(weights_file):
        print("[ERROR] No mesh_weights.json file found. Cannot import weights.")
        return

    with open(weights_file, "r") as file:
        mesh_weights = json.load(file)  # Read weight data from file

    selected_meshes = cmds.ls(selection=True, type="transform")
    if not selected_meshes:
        print("[WARNING] No meshes selected. Attempting to apply to all stored meshes.")
        selected_meshes = list(mesh_weights.keys())  # Use all meshes from JSON if none are selected

    for mesh in selected_meshes:
        if mesh not in mesh_weights:
            print(f"[WARNING] No weight data found for {mesh}, skipping import.")
            continue

        print(f"🔄 Importing weights for: {mesh}")

        # **Unlock transformations to prevent errors**
        for attr in ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ"]:
            if cmds.attributeQuery(attr, node=mesh, exists=True) and cmds.getAttr(f"{mesh}.{attr}", lock=True):
                cmds.setAttr(f"{mesh}.{attr}", lock=False)
                print(f"🔓 Unlocked {attr} on {mesh}")

        # **Find or create a skinCluster for the mesh**
        skin_clusters = cmds.ls(cmds.listHistory(mesh), type="skinCluster")
        if not skin_clusters:
            print(f"[INFO] No skinCluster found on {mesh}, binding joints before importing weights.")

            # Get all joints listed in the stored weight data
            all_joints = set()
            for vertex_data in mesh_weights[mesh].values():
                all_joints.update(vertex_data.keys())  # Collect all joints affecting any vertex

            all_joints = list(filter(cmds.objExists, all_joints))  # Ensure joints exist in the scene
            if not all_joints:
                print(f"[ERROR] No valid joints found for {mesh}. Skipping weight import.")
                continue

            # Create a new skinCluster with the correct joints
            skin_cluster = cmds.skinCluster(all_joints, mesh, toSelectedBones=True, normalizeWeights=1)[0]
        else:
            skin_cluster = skin_clusters[0]

        # **Apply stored weights per vertex**
        for vertex_index, influences in mesh_weights[mesh].items():
            vertex = f"{mesh}.vtx[{vertex_index}]"

            # **Filter out missing joints**
            valid_influences = {joint: weight for joint, weight in influences.items() if cmds.objExists(joint)}

            # **Apply weights using skinPercent**
            if valid_influences:
                cmds.skinPercent(skin_cluster, vertex, transformValue=list(valid_influences.items()))

        print(f"✅ Successfully imported weights for {mesh}")


class MeshToolUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mesh Export/Import Tool")
        self.resize(300, 400)  # Increase height to fit new buttons

        self.setLayout(QtWidgets.QVBoxLayout())

        self.export_button = QtWidgets.QPushButton("Export Meshes")
        self.import_button = QtWidgets.QPushButton("Import Meshes")
        self.export_weights_button = QtWidgets.QPushButton("Export Weights")  # New Button
        self.import_weights_button = QtWidgets.QPushButton("Import Weights")  # New Button

        self.layout().addWidget(self.export_button)
        self.layout().addWidget(self.import_button)
        self.layout().addWidget(self.export_weights_button)  # Add Button to UI
        self.layout().addWidget(self.import_weights_button)  # Add Button to UI

        self.export_button.clicked.connect(export_selected_meshes)
        self.import_button.clicked.connect(import_meshes)
        self.export_weights_button.clicked.connect(export_mesh_weights)  # Connect Button
        self.import_weights_button.clicked.connect(import_mesh_weights)  # Connect Button

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
