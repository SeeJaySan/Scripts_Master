import os
import maya.cmds as mc
import maya.mel as mel

class BfaOpsAnimExporter(object):
    def __init__(self):
        self.window_name = "BfaOps_AnimExport"
        self.title = "Anim Exporter"
        self.size = (400, 120)

        self.create_ui()

    def create_ui(self):
        # Close old window if it exists
        if mc.window(self.window_name, exists=True):
            mc.deleteUI(self.window_name, window=True)

        # Create new window
        self.window = mc.window(self.window_name, title=self.title)

        mc.columnLayout(adjustableColumn=True)
        mc.text(self.title)
        mc.separator(height=20)

        self.prep_btn = mc.button(label="Prep", command=self.prepare_scene)
        mc.separator(height=20)
        mc.text("Set Time Range")
        mc.separator(height=10)
        self.min_time_btn = mc.button(label="Set Min Time", command=self.set_min_time)
        self.max_time_btn = mc.button(label="Set Max Time", command=self.set_max_time)
        mc.separator(height=20)
        mc.text("Exporting")
        mc.separator(height=10)
        self.export_selected_btn = mc.button(label="First Time Export", command=self.export_selection, enable=False)
        self.export_btn = mc.button(label="Export", command=self.export_animations, enable=False)
        mc.separator(height=20)
        mc.text("Restarting File")
        mc.separator(height=10)
        self.reopen_btn = mc.button(label="Reopen", command=self.restart_file)

        mc.separator(height=20)
        mc.showWindow()

    def prepare_scene(self, *args):
        # Prepare scene for export
        mel.eval("file -save;")
        mel.eval('namespace -mergeNamespaceWithRoot -removeNamespace "SKL_robin";')

        all_ref_paths = mc.file(q=True, reference=True) or []

        for ref_path in all_ref_paths:
            if mc.referenceQuery(ref_path, isLoaded=True):
                mc.file(ref_path, importReference=True)
                new_ref_paths = mc.file(q=True, reference=True)
                if new_ref_paths:
                    all_ref_paths.extend([path for path in new_ref_paths if path not in all_ref_paths])

        mc.select("SKL")
        self.move_selection_to_world("DOWN")

        mc.select("GEO")
        self.move_children_to_world()

        mc.select("Root", hi=True)

        mc.button(self.export_selected_btn, e=True, enable=True)
        mc.button(self.export_btn, e=True, enable=True)

        mc.button(self.prep_btn, e=True, enable=False)
        mc.button(self.min_time_btn, e=True, enable=False)
        mc.button(self.max_time_btn, e=True, enable=False)

    def move_selection_to_world(self, direction):
        selected = mc.pickWalk(direction=direction)
        mc.parent(selected, world=True)

    def move_children_to_world(self):
        children = mc.listRelatives(c=True)
        if children:
            mc.parent(children, world=True)

    def export_animations(self, *args):
        mc.select("Root", hi=True)

        filepath = mc.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        path = filepath.replace(filename, "")
        new_filename = filename.replace("ma", "fbx")
        new_path = os.path.join(path, "exportTesting", new_filename)

        min_time = mc.playbackOptions(q=True, min=True)
        max_time = mc.playbackOptions(q=True, max=True)

        mel.eval("FBXResetExport")
        mel.eval("FBXExportBakeComplexAnimation -v 1")
        mel.eval(f"FBXExportBakeComplexStart -v {min_time}")
        mel.eval(f"FBXExportBakeComplexEnd -v {max_time}")
        mel.eval("FBXExportAnimationOnly -v 1")
        mel.eval(f"FBXExport -f \"{new_path}\" -s")

    def restart_file(self, *args):
        filepath = mc.file(q=True, sn=True)
        mc.file(filepath, open=True, force=True)

        mc.button(self.export_selected_btn, e=True, enable=False)
        mc.button(self.export_btn, e=True, enable=False)
        mc.button(self.prep_btn, e=True, enable=True)
        mc.button(self.min_time_btn, e=True, enable=True)
        mc.button(self.max_time_btn, e=True, enable=True)

    def set_min_time(self, *args):
        current_time = mc.currentTime(q=True)
        mc.playbackOptions(min=current_time, ast=current_time)

    def set_max_time(self, *args):
        current_time = mc.currentTime(q=True)
        mc.playbackOptions(max=current_time, aet=current_time)

    def export_selection(self, *args):
        mel.eval("ExportSelection;")

def main():
    exporter = BfaOpsAnimExporter()
    exporter.run()