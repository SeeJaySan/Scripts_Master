"""
File: QuickRigTool.py
Author: CJ Nowacek
Created Date: NA
Description: Quick Rig Tool for creating, editing joints, and creating controls in Maya.
"""

# IMPORT Python Standard Libraries
import sys
import os

# IMPORT PySide2 and Shiboken2
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

# IMPORT Maya Libraries
from maya import cmds as mc
from maya import mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# IMPORT Third-Party Libraries
from msc.third_party import zbw_controlShapes as zbw_con

# IMPORT Local Modules
from msc import jointCreateAndOrientatorModule as jCO


# Function to return the Maya main window as a Python object
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


# Widget for creating joints
class CreateJointsWidget(QtWidgets.QWidget):

    def __init__(self, parent=maya_main_window()):
        super(CreateJointsWidget, self).__init__(parent)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.button1 = QtWidgets.QPushButton("Start")
        self.button2 = QtWidgets.QPushButton("Aim")
        self.button3 = QtWidgets.QPushButton("CometOrient")
        self.button4 = QtWidgets.QPushButton("CometOrient")

    def create_layout(self):
        #layout = QtWidgets.QVBoxLayout(self)
        layout_01 = QtWidgets.QHBoxLayout(self)
        layout_02 = QtWidgets.QHBoxLayout(self)
        
        #layout_01.addWidget(self.button1)
        #layout_01.addWidget(self.button2)
        layout_02.addWidget(self.button1)


# Widget for editing joints
class EditJointsWidget(QtWidgets.QWidget):

    def __init__(self, parent=maya_main_window()):
        super(EditJointsWidget, self).__init__(parent)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.button1 = QtWidgets.QPushButton("Turn on Axis")
        self.button2 = QtWidgets.QPushButton("Turn off Axis")

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)


# Widget for creating controls
class CreateControlWidget(QtWidgets.QWidget):

    def __init__(self, parent=maya_main_window()):
        super(CreateControlWidget, self).__init__(parent)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.button1 = QtWidgets.QPushButton("Create Control")
        self.button2 = QtWidgets.QPushButton("Turn off Axis")

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)


# Main dialog window with tab widget
class TabWidgetDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Quick Rig Tool"

    def __init__(self, parent=maya_main_window()):
        super(TabWidgetDialog, self).__init__(parent)
        self.setFixedSize(500, 300)
        self.setWindowTitle(self.WINDOW_TITLE)
        
        # Setting window flags based on OS
        if mc.about(ntOS=True):
            self.setWindowFlags(
                self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint
            )
        elif mc.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        # Removing the question mark from the dialog window
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.CJ_wdg = CreateJointsWidget()
        self.EJ_wdg = EditJointsWidget()
        self.CC_wdg = CreateControlWidget()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.CJ_wdg, "Create Joints")
        self.tab_widget.addTab(self.EJ_wdg, "Edit Joints")
        self.tab_widget.addTab(self.CC_wdg, "Create Controls")

        self.joint_module = jCO.jointCreateAndOrientator()

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        layout.addStretch()

    def create_connections(self):
        self.CJ_wdg.button1.clicked.connect(self.joint_module.createBaseJoint)
        self.CJ_wdg.button2.clicked.connect(self.joint_module.endBaseJoint)
        
        self.EJ_wdg.button1.clicked.connect(self.joint_module.turnOnJointAxisVis)
        self.EJ_wdg.button2.clicked.connect(self.joint_module.turnOffJointAxisVis)
        
        self.CC_wdg.button1.clicked.connect(self.joint_module.createControl)
        
        
    # Functions
    def run_comet_joint_orient(self):
        pass




# Main function to run the tool
def main(*args):
    dialog = TabWidgetDialog()
    dialog.show()
