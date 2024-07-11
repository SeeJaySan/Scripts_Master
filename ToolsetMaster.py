"""
File: ToolsetMaster.py
Author: CJ Nowacek
Date: 2024-03-17
Description: ToolsetMaster fuctionality for loading script and generally useful tools
"""

# IMPORT Python
import sys
import os
import importlib
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

# IMPORT maya

from maya import cmds as mc
from maya import mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from cn_rigging_scripts import cn_jointCreateAndOrientatorModule as jCO

# IMPORT Third-Party
from cn_rigging_scripts import zbw_controlShapes as zbw_con

# getting scripts from live folder
liveScriptsPath = r"C:\Users\cjnowacek\Desktop\important files\scripts\myScript\live"

moduleNames = []

dir_list = os.listdir(liveScriptsPath)
for each in dir_list:
    if each.endswith(".py"):
        newName = each.split(".")[0]
        moduleNames.append(newName)
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


class ModelTools(QtWidgets.QWidget):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(ModelTools, self).__init__(parent)

        # create widgets
        self.script_cbx = QtWidgets.QComboBox()
        self.run_btn = QtWidgets.QPushButton("Run")

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.script_cbx)
        layout.addWidget(self.run_btn)


class RigTools(QtWidgets.QWidget):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(RigTools, self).__init__(parent)

        # create widgets
        self.script_cbx = QtWidgets.QComboBox()
        self.run_btn = QtWidgets.QPushButton("Run")

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.script_cbx)
        layout.addWidget(self.run_btn)


class LoadScriptsWidget(QtWidgets.QWidget):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(LoadScriptsWidget, self).__init__(parent)

        # create widgets
        self.script_cbx = QtWidgets.QComboBox()

        self.run_btn = QtWidgets.QPushButton("Run")

        # layout

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.script_cbx)
        layout.addWidget(self.run_btn)


class TabWidgetDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Toolset Master"

    def __init__(self, parent=maya_main_window()):
        super(TabWidgetDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if mc.about(ntOS=True):
            self.setWindowFlags(
                self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint
            )
        elif mc.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.model_wdg = ModelTools()
        self.rig_wdg = RigTools()
        self.script_wdg = LoadScriptsWidget()

        for each in moduleNames:
            self.script_wdg.script_cbx.addItem("{0}".format(each))

        self.tab_widget = QtWidgets.QTabWidget()

        self.tab_widget.addTab(self.script_wdg, "Load Scripts")
        self.tab_widget.addTab(self.model_wdg, "model")
        self.tab_widget.addTab(self.rig_wdg, "rig")

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        layout.addStretch()

    def create_connections(self):
        self.script_wdg.run_btn.clicked.connect(self.run)

    def run(self):
        cbxValue = self.script_wdg.script_cbx.currentText()
        # print (cbxValue)
        # scriptToReload = liveScriptsPath + cbxValue + ".py"

        if liveScriptsPath == bool(os.path.exists(liveScriptsPath)):
            pass
        else:
            # TODO write a custom path widow if the path isn't found -- get the code from the geoExporter
            pass

        if liveScriptsPath not in sys.path:
            sys.path.append(liveScriptsPath)

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
            pass

        that = this.main()
        that.show()

        # test_dialog = ToolsetMaster.TabWidgetDialog()
