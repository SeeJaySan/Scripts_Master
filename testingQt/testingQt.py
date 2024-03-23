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

from rigging import jointCreateAndOrientatorModule as jCO

# IMPORT Third-Party
import zbw_controlShapes as zbw_con

# getting scripts from live folder
liveScriptsPath = r'C:\Users\cjnowacek\Desktop\important files\scripts\myScript\live'

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


class ButtonWidget(QtWidgets.QWidget):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(ButtonWidget, self).__init__(parent)

        # create widgets

        self.script_cbx = QtWidgets.QComboBox()
        self.run_btn = QtWidgets.QPushButton('Run')

        # layout

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.script_cbx)
        layout.addWidget(self.run_btn)


class TabWidgetDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Tools"

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

        # fileMenu = mainMenu.addMenu("File")

    def create_widgets(self):
        self.buttons_wdg = ButtonWidget()

        for each in moduleNames:

            self.buttons_wdg.script_cbx.addItem("{0}".format(each))

        self.tab_widget = QtWidgets.QTabWidget()

        self.tab_widget.addTab(self.buttons_wdg, "Create Tab")

        self.this = jCO.jointCreateAndOrientator()

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        layout.addStretch()

    def create_connections(self):
        self.buttons_wdg.run_btn.clicked.connect(self.run)


    def run(self):
        cbxValue = self.buttons_wdg.script_cbx.currentText()
        #print (cbxValue)
        scriptToReload = liveScriptsPath + cbxValue + ".py"
