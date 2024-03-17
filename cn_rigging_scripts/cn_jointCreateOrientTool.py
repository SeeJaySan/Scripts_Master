# IMPORT Python
import sys
import os
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

# IMPORT maya

from maya import cmds as mc
from maya import mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# Import My Modules
# import jointCreateAndOrientator

# IMPORT Third-Party
import zbw_controlShapes as zbw_con

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


class ButtonWidget(QtWidgets.QWidget):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(ButtonWidget, self).__init__(parent)

        # create widgets

        self.button1 = QtWidgets.QPushButton('Start')
        self.button2 = QtWidgets.QPushButton('Aim')
        self.button3 = QtWidgets.QPushButton('Create')

        # layout

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        # layout.addWidget(self.button3)


class TabWidgetDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Custom Tab Widget Example"

    def __init__(self, parent=maya_main_window()):
        super(TabWidgetDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if mc.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^
                                QtCore.Qt.WindowContextHelpButtonHint)
        elif mc.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        # getting rid of the question mark
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.buttons_wdg = ButtonWidget()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.buttons_wdg, "Create Joints")
        self.this = jointCreateAndOrientator()

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        layout.addStretch()

    def create_connections(self):
        self.buttons_wdg.button1.clicked.connect(self.this.createBaseJoint)
        self.buttons_wdg.button2.clicked.connect(self.this.endBaseJoint)
        # self.buttons_wdg.button3.clicked.connect(self.this.parentAndOrient)


class jointCreateAndOrientator(object):

    def __init__(self):
        self.baseJnt = []
        self.endJnt = []

    def createBaseJoint(self):

        sel = mc.ls(sl=1)
        clstr = mc.cluster()
        mc.select(cl=1)
        self.baseJnt = mc.joint(rad=10)
        mc.select(cl=1)
        const = mc.parentConstraint(clstr, self.baseJnt, mo=0)
        mc.delete(const, clstr)
        mc.select(sel)
        mc.hilite(sel, tgl=1)

    def endBaseJoint(self):

        clstr = mc.cluster()
        mc.select(cl=1)
        self.endJnt = mc.joint(rad=10)
        mc.select(cl=1)
        const = mc.parentConstraint(clstr, self.endJnt, mo=0)
        mc.delete(const, clstr)
        self.parentAndOrient()

    def parentAndOrient(self):

        mc.parent(self.endJnt, self.baseJnt)

        mc.joint(self.baseJnt, e=True, oj="xyz",
                 secondaryAxisOrient="zdown", ch=True)

        mc.joint(self.endJnt, e=True, oj="none", ch=True)
