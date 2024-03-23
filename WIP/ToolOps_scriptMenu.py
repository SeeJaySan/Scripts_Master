# IMPORT Python
import sys
import importlib
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

# IMPORT maya
from maya import cmds as mc
from maya import mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui

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


# UI creation
class ToolOps_scriptMenuUI(QtWidgets.QDialog):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(ToolOps_scriptMenuUI, self).__init__(parent)

        self.setWindowTitle("Tool_Ops_v001")
        self.setMaximumSize(400, 1000)
        self.setMinimumSize(243, 180)
        self.setGeometry((1920 / 10) * 7.05, 1080 / 2 - 240, 300, 190)

    # load scripts
    def ToolOps_scriptMenuUI(self):

        for module_name in list(sys.modules.keys()):
            top_module = module_name.split(".")[0]
            print(top_module)

            if top_module == "rigOps_createContols":
                importlib.reload((sys.modules[module_name]))

            if top_module == "ArmOps_IKFKSwitch":
                importlib.reload((sys.modules[module_name]))

        if path not in sys.path:
            sys.path.append(path)

        import rigOps_createContols
        import ArmOps_IKFKSwitch

        print("execute with: rigOps_createContols.rigOps_createContols()")
        print('execute with: ArmOps_IKFKSwitch.ArmOps_IKFKSwitch("L")')
        print(rigOps_createContols)
        print(ArmOps_IKFKSwitch)

        self.create_widgets()
        self.create_layout()
        # self.create_connections()

        # getting rid of the question mark
        if sys.version_info.major >= 3:
            return self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        else:
            return self.setWindowFlags(
                self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint
            )

        self.tools = ToolOps_scriptMenu()

    # Creating widgets

    def create_widgets(self):

        self.idk_lb = QtWidgets.QLabel("Scripts")

        # self.scripts_lw = QtWidgets.QListWidget()
        # self.scripts_lw.addItem(rigOps_createContols.rigOps_createContols())
        # self.scripts_lw.addItem('hello')

        self.Execute_bn = QtWidgets.QPushButton("Execute")

        # self.toolWindow = QtWidgets.QSpinBox()
        # self.twist_sb.setFixedHeight(17)
        # self.twist_sb.setFixedWidth(20)

    # Creating layouts

    def create_layout(self):

        # Create Sub Layouts
        test_box_vbox = QtWidgets.QVBoxLayout()
        # test_box_vbox.addWidget(self.scripts_lw)
        test_box_vbox.addWidget(self.idk_lb)

        # Button Layout
        Button_layout_vbox = QtWidgets.QVBoxLayout()
        Button_layout_vbox.addWidget(self.Execute_bn)
        Button_layout_vbox.addStretch()

        # Building nested layouts----------------------------------------|

        # Building Main Layout-----------------------------------------|
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(test_box_vbox)
        main_layout.addLayout(Button_layout_vbox)


"""
    # Creating connections
    def create_connections(self):

        # Creates rig buttons
        self.Execute_bn.clicked.connect(self.tools.build_guides)
        self.create_joints_btn.clicked.connect(self.tools.build_joints)
        self.create_rig_btn.clicked.connect(self.tools.build_rig)"""


class ToolOps_scriptMenu(object):

    # Initializing Variables
    def __init__(self):

        self.error = "IKFK Tool Error:"

    # Update the values from the ui window input
    def update_side(self, text):

        self.prefix = text
        if " " in self.prefix:
            self.prefix = self.prefix.replace(" ", "_")
        print(text)

    def update_type(self, rigtype):

        self.rigType = rigtype
        if " " in self.rigType:
            self.rigType = self.rigType.replace(" ", "_")
        print(rigtype)
