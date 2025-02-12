from PySide2 import QtWidgets
import maya.cmds as cmds
import os
import json

def main(*args):
    launch_ui()
    
filepath = cmds.file(q=True, sn=True)
filename = os.path.basename(filepath)
raw_name, extension = os.path.splitext(filename)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "characterCompilerTest", f"{raw_name}_skeleton.json")

def get_bone_data():
    bones = cmds.ls(type="joint")
    bone_data = {}
    
    for bone in bones:
        parent = cmds.listRelatives(bone, parent=True)
        position = cmds.xform(bone, q=True, ws=True, translation=True)
        orientation = cmds.joint(bone, q=True, orientation=True)
        radius = cmds.getAttr(f"{bone}.radius")  # Get the radius
        
        bone_data[bone] = {
            "parent": parent[0] if parent else None,
            "position": position,
            "orientation": orientation,
            "radius": radius
        }
    
    with open(desktop_path, "w") as file:
        json.dump(bone_data, file, indent=4)
    print("Bone data saved to", desktop_path)

def create_bones_from_file():
    # Prompt user for directory to open the file dialog
    dir_path = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory", os.path.expanduser("~"))
    
    if not dir_path:
        print("No directory selected!")
        return

    file_path = os.path.join(dir_path, "tmp.json")
    
    if not os.path.exists(file_path):
        print("No tmp.json file found in the selected directory!")
        return
    
    with open(file_path, "r") as file:
        bone_data = json.load(file)
    
    created_bones = {}
    root_bones = []
    
    # Create bones first without parenting
    for bone, data in bone_data.items():
        new_bone = cmds.createNode("joint", name=bone)
        cmds.xform(new_bone, ws=True, translation=data["position"])
        cmds.joint(new_bone, e=True, orientation=data["orientation"])
        cmds.setAttr(f"{new_bone}.radius", data["radius"])  # Set the radius
        
        created_bones[bone] = new_bone
        
        if data["parent"] is None:
            root_bones.append(new_bone)
    
    # Parent bones in the correct hierarchy
    for bone, data in bone_data.items():
        if data["parent"] and data["parent"] in created_bones:
            cmds.parent(created_bones[bone], created_bones[data["parent"]])
    
    print("Bones recreated with correct hierarchy, preserving multiple root chains.")

class BoneToolUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bone Tool")
        self.setLayout(QtWidgets.QVBoxLayout())
        
        self.export_button = QtWidgets.QPushButton("Export Bones")
        self.import_button = QtWidgets.QPushButton("Import Bones")
        
        self.layout().addWidget(self.export_button)
        self.layout().addWidget(self.import_button)
        
        self.export_button.clicked.connect(get_bone_data)
        self.import_button.clicked.connect(create_bones_from_file)
        
        self.show()

def launch_ui():
    global bone_tool_ui
    bone_tool_ui = BoneToolUI()