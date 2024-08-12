"""
File: ToolsetMaster.py
Author: CJ Nowacek
Created Date: 2024-03-17
Description: ToolsetMaster functionality for loading scripts and generally useful tools.
"""

import sys
import os
import importlib
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

from maya import cmds as mc
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from third_party import zbw_controlShapes as zbw_con


ROOTDIR = os.path.dirname(__file__)

SCRIPTS_PATHS = {
    "modules": os.path.join(ROOTDIR, "modules"),
    "model": os.path.join(ROOTDIR, "model"),
    "rig": os.path.join(ROOTDIR, "rig"),
    "anim": os.path.join(ROOTDIR, "anim"),
    "tool": os.path.join(ROOTDIR, "tool"),
    "wip": os.path.join(ROOTDIR, "WIP")
}

def list_modules(script_path):
    """List all Python files in a given directory."""
    module_names = []
    for each in os.listdir(script_path):
        if each.endswith(".py"):
            module_names.append(each.split(".")[0])
    return module_names

def maya_main_window():
    """Return the Maya main window widget as a Python object."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class TM_Tab(QtWidgets.QWidget):
    """Class to define the UI structure for each tab."""

    def __init__(self, parent=maya_main_window()):
        super(TM_Tab, self).__init__(parent)

        # Create widgets
        self.script_cbx = QtWidgets.QComboBox()
        self.run_btn = QtWidgets.QPushButton("Run")
        self.test_le = QtWidgets.QLineEdit("Enter Text", self)

        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.script_cbx)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.test_le)
        layout.setAlignment(QtCore.Qt.AlignTop)


class TM_TabWindow(QtWidgets.QDialog):
    """Main dialog window for ToolsetMaster."""

    WINDOW_TITLE = "Toolset Master"
    WIDTH = 400
    HEIGHT = 125

    def __init__(self, parent=maya_main_window()):
        super(TM_TabWindow, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        if mc.about(ntOS=True):
            self.setWindowFlags(
                self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint
            )
        elif mc.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.module_names = {key: list_modules(path) for key, path in SCRIPTS_PATHS.items()}

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create widgets for all tabs."""
        self.tabs = {
            "Model": TM_Tab(),
            "Rig": TM_Tab(),
            "Anim": TM_Tab(),
            "Tool": TM_Tab(),
            "WIP": TM_Tab(),
            "Other": TM_Tab()
        }

        for key, tab in self.tabs.items():
            script_list = self.module_names.get(key.lower(), [])
            tab.script_cbx.addItems(script_list)

        self.tab_widget = QtWidgets.QTabWidget()
        for name, tab in self.tabs.items():
            self.tab_widget.addTab(tab, name)

    def create_layout(self):
        """Set the layout of the main dialog."""
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tab_widget)

    def create_connections(self):
        """Connect buttons to their respective functions."""
        self.tabs["Model"].run_btn.clicked.connect(lambda: self.run_script("model"))
        self.tabs["Rig"].run_btn.clicked.connect(lambda: self.run_script("rig"))
        self.tabs["Anim"].run_btn.clicked.connect(lambda: self.run_script("anim"))
        self.tabs["Tool"].run_btn.clicked.connect(lambda: self.run_script("tool"))
        self.tabs["WIP"].run_btn.clicked.connect(lambda: self.run_script("wip"))
        self.tabs["Other"].run_btn.clicked.connect(lambda: self.run_script("other"))

    def run_script(self, category):
        """Handle the logic for running the selected script."""
        script_path = SCRIPTS_PATHS.get(category, "")
        tab = self.tabs[category.capitalize()]
        selected_script = tab.script_cbx.currentText()

        if script_path not in sys.path:
            sys.path.append(script_path)

        if selected_script in sys.modules:
            importlib.reload(sys.modules[selected_script])
        else:
            importlib.import_module(selected_script)

        module = sys.modules[selected_script]
        try:
            module.main().show()
        except AttributeError:
            om.MGlobal.displayWarning(f"No main function found in {selected_script}")


if __name__ == "__main__":
    try:
        dialog.close()  # pylint: disable=E0601
        dialog.deleteLater()
    except:
        pass

    dialog = TM_TabWindow()
    dialog.show()
