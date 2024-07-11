"""
File: ToolsetMaster.py
Author: CJ Nowacek
Created Date: 2024-03-17
Description: ToolsetMaster fuctionality for loading script and generally useful tools
"""

# Importing Python
import sys
import os
import importlib
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

# Import maya
from maya import cmds as mc
from maya import mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# Importing Third-Party
from third_party import zbw_controlShapes as zbw_con

# Getting folder paths
ROOTDIR = os.path.dirname(__file__)

modual_ScriptsPath = ROOTDIR + r"\modules"
model_ScriptsPath = ROOTDIR + r"\model"
rig_ScriptsPath = ROOTDIR + r"\rig"
anim_ScriptsPath = ROOTDIR + r"\anim"
tool_ScriptsPath = ROOTDIR + r"\tool"
wip_ScriptsPath = ROOTDIR + r"\WIP"

# Creating lists for modules in folders
modular_ModuleNames = []
model_ModuleNames = []
rig_ModuleNames = []
anim_ModuleNames = []
tool_ModuleNames = []
wip_ModuleNames = []

# Appending moduals to a list
dir_list = os.listdir(modual_ScriptsPath)
for each in dir_list:
    if each.endswith(".py"):
        newName = each.split(".")[0]
        modular_ModuleNames.append(newName)
    else:
        continue

dir_list = os.listdir(model_ScriptsPath)
for each in dir_list:
    if each.endswith(".py"):
        newName = each.split(".")[0]
        model_ModuleNames.append(newName)
    else:
        continue

dir_list = os.listdir(rig_ScriptsPath)
for each in dir_list:
    if each.endswith(".py"):
        newName = each.split(".")[0]
        rig_ModuleNames.append(newName)
    else:
        continue

dir_list = os.listdir(anim_ScriptsPath)
for each in dir_list:
    if each.endswith(".py"):
        newName = each.split(".")[0]
        anim_ModuleNames.append(newName)
    else:
        continue

dir_list = os.listdir(tool_ScriptsPath)
for each in dir_list:
    if each.endswith(".py"):
        newName = each.split(".")[0]
        tool_ModuleNames.append(newName)
    else:
        continue

dir_list = os.listdir(wip_ScriptsPath)
for each in dir_list:
    if each.endswith(".py"):
        newName = each.split(".")[0]
        wip_ModuleNames.append(newName)
    else:
        continue


# Main maya window
def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

# Defining tab widgets
class TM_Tab(QtWidgets.QWidget):

    # Initiallizing window Variables
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
        layout.setAlignment((QtCore.Qt.AlignTop))

