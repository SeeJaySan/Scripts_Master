"""
/ToolsetMaster.py

A dockable UI for Autodesk Maya designed to streamline rigging workflows. 
This script provides tools for creating, orienting, and visualizing joint structures, 
batch renaming, and additional utility widgets.

### Features:
- Enables creation, modification, and visualization of hierarchical structures.
- Offers batch processing tools for efficient renaming and organization.
- Includes interactive UI components such as sliders, dropdowns, and input fields.
- Seamlessly integrates into Maya’s workspace as a dockable interface.

### Usage:
1. Run the script to launch the `ToolsetMaster` UI.
2. Select a tool category tab to access its respective functions.
3. Choose a script from the dropdown and execute it with the run button.

### Metadata:
- **Author:** CJ Nowacek
- **Version:** 1.0.0
- **License:** GPL
- **Maintainer:** CJ Nowacek
- **Status:** Production
"""
# ------------------------------
# Imports
# ------------------------------
import sys
import os
import importlib
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

from maya import cmds as mc
from maya import OpenMaya as om
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from msc.third_party import zbw_controlShapes as zbw_con

# ------------------------------
# Varables
# ------------------------------

# Define the root directory where script paths will be sourced
ROOTDIR = os.path.dirname(__file__)

# Define the various script categories and their corresponding directories
SCRIPTS_PATHS = {
    "model": os.path.join(ROOTDIR, "model"),
    "rig": os.path.join(ROOTDIR, "rig"),
    "anim": os.path.join(ROOTDIR, "anim"),
    # "scene": os.path.join(ROOTDIR, "scene"),
    # "tool": os.path.join(ROOTDIR, "tool"),
    "wip": os.path.join(ROOTDIR, "WIP"),
}


def maya_main_window():
    """Return the Maya main window widget as a Python object."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


# ------------------------------
# Utility Functions
# ------------------------------


def list_modules(script_path):
    """Retrieve a list of Python script names (without .py extension) from a given directory."""
    module_names = []
    for each in os.listdir(script_path):
        if each.endswith(".py"):
            module_names.append(each.split(".")[0])
    return module_names


class TM_Tab(QtWidgets.QWidget):
    """Class defining the UI layout and components for each script category tab."""

    def __init__(self, parent=maya_main_window()):
        super(TM_Tab, self).__init__(parent)

        # Create the script selection dropdown and run button
        self.script_cbx = QtWidgets.QComboBox()
        self.run_btn = QtWidgets.QPushButton("Run")

        # Create a text input field for optional user parameters
        self.test_le = QtWidgets.QLineEdit("", self)

        # Layout configuration
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.script_cbx)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.test_le)
        layout.setAlignment(QtCore.Qt.AlignTop)


class TM_TabWindow(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    """Main dockable window containing the ToolsetMaster UI."""

    WINDOW_TITLE = "Toolset Master"
    WIDTH = 400
    HEIGHT = 125

    def __init__(self, parent=maya_main_window()):
        super(TM_TabWindow, self).__init__(parent)

        # Configure window properties
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        # Adjust window flags for different operating systems
        if mc.about(ntOS=True):
            self.setWindowFlags(
                self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint
            )
        elif mc.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        # Load available script modules
        self.module_names = {
            key: list_modules(path) for key, path in SCRIPTS_PATHS.items()
        }

        # Initialize UI elements
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create UI widgets and populate script selection lists."""
        self.tabs = {
            "Model": TM_Tab(),
            "Rig": TM_Tab(),
            "Anim": TM_Tab(),
            # "Tool": TM_Tab(),
            # "Scene": TM_Tab(),
            "Wip": TM_Tab(),
        }

        # Populate script dropdowns for each tab
        for key, tab in self.tabs.items():
            script_list = self.module_names.get(key.lower(), [])
            tab.script_cbx.addItems(script_list)

        # Create a tab widget and add each category as a separate tab
        self.tab_widget = QtWidgets.QTabWidget()
        for name, tab in self.tabs.items():
            self.tab_widget.addTab(tab, name)

    def create_layout(self):
        """Define and set up the layout for the main window."""
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tab_widget)

    def create_connections(self):
        """Connect button clicks to the script execution function."""
        self.tabs["Model"].run_btn.clicked.connect(lambda: self.run_script("model"))
        self.tabs["Rig"].run_btn.clicked.connect(lambda: self.run_script("rig"))
        self.tabs["Anim"].run_btn.clicked.connect(lambda: self.run_script("anim"))
        # self.tabs["Tool"].run_btn.clicked.connect(lambda: self.run_script("tool"))
        # self.tabs["Scene"].run_btn.clicked.connect(lambda: self.run_script("scene"))
        self.tabs["Wip"].run_btn.clicked.connect(lambda: self.run_script("wip"))

    def run_script(self, category):
        """Handle script execution based on the selected category and script."""
        script_path = SCRIPTS_PATHS.get(category, "")
        tab = self.tabs[category.capitalize()]
        selected_script = tab.script_cbx.currentText()

        # Retrieve user-provided input from the text field
        user_input = tab.test_le.text()

        # Ensure the script's directory is in the Python path
        if script_path not in sys.path:
            sys.path.append(script_path)

        # Dynamically import or reload the selected script
        if selected_script in sys.modules:
            importlib.reload(sys.modules[selected_script])
        else:
            importlib.import_module(selected_script)

        module = sys.modules[selected_script]

        try:
            # Attempt to call the script's main function with user input
            module.main(user_input).show()
        except AttributeError:
            pass  # Ignore errors if no main function is found
            # om.MGlobal.displayWarning("No main function found in {0}".format(selected_script))


def show_dockable_widget():
    """Display the ToolsetMaster window as a dockable widget in Maya."""
    try:
        # Close any existing instance of the ToolsetMaster window before opening a new one
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, TM_TabWindow):
                widget.close()
                widget.deleteLater()
    except Exception as e:
        print("Error closing existing widget: {0}".format(e))

    # Launch a new instance of the ToolsetMaster window
    dockable_widget = TM_TabWindow()
    dockable_widget.show(dockable_widget)


# Entry point when running the script directly
if __name__ == "__main__":
    show_dockable_widget()
