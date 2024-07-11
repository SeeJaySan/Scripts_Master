# IMPORT Python
import sys
import os
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

# IMPORT maya

from maya import cmds as mc
from maya import mel as mel

import importlib
from maya import OpenMaya as om
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


# TODO add reload fuction to the imported module

from modules import jointCreateAndOrientatorModule as jCO


# IMPORT Third-Party
from third_party import zbw_controlShapes as zbw_con

# Main maya window


def main():
    asdf = TabWidgetDialog()
    asdf.show()


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class CreateJointsWidget(QtWidgets.QWidget):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(CreateJointsWidget, self).__init__(parent)

        # create widgets

        self.button1 = QtWidgets.QPushButton("Start")
        self.button2 = QtWidgets.QPushButton("Aim")
        # self.button3 = QtWidgets.QPushButton('Create')

        # layout

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        # layout.addWidget(self.button3)


class EditJointsWidget(QtWidgets.QWidget):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(EditJointsWidget, self).__init__(parent)

        # create widgets

        self.button1 = QtWidgets.QPushButton("Turn on Axis")
        self.button2 = QtWidgets.QPushButton("Turn off Axis")
        # self.button3 = QtWidgets.QPushButton('Create')

        # layout

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        # layout.addWidget(self.button3)
        
class CreatControlWidget(QtWidgets.QWidget):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(CreatControlWidget, self).__init__(parent)

        # create widgets

        self.button1 = QtWidgets.QPushButton("Create Control")
        self.button2 = QtWidgets.QPushButton("Turn off Axis")
        # self.button3 = QtWidgets.QPushButton('Create')

        # layout

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        # layout.addWidget(self.button3)


class TabWidgetDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Quick Rig Tool"

    def __init__(self, parent=maya_main_window()):
        super(TabWidgetDialog, self).__init__(parent)
        
        self.width = 500
        self.height = 300
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        

        self.setWindowTitle(self.WINDOW_TITLE)
        
        if mc.about(ntOS=True):
            self.setWindowFlags(
                self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint
            )
        elif mc.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        # getting rid of the question mark
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.CJ_wdg = CreateJointsWidget()
        self.EJ_wdg = EditJointsWidget()
        self.CC_wdg = CreatControlWidget()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.CJ_wdg, "Create Joints")
        self.tab_widget.addTab(self.EJ_wdg, "Edit Joints")
        self.tab_widget.addTab(self.CC_wdg, "Create Controls")
        self.this = jCO.jointCreateAndOrientator()

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        layout.addStretch()

    def create_connections(self):
        self.CJ_wdg.button1.clicked.connect(self.this.createBaseJoint)
        self.CJ_wdg.button2.clicked.connect(self.this.endBaseJoint)
        # self.CJ_wdg.button3.clicked.connect(self.this.parentAndOrient)
        
        self.EJ_wdg.button1.clicked.connect(self.this.turnOnJointAxisVis)
        self.EJ_wdg.button2.clicked.connect(self.this.turnOffJointAxisVis)
        
        self.CC_wdg.button1.clicked.connect(self.this.createControl)
        