# Creating main dialog
class TM_TabWindow(QtWidgets.QDialog):

    WINDOW_TITLE = "Toolset Master"

    def __init__(self, parent=maya_main_window()):
        super(TM_TabWindow, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.width = 400
        self.height = 125
        
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        
        '''
        self.setGeometry(
            (1920 / 2) - self.width / 2,
            (1080 / 2) - self.height / 2,
            self.width,
            self.height,
        )
        '''

        if mc.about(ntOS=True):
            self.setWindowFlags(
                self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint
            )
        elif mc.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.reloadModuals()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def reloadModuals(self):
        path = modual_ScriptsPath
        if path not in sys.path:
            sys.path.append(path)

        for i in modular_ModuleNames:
            pass
            #importlib.reload((sys.modules[(i)]))
            #if i in list(sys.modules.keys()):
               # importlib.reload((sys.modules[(i)]))
        #    else:
             #   importlib.import_module(i)

    def create_widgets(self):
        self.model_wdg = TM_Tab()
        self.rig_wdg = TM_Tab()
        self.anim_wdg = TM_Tab()
        self.tool_wdg = TM_Tab()
        self.wip_wdg = TM_Tab()
        self.render_wdg = TM_Tab()
        self.script_wdg = TM_Tab()

        for each in model_ModuleNames:
            self.model_wdg.script_cbx.addItem("{0}".format(each))

        for each in rig_ModuleNames:
            self.rig_wdg.script_cbx.addItem("{0}".format(each))

        for each in anim_ModuleNames:
            self.anim_wdg.script_cbx.addItem("{0}".format(each))

        for each in tool_ModuleNames:
            self.tool_wdg.script_cbx.addItem("{0}".format(each))

        for each in wip_ModuleNames:
            self.wip_wdg.script_cbx.addItem("{0}".format(each))

        self.tab_widget = QtWidgets.QTabWidget()

        self.tab_widget.addTab(self.model_wdg, "Model")
        self.tab_widget.addTab(self.rig_wdg, "Rig")
        self.tab_widget.addTab(self.anim_wdg, "Anim")
        self.tab_widget.addTab(self.tool_wdg, "Tool")
        self.tab_widget.addTab(self.wip_wdg, "WIP")
        self.tab_widget.addTab(self.script_wdg, "Other")

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        # layout.addStretch()

    def create_connections(self):
        self.model_wdg.run_btn.clicked.connect(self.model_wdg_run)
        self.rig_wdg.run_btn.clicked.connect(self.rig_wdg_run)
        self.anim_wdg.run_btn.clicked.connect(self.anim_wdg_run)
        self.tool_wdg.run_btn.clicked.connect(self.tool_wdg_run)
        self.script_wdg.run_btn.clicked.connect(self.script_wdg_run)
        self.wip_wdg.run_btn.clicked.connect(self.wip_wdg_run)

    # Run commands for each of the widgets
    def model_wdg_run(self):

        path = model_ScriptsPath
        cbxValue = self.model_wdg.script_cbx.currentText()

        print(cbxValue)
        # scriptToReload = rig_ScriptsPath + cbxValue + ".py"

        # TODO write a loop to cycle through all the paths with a for loop
        # for paths in allPaths:
        # if paths not in sys.path:

        if path not in sys.path:
            sys.path.append(path)

        # cycle through all moduals and reload them - TODO
        if cbxValue in list(sys.modules.keys()):
            importlib.reload((sys.modules[(cbxValue)]))
            this = sys.modules[(cbxValue)]
            # that = this.main()

            # that = (dir(this)) # get the modules in the file

        else:
            importlib.import_module(cbxValue)
            this = sys.modules[(cbxValue)]
            # that = this.main()

        try:
            that.close()
            that.deleteLater()
        except:
            that = this.main()
            try:
                that.show()
            except:
                pass

        # test_dialog = ToolsetMaster.TM_TabWindow()

    def rig_wdg_run(self):

        path = rig_ScriptsPath
        cbxValue = self.rig_wdg.script_cbx.currentText()

        print(cbxValue)
        # scriptToReload = rig_ScriptsPath + cbxValue + ".py"

        # TODO write a loop to cycle through all the paths with a for loop
        # for paths in allPaths:
        # if paths not in sys.path:

        if path not in sys.path:
            sys.path.append(path)

        # cycle through all moduals and reload them - TODO
        if cbxValue in list(sys.modules.keys()):
            importlib.reload((sys.modules[(cbxValue)]))
            this = sys.modules[(cbxValue)]
            # that = this.main()

            # that = (dir(this)) # get the modules in the file

        else:
            importlib.import_module(cbxValue)
            this = sys.modules[(cbxValue)]
            # that = this.main()

        try:
            that.close()
            that.deleteLater()
        except:

            that = this.main()
            try:
                that.show()
            except:
                pass

        # add def main() to files in order to keep the actually main() named unique

        # def main():
        # BfaOps_AnimExportPrep()

        # test_dialog = ToolsetMaster.TM_TabWindow()

    def anim_wdg_run(self):

        path = anim_ScriptsPath
        cbxValue = self.anim_wdg.script_cbx.currentText()

        print(cbxValue)
        # scriptToReload = rig_ScriptsPath + cbxValue + ".py"

        # TODO write a loop to cycle through all the paths with a for loop
        # for paths in allPaths:
        # if paths not in sys.path:

        if path not in sys.path:
            sys.path.append(path)

        # cycle through all moduals and reload them - TODO
        if cbxValue in list(sys.modules.keys()):
            importlib.reload((sys.modules[(cbxValue)]))
            this = sys.modules[(cbxValue)]
            # that = this.main()

            # that = (dir(this)) # get the modules in the file

        else:
            importlib.import_module(cbxValue)
            this = sys.modules[(cbxValue)]
            # that = this.main()

        try:
            that.close()
            that.deleteLater()
        except:

            that = this.main()
            try:
                that.show()
            except:
                pass

        # add def main() to files in order to keep the actually main() named unique

        # def main():
        # BfaOps_AnimExportPrep()

        # test_dialog = ToolsetMaster.TM_TabWindow()

    def script_wdg_run(self):

        path = rig_ScriptsPath
        cbxValue = self.script_wdg.script_cbx.currentText()

        print(cbxValue)
        # scriptToReload = rig_ScriptsPath + cbxValue + ".py"

        # TODO write a loop to cycle through all the paths with a for loop
        # for paths in allPaths:
        # if paths not in sys.path:

        if path not in sys.path:
            sys.path.append(path)

        # cycle through all moduals and reload them - TODO
        if cbxValue in list(sys.modules.keys()):
            importlib.reload((sys.modules[(cbxValue)]))
            this = sys.modules[(cbxValue)]
            # that = this.main()

            # that = (dir(this)) # get the modules in the file

        else:
            importlib.import_module(cbxValue)
            this = sys.modules[(cbxValue)]
            # that = this.main()

        try:
            that.close()
            that.deleteLater()
        except:
            that = this.main()
            try:
                that.show()
            except:
                pass

        # test_dialog = ToolsetMaster.TM_TabWindow()

    def tool_wdg_run(self):

        path = tool_ScriptsPath
        cbxValue = self.tool_wdg.script_cbx.currentText()

        print(cbxValue)
        # scriptToReload = rig_ScriptsPath + cbxValue + ".py"

        # TODO write a loop to cycle through all the paths with a for loop
        # for paths in allPaths:
        # if paths not in sys.path:

        if path not in sys.path:
            sys.path.append(path)

        # cycle through all moduals and reload them - TODO
        if cbxValue in list(sys.modules.keys()):
            importlib.reload((sys.modules[(cbxValue)]))
            this = sys.modules[(cbxValue)]
            # that = this.main()

            # that = (dir(this)) # get the modules in the file

        else:
            importlib.import_module(cbxValue)
            this = sys.modules[(cbxValue)]
            # that = this.main()

        try:
            that.close()
            that.deleteLater()
        except:

            that = this.main()
            try:
                that.show()
            except:
                pass

        # add def main() to files in order to keep the actually main() named unique

        # def main():
        # BfaOps_AnimExportPrep()

        # test_dialog = ToolsetMaster.TM_TabWindow()

    def wip_wdg_run(self):

        path = wip_ScriptsPath
        cbxValue = self.wip_wdg.script_cbx.currentText()

        print(cbxValue)
        # scriptToReload = rig_ScriptsPath + cbxValue + ".py"

        # TODO write a loop to cycle through all the paths with a for loop
        # for paths in allPaths:
        # if paths not in sys.path:

        if path not in sys.path:
            sys.path.append(path)

        # cycle through all moduals and reload them - TODO
        if cbxValue in list(sys.modules.keys()):
            importlib.reload((sys.modules[(cbxValue)]))
            this = sys.modules[(cbxValue)]
            # that = this.main()

            # that = (dir(this)) # get the modules in the file

        else:
            importlib.import_module(cbxValue)
            this = sys.modules[(cbxValue)]
            # that = this.main()

        try:
            that.close()
            that.deleteLater()
        except:

            that = this.main()
            try:
                that.show()
            except:
                pass

        # add def main() to files in order to keep the actually main() named unique

        # def main():
        # BfaOps_AnimExportPrep()

        # test_dialog = ToolsetMaster.TM_TabWindow()
