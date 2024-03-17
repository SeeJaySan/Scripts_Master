# IMPORT Python
import sys
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

# IMPORT maya
from maya import cmds as mc
from maya import mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui

# IMPORT cn_ikfk scripts

import cn_autoRig

# IMPORT Third-Party
from third_party import zbw_controlShapes as zbw_con

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
class AutoHandUI(QtWidgets.QDialog):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(AutoHandUI, self).__init__(parent)

        self.setWindowTitle("cn_Hand_builder_v01")
        self.setMaximumSize(400, 250)
        self.setMinimumSize(243, 180)
        self.setGeometry((1920/10)*7.05, 1080/2-240, 300, 190)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        # getting rid of the question mark
        if sys.version_info.major >= 3:
            return self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        else:
            return self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

    # Creating widgets
    def create_widgets(self):
        self.side_lb = QtWidgets.QLabel('Side:')
        self.side_le = QtWidgets.QLineEdit('L')
        self.side_le.setMaximumWidth(25)

        self.type_lb = QtWidgets.QLabel('Rig Type:')
        self.type_le = QtWidgets.QLineEdit('Hand')
        self.type_le.setDisabled(True)

        self.orientation_lb = QtWidgets.QLabel('Aim Axis:')
        self.orientation_cb = QtWidgets.QComboBox()
        self.orientation_cb.addItems(
            ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx'])
        self.orientation_cb.setCurrentIndex(3)

        self.up_lb = QtWidgets.QLabel('Secondary Axis:')
        self.up_cb = QtWidgets.QComboBox()
        self.up_cb.addItems(
            ['xup', 'xdown', 'yup', 'ydown', 'zup', 'zdown'])
        self.up_cb.setCurrentIndex(5)

        self.jointOrientation_reverse_ckb = QtWidgets.QCheckBox('Reverse')
        self.secondaryOrientationUP_reverse_ckb = QtWidgets.QCheckBox(
            'Reverse')

        self.create_guides_btn = QtWidgets.QPushButton('Create Guides')
        self.create_joints_btn = QtWidgets.QPushButton('Create Joints')
        self.create_rig_btn = QtWidgets.QPushButton('Create Rig')

        self.rig = AutoHand()

    # Creating layouts

    def create_layout(self):

        # Create Sub Layouts
        ikfk_info_layout_form = QtWidgets.QFormLayout()
        ikfk_create_layout_form = QtWidgets.QFormLayout()
        ikfk_create_layout_form.setAlignment(QtCore.Qt.AlignCenter)
        extra_settings_layout_form = QtWidgets.QFormLayout()

        # Naming Layout
        naming_layout_hbox = QtWidgets.QHBoxLayout()
        naming_layout_hbox.addWidget(self.side_lb)
        naming_layout_hbox.addWidget(self.side_le)
        naming_layout_hbox.addWidget(self.type_lb)
        naming_layout_hbox.addWidget(self.type_le)

        # Orientatin Combo Box
        orientation_layout_gb = QtWidgets.QGroupBox()
        orientation_layout_hbox = QtWidgets.QHBoxLayout()
        orientation_layout_gb.setLayout(orientation_layout_hbox)
        orientation_layout_hbox.addWidget(self.orientation_lb)
        orientation_layout_hbox.addWidget(self.orientation_cb)
        orientation_layout_hbox.addWidget(self.up_lb)
        orientation_layout_hbox.addStretch()
        orientation_layout_hbox.addWidget(self.up_cb)

        # Button Layout
        Button_layout_vbox = QtWidgets.QVBoxLayout()
        Button_layout_vbox.addWidget(self.create_guides_btn)
        Button_layout_vbox.addStretch()
        Button_layout_vbox.addWidget(self.create_joints_btn)
        Button_layout_vbox.addStretch()
        Button_layout_vbox.addWidget(self.create_rig_btn)

        # Building nested layouts----------------------------------------|

        # Building IKFK info fields
        ikfk_info_layout_form.addRow(naming_layout_hbox)
        ikfk_info_layout_form.addRow(orientation_layout_gb)
        # ikfk_info_layout_form.addRow(aim_layout_gb)
        # ikfk_info_layout_form.addRow(Up_layout_gb)

       # extra_settings_layout_form.addRow(extra_settings_layout_hbox)

        # Building Main Layout-----------------------------------------|
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(ikfk_info_layout_form)
        main_layout.addLayout(Button_layout_vbox)

    # Creating connections

    def create_connections(self):
        ''' # Update variable values
        self.side_le.textChanged.connect(self.rig.update_side)
        self.type_le.textChanged.connect(self.rig.update_type)
        self.orientation_cb.currentIndexChanged.connect(
            self.rig.update_orientation)
        self.up_cb.currentIndexChanged.connect(
            self.rig.update_up)'''

        # Creates rig buttons
        self.create_guides_btn.clicked.connect(self.rig.create_guides)
        self.create_joints_btn.clicked.connect(self.rig.build_joints)
        self.create_rig_btn.clicked.connect(self.rig.build_rig)


class AutoHand(object):

    # Initializing Variables
    def __init__(self):

        # UI settings
        self.rigType = 'arm'
        self.prefix = 'L'
        self.orig_prefix = ''
        self.MIRROR_PREFIX = 'R'
        self.Init_JNT = []
        self.jointOrientation = 'xzy'
        self.orientationUp = 'zdown'
        self.mirror = 1
        self.twist = 1
        self.twistJointCount = 1

        # Object constants
        self.GROUP = 'GRP'
        self.JOINT = 'JNT'
        self.GUIDE = 'GUIDE'
        self.OFFSET = 'OFF'
        self.CONTROL = 'CON'

        # Rig name
        self.ROOT = 'ROOT'
        self.MID = 'MID'
        self.END = 'END'

        # Arm constants
        self.SHOULDER = 'SHOULDER'
        self.ELBOW = 'ELBOW'
        self.WRIST = 'WRIST'

        # Twist contrants
        self.RTM = 'RTM'
        self.MTE = 'MTE'

        self.arm_names = {
            'ARM': ('CLAVICLE', 'SHOULDER', 'ELBOW', 'WRIST'), }
        self.hand_names = {
            'FINGERS': {'WRIST': 'WRIST',
                        'THUMB': ('THUMB1', 'THUMB2', 'THUMB3', 'THUMBEND'),
                        'INDEX': ('THUMB1', 'INDEX2', 'INDEX3', 'INDEXEND'),
                        'MIDDLE': ('MIDDLE1', 'MIDDLE2', 'MIDDLE3', 'MIDDLEEND'),
                        'RING': ('RING1', 'RING2', 'RING3', 'RINGEND'),
                        'PINKY': ('THUMB1', 'PINKY2', 'PINKY3', 'PINKYEND')}}

        self.error = 'IKFK Tool Error:'
        self.prefix_error_check = ''
        self.rigType_error_check = ''

    # Update the values from the ui window input
    def update_side(self, text):

        self.prefix = text
        if ' ' in self.prefix:
            self.prefix = self.prefix.replace(' ', '_')
        print(text)

    def update_type(self, rigtype):

        self.rigType = rigtype
        if ' ' in self.rigType:
            self.rigType = self.rigType.replace(' ', '_')
        print(rigtype)

    def update_mirror(self, mirror):

        if mirror:
            self.mirror = 1
        else:
            self.mirror = 0
        print(self.mirror)

    def update_twist(self, twist):

        if twist:
            self.twist = 1
        else:
            self.twist = 0
        print(self.twist)

    def update_orientation(self, orientation):

        if orientation == 0:
            self.jointOrientation = 'xyz'
        elif orientation == 1:
            self.jointOrientation = 'yzx'
        elif orientation == 2:
            self.jointOrientation = 'zxy'
        elif orientation == 3:
            self.jointOrientation = 'xzy'
        elif orientation == 4:
            self.jointOrientation = 'yxz'
        elif orientation == 5:
            self.jointOrientation = 'zyx'

        print(self.jointOrientation)

    def update_up(self, up):

        if up == 0:
            self.orientationUp = 'xup'
        elif up == 1:
            self.orientationUp = 'xdown'
        elif up == 2:
            self.orientationUp = 'yup'
        elif up == 3:
            self.orientationUp = 'ydown'
        elif up == 4:
            self.orientationUp = 'zup'
        elif up == 5:
            self.orientationUp = 'zdown'

        print(self.orientationUp)

    def update_twist_joint_count(self, number):

        self.twistJointCount = number
        print(self.twistJointCount)

    def create_guides(self):
        print(1)
        self.thumb = cn_autoRig.TwoBoneIKFK()
        self.index = cn_autoRig.TwoBoneIKFK()
        self.middle = cn_autoRig.TwoBoneIKFK()
        self.ring = cn_autoRig.TwoBoneIKFK()
        self.pinky = cn_autoRig.TwoBoneIKFK()

        self.thumb.rigType = 'thumb'
        self.index.rigType = 'index'
        self.middle.rigType = 'middle'
        self.ring.rigType = 'ring'
        self.pinky.rigType = 'pinky'

        self.thumb.build_guides()
        self.index.build_guides()
        self.middle.build_guides()
        self.ring.build_guides()
        self.pinky.build_guides()

        # mc.select(cl = 1)
       # mc.select('{}.t'.format(self.thumb.root_loc_control))

        mc.setAttr('{}.t'.format(self.thumb.root_loc_control), 0, -0.5, 3)
        mc.setAttr('{}.t'.format(self.index.root_loc_control), 8.5, 1, 2.25)
        mc.setAttr('{}.t'.format(self.middle.root_loc_control), 9, 1.5, 0)
        mc.setAttr('{}.t'.format(self.ring.root_loc_control), 8.5, 1.25, -2.25)
        mc.setAttr('{}.t'.format(self.pinky.root_loc_control), 8, 1, -4.5)

        mc.setAttr('{}.r'.format(self.thumb.root_loc_control), 90, 0, 0.1)
        mc.setAttr('{}.r'.format(self.index.root_loc_control), 90, 0, 0.1)
        mc.setAttr('{}.r'.format(self.middle.root_loc_control), 90, 0, 0.1)
        mc.setAttr('{}.r'.format(self.ring.root_loc_control), 90, 0, 0.1)
        mc.setAttr('{}.r'.format(self.pinky.root_loc_control), 90, 0, 0.1)

    def build_joints(self):
        self.thumb.build_joints()
        self.index.build_joints()
        self.middle.build_joints()
        self.ring.build_joints()
        self.pinky.build_joints()

    def build_rig(self):
        self.thumb.mirror = 0
        self.index.mirror = 0
        self.middle.mirror = 0
        self.ring.mirror = 0
        self.pinky.mirror = 0

        self.thumb.twist = 0
        self.index.twist = 0
        self.middle.twist = 0
        self.ring.twist = 0
        self.pinky.twist = 0

        self.thumb.build_rig()
        self.index.build_rig()
        self.middle.build_rig()
        self.ring.build_rig()
        self.pinky.build_rig()

        # requires xzy orientation, z down

        def build_set_driven_keys():
            self.rigType = 'Hand'
            self.hand_attribute_Grp = mc.createNode(
                'transform', n='{}_{}_ATRIBUTES_GRP'.format(self.prefix, self.rigType))
            mc.addAttr(ln='Splay', at='float', k=True, dv=0, min=-15, max=15)
            mc.addAttr(ln='Curl', at='float', k=True, dv=0, min=-90, max=90)
            mc.select(self.hand_attribute_Grp)

            mc.setDrivenKeyframe(cd = self.hand_attribute_Grp +
                                 '.Curl', dv = -90,  dn = True,  at = self.thumb.root_controls_sdk + '.rotateZ')

            build_set_driven_keys()
