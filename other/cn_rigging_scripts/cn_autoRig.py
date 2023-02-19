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
class TwoBoneIKFKUI(QtWidgets.QDialog):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(TwoBoneIKFKUI, self).__init__(parent)

        self.setWindowTitle("cn_Ikfk_Tool_v01")
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
        self.type_le = QtWidgets.QLineEdit('Arm')

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

        self.extra_lb = QtWidgets.QLabel('Extra Settings:')
        self.mirror_ckb = QtWidgets.QCheckBox('Mirror')
        self.mirror_ckb.toggle()
        self.mirror_ckb.setMaximumWidth(51)
        self.twist_ckb = QtWidgets.QCheckBox('Twist')
        self.twist_ckb.setMaximumWidth(45)
        self.twist_ckb.toggle()
        self.twist_lb = QtWidgets.QLabel('#')
        self.twist_sb = QtWidgets.QSpinBox()
        self.twist_sb.setValue(1)
        self.twist_sb.setAlignment(QtCore.Qt.AlignVCenter)
        self.twist_sb.setFixedHeight(17)
        self.twist_sb.setFixedWidth(20)
        self.twist_sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.stretch_ckb = QtWidgets.QCheckBox('Stretch')
        self.stretch_ckb.setMaximumWidth(55)
        self.bend_ckb = QtWidgets.QCheckBox('Bend')
        # self.bend_ckb.setMaximumWidth(44)
        self.bend_ckb.setMinimumWidth(1000)

        self.rig = TwoBoneIKFK()

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

        # Extra Settings Layout
        extra_settings_layout_hbox = QtWidgets.QHBoxLayout()
        extra_settings_layout_hbox.addWidget(self.extra_lb)
        extra_settings_layout_hbox.addWidget(self.mirror_ckb)
        extra_settings_layout_hbox.addWidget(self.twist_ckb)
        extra_settings_layout_hbox.addWidget(self.twist_lb)
        extra_settings_layout_hbox.addWidget(self.twist_sb)
        extra_settings_layout_hbox.addWidget(self.stretch_ckb)
        extra_settings_layout_hbox.addWidget(self.bend_ckb)

        # Building nested layouts----------------------------------------|

        # Building IKFK info fields
        ikfk_info_layout_form.addRow(naming_layout_hbox)
        ikfk_info_layout_form.addRow(orientation_layout_gb)
        # ikfk_info_layout_form.addRow(aim_layout_gb)
        # ikfk_info_layout_form.addRow(Up_layout_gb)

        extra_settings_layout_form.addRow(extra_settings_layout_hbox)

        # Building Main Layout-----------------------------------------|
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(ikfk_info_layout_form)
        main_layout.addLayout(Button_layout_vbox)
        main_layout.addLayout(extra_settings_layout_form)

    # Creating connections
    def create_connections(self):

        # Update variable values
        self.side_le.textChanged.connect(self.rig.update_side)
        self.type_le.textChanged.connect(self.rig.update_type)
        self.mirror_ckb.toggled.connect(self.rig.update_mirror)
        self.twist_ckb.toggled.connect(self.rig.update_twist)
        self.twist_ckb.toggled.connect(self.hide_spinbox)
        self.twist_sb.valueChanged.connect(self.rig.update_twist_joint_count)
        self.orientation_cb.currentIndexChanged.connect(
            self.rig.update_orientation)
        self.up_cb.currentIndexChanged.connect(
            self.rig.update_up)

        # Creates rig buttons
        self.create_guides_btn.clicked.connect(self.rig.build_guides)
        self.create_joints_btn.clicked.connect(self.rig.build_joints)
        self.create_rig_btn.clicked.connect(self.rig.build_rig)

    # Show and Hide spin box
    def hide_spinbox(self, checked):
        print('this is printing')
        this = 0
        if checked == 1:
            self.twist_sb.show()
            self.twist_lb.show()
        else:
            self.twist_sb.hide()
            self.twist_lb.hide()


class TwoBoneIKFK(object):

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
        self.SDK = 'SDK'
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

    def create_guides(self, newRigtype='none'):

        if newRigtype != 'none':
            self.rigType = newRigtype

        # Checking for duplocation errors and existing rig errors
        if self.prefix == self.prefix_error_check and self.rigType == self.rigType_error_check and mc.objExists(self.rigPart):
            om.MGlobal_displayError(
                '{0} Duplicate rig error. Please change the names'.format(self.error))
            return

        # Building guide group
        self.arm_guide_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.GROUP))
        self.arm_guide_loc_group = mc.createNode(
            'transform', name='{}_{}_LOC_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.GROUP), parent=self.arm_guide_group)
        self.arm_guide_control_group = mc.createNode(
            'transform', name='{}_{}_{}_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.CONTROL, self.GROUP), parent=self.arm_guide_group)

        # Building IKFK locators
        self.root_loc = mc.spaceLocator(
            name='{}_{}_ROOT_{}'.format(self.prefix, self.rigType, self.GUIDE))[0]
        self.mid_loc = mc.spaceLocator(
            name='{}_{}_MID_{}'.format(self.prefix, self.rigType, self.GUIDE))[0]
        self.end_loc = mc.spaceLocator(
            name='{}_{}_END_{}'.format(self.prefix, self.rigType, self.GUIDE))[0]

        # Creating list of all the locators
        self.loc_list = list()
        self.loc_list.append(self.root_loc)
        self.loc_list.append(self.mid_loc)
        self.loc_list.append(self.end_loc)

        # Disable editing the locator
        for loc in self.loc_list:

            mc.setAttr((loc + '.overrideEnabled'), 1)
            mc.setAttr((loc + '.overrideDisplayType'), 2)

        # Create locator offset
        mc.setAttr('{}.t'.format(self.root_loc),
                   0, 0, 0)
        mc.setAttr('{}.t'.format(self.mid_loc),
                   5, 0, 0)
        mc.setAttr('{}.t'.format(self.end_loc),
                   10, 0, 0)

        # create controls to move locators
        self.root_loc_control = mc.circle(
            name='{}_{}_{}_{}_{}'.format(self.prefix, self.rigType, self.SHOULDER, self.GUIDE, self.CONTROL), r=2, nr=(1, 0, 0))[0]
        shoulder_PC = mc.parentConstraint(self.root_loc, self.root_loc_control)
        mc.delete(shoulder_PC)

        self.elbow_loc_control = mc.circle(
            name='{}_{}_{}_{}_{}'.format(self.prefix, self.rigType, self.ELBOW, self.GUIDE, self.CONTROL), r=2, nr=(1, 0, 0))[0]
        elbow_PC = mc.parentConstraint(self.mid_loc, self.elbow_loc_control)

        # lock incorrect second joint movements for IKFK
        #mc.setAttr(self.elbow_loc_control + '.rx', lock=True)
        #mc.setAttr(self.elbow_loc_control + '.rz', lock=True)
        #mc.setAttr(self.elbow_loc_control + '.ty', lock=True)
        mc.delete(elbow_PC)

        self.wrist_loc_control = mc.circle(
            name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.WRIST, self.GUIDE, self.CONTROL), r=2, nr=(1, 0, 0))[0]
        wrist_PC = mc.parentConstraint(self.end_loc, self.wrist_loc_control)
        #mc.setAttr(self.wrist_loc_control + '.ty', lock=True)
        mc.delete(wrist_PC)

        # parenting
        mc.parent(self.root_loc_control, self.arm_guide_control_group)
        mc.parent(self.elbow_loc_control, self.root_loc_control)
        mc.parent(self.wrist_loc_control, self.elbow_loc_control)
        mc.parent(self.root_loc, self.arm_guide_loc_group)
        mc.parent(self.mid_loc, self.arm_guide_loc_group)
        mc.parent(self.end_loc, self.arm_guide_loc_group)
        mc.parentConstraint(self.root_loc_control, self.root_loc, mo=True)
        mc.parentConstraint(self.elbow_loc_control, self.mid_loc, mo=True)
        mc.parentConstraint(self.wrist_loc_control, self.end_loc, mo=True)

        # Focus camera on guide rig
        mc.select(self.arm_guide_group)
        camera = mc.ls(cameras=True)
        mc.viewFit(camera[1])

        # elbow rotate for testing
        mc.select(self.elbow_loc_control)
        mc.rotate(y=15)
        mel.eval('rotate -r -eu -fo 0 -28.349661 0 ')

        mc.select(clear=True)

    # Create Hierarchy
    def createHierarchy(self, mirroring=0):

        if mirroring == 1 and 'L_':
            self.orig_prefix = self.prefix
            self.prefix = self.MIRROR_PREFIX
        else:
            om.MGlobal_displayError(
                'IKFK Tool: mirroring only supported for left (L) to right (R)')

        # create
        self.rigPart = mc.createNode(
            'transform', name='{}_{}_{}'.format(self.prefix, self.rigType, self.GROUP))

        if mirroring == 0:
            mc.parent('{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.GUIDE, self.GROUP), self.rigPart)

        self.rig_jnt_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.JOINT, self.GROUP), parent=self.rigPart)

        self.rig_con_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.CONTROL, self.GROUP), parent=self.rigPart)

        self.fk_jnt_group = mc.createNode(
            'transform', name='{}_{}_FK_{}_{}'.format(
                self.prefix, self.rigType, self.JOINT, self.GROUP), parent=self.rigPart)

        self.ik_jnt_group = mc.createNode(
            'transform', name='{}_{}_IK_{}_{}'.format(
                self.prefix, self.rigType, self.JOINT, self.GROUP), parent=self.rigPart)

        mc.select(cl=True)

        if mirroring == 0:
            self.rigPart_old = self.rigPart
            self.arm_jnt_group_orig = self.rig_jnt_group
            self.arm_con_group_orig = self.rig_con_group
            self.fk_jnt_group_orig = self.fk_jnt_group
            self.ik_jnt_group_orig = self.ik_jnt_group

        mc.select(cl=True)

    # Create Base Joints for IKFK

    def create_joints(self, mirroring=0):

        if mirroring == 0:
            self.Init_JNT = []
            multiple = 1
            for loc in self.loc_list:

                mat = mc.xform(loc, q=True, m=True, ws=True)
                jnt = mc.joint(name='{}_{}_Skin{}_{}'.format(
                    self.prefix, self.rigType, multiple, self.JOINT))
                mc.setAttr('{}.radius'.format(jnt), 1)
                mc.xform(jnt, m=mat, ws=True)
                self.Init_JNT.append(jnt)
                multiple = multiple + 1

            mc.makeIdentity(self.Init_JNT[0],
                            a=True, t=0, r=1, s=0, n=0, pn=True)
            mc.makeIdentity(self.Init_JNT[1],
                            a=True, t=0, r=1, s=0, n=0, pn=True)
            mc.makeIdentity(self.Init_JNT[2],
                            a=True, t=0, r=1, s=0, n=0, pn=True)

            # Orient joints
            mc.joint(self.Init_JNT[0], edit=True, oj=self.jointOrientation,
                     sao=self.orientationUp, ch=True, zso=True)

            mc.joint(self.Init_JNT[1], edit=True, oj=self.jointOrientation,
                     sao=self.orientationUp, ch=True, zso=True)

            mc.joint(self.Init_JNT[2], edit=True, oj='none')

            # parent joint chain to joint group
            mc.parent(self.Init_JNT[0], self.rig_jnt_group)

            # fix second joint orientation
            if self.jointOrientation[0] == 'x':
                mc.setAttr(self.Init_JNT[1] + '.jointOrientX', 0)
            if self.jointOrientation[0] == 'y':
                mc.setAttr(self.Init_JNT[1] + '.jointOrientY', 0)
            if self.jointOrientation[0] == 'z':
                mc.setAttr(self.Init_JNT[1] + '.jointOrientZ', 0)

            # Delete the guide group
            # mc.delete(self.arm_guide_group)
            mc.hide(self.arm_guide_group)

            mc.select(cl=True)

            # Create a warning to check orientations on joint before continuing
            om.MGlobal_displayWarning(
                'Check Joint Orientations before proceeding')

        # Mirror base joints to create IKFK on the opposing side
    def mirroring_joints(self):

        # self.old_prefix = self.prefix
        self.prefix = self.MIRROR_PREFIX

        # Clear selection
        mc.select(cl=1)

        # Create dummy joint to mirror the joints across
        mirror_joint = mc.joint(n='C_{}_mirror_dummie_{}'.format(
            self.rigType, self.JOINT))

        # Parent original joint chain to  mirror joint
        mc.parent(self.Init_JNT[0], mirror_joint)

        # Mirror original joint chain
        self.mirrored_joints = mc.mirrorJoint(
            self.Init_JNT[0], myz=True, mb=True, searchReplace=['L_', 'R_'])

        # Reparent orginal joint chain to it's group
        mc.parent(self.Init_JNT[0], self.arm_jnt_group_orig)

        # Parent mirrored joint chain to it's group
        mc.parent(self.mirrored_joints[0], self.rig_jnt_group)

        # Delete mirrored joint
        mc.delete(mirror_joint)

        # Delete the dummy orig joint
        mc.delete(self.Init_JNT[0])

    def get_bnd_joint_data(self, mirroring=0):
        if mirroring == 0:
            self.Bnd1_pos = mc.xform(self.Init_JNT[0], q=True, t=True, ws=True)
            self.Bnd2_pos = mc.xform(self.Init_JNT[1], q=True, t=True, ws=True)
            self.Bnd3_pos = mc.xform(self.Init_JNT[2], q=True, t=True, ws=True)

            self.Bnd1_mat = mc.xform(self.Init_JNT[0], q=True, m=True, ws=True)
            self.Bnd2_mat = mc.xform(self.Init_JNT[1], q=True, m=True, ws=True)
            self.Bnd3_mat = mc.xform(self.Init_JNT[2], q=True, m=True, ws=True)
        if mirroring == 1:

            self.bn_joint_1 = self.mirrored_joints[0]
            self.bn_joint_2 = self.mirrored_joints[0]
            self.bn_joint_3 = self.mirrored_joints[0]

            self.Bnd1_pos = mc.xform(
                self.mirrored_joints[0], q=True, t=True, ws=True)
            self.Bnd2_pos = mc.xform(
                self.mirrored_joints[1], q=True, t=True, ws=True)
            self.Bnd3_pos = mc.xform(
                self.mirrored_joints[2], q=True, t=True, ws=True)

            self.Bnd1_mat = mc.xform(
                self.mirrored_joints[0], q=True, m=True, ws=True)
            self.Bnd2_mat = mc.xform(
                self.mirrored_joints[1], q=True, m=True, ws=True)
            self.Bnd3_mat = mc.xform(
                self.mirrored_joints[2], q=True, m=True, ws=True)

    # Create IKFK joints and blend color connections

    def ikfkProcessdure(self, mirroring=0):

        # Create Bind joints
        if mirroring == 0:
            self.joint_radius = mc.getAttr((self.Init_JNT[0] + '.radius'))
            self.joint_radius = int(self.joint_radius)/2

            self.bn_joint_1 = mc.duplicate(self.Init_JNT[0], n='{}'.format(
                self.Init_JNT[0]).replace('Skin', 'BN'), po=1)
            mc.setAttr(self.bn_joint_1[0] + '.radius', self.joint_radius)

            self.bn_joint_2 = mc.duplicate(self.Init_JNT[1], n='{}'.format(
                self.Init_JNT[1]).replace('Skin', 'BN'), po=1)
            mc.setAttr(self.bn_joint_2[0] + '.radius', self.joint_radius)

            self.bn_joint_3 = mc.duplicate(self.Init_JNT[2], n='{}'.format(
                self.Init_JNT[2]).replace('Skin', 'BN'), po=1)
            mc.setAttr(self.bn_joint_3[0] + '.radius', self.joint_radius)
            mc.select(cl=1)

            mc.parent(self.bn_joint_3, self.bn_joint_2)
            mc.parent(self.bn_joint_2, self.bn_joint_1)

        if mirroring == 1:
            self.joint_radius = mc.getAttr(
                (self.mirrored_joints[0] + '.radius'))
            self.joint_radius = int(self.joint_radius)/2

            self.bn_joint_1 = mc.duplicate(self.mirrored_joints[0], n='{}'.format(
                self.mirrored_joints[0]).replace('Skin', 'BN'), po=1)
            mc.setAttr(self.bn_joint_1[0] + '.radius', self.joint_radius)

            self.bn_joint_2 = mc.duplicate(self.mirrored_joints[1], n='{}'.format(
                self.mirrored_joints[1]).replace('Skin', 'BN'), po=1)
            mc.setAttr(self.bn_joint_2[0] + '.radius', self.joint_radius)

            self.bn_joint_3 = mc.duplicate(self.mirrored_joints[2], n='{}'.format(
                self.mirrored_joints[2]).replace('Skin', 'BN'), po=1)
            mc.setAttr(self.bn_joint_3[0] + '.radius', self.joint_radius)
            mc.select(cl=1)

            mc.parent(self.bn_joint_3, self.bn_joint_2)
            mc.parent(self.bn_joint_2, self.bn_joint_1)

        '''
        mc.xform(self.bn_joint_1, m=self.Bnd1_mat, ws=True)
        mc.xform(self.bn_joint_2, m=self.Bnd2_mat, ws=True)
        mc.xform(self.bn_joint_3, m=self.Bnd3_mat, ws=True)'''

        # Create FK joints
        self.fk_joint_1 = mc.duplicate(self.bn_joint_1[0], n='{}'.format(
            self.bn_joint_1[0]).replace('BN', 'FK'), po=1)
        mc.setAttr(self.fk_joint_1[0] + '.radius', self.joint_radius*1.5)

        self.fk_joint_2 = mc.duplicate(self.bn_joint_2[0], n='{}'.format(
            self.bn_joint_2[0]).replace('BN', 'FK'), po=1)
        mc.setAttr(self.fk_joint_2[0] + '.radius', self.joint_radius*1.5)

        self.fk_joint_3 = mc.duplicate(self.bn_joint_3[0], n='{}'.format(
            self.bn_joint_3[0]).replace('BN', 'FK'), po=1)
        mc.setAttr(self.fk_joint_3[0] + '.radius', self.joint_radius*1.5)

        # mc.xform(self.fk_joint_1, m=self.Bnd1_mat, ws=True)
        # mc.xform(self.fk_joint_2, m=self.Bnd2_mat, ws=True)
        # mc.xform(self.fk_joint_3, m=self.Bnd3_mat, ws=True)

        # Parent FK chain together
        mc.parent(self.fk_joint_3, self.fk_joint_2)
        mc.parent(self.fk_joint_2, self.fk_joint_1)
        mc.parent(self.fk_joint_1, self.fk_jnt_group)

        # Create IK joints
        self.ik_joint_1 = mc.duplicate(self.bn_joint_1[0], n='{}'.format(
            self.bn_joint_1[0]).replace('BN', 'IK'), po=1)
        mc.setAttr(self.ik_joint_1[0] + '.radius', self.joint_radius*0.5)

        self.ik_joint_2 = mc.duplicate(self.bn_joint_2[0], n='{}'.format(
            self.bn_joint_2[0]).replace('BN', 'IK'), po=1)
        mc.setAttr(self.ik_joint_2[0] + '.radius', self.joint_radius*0.5)

        self.ik_joint_3 = mc.duplicate(self.bn_joint_3[0], n='{}'.format(
            self.bn_joint_3[0]).replace('BN', 'IK'), po=1)
        mc.setAttr(self.ik_joint_3[0] + '.radius', self.joint_radius*0.5)

        # Parent IK chain together
        mc.parent(self.ik_joint_3, self.ik_joint_2)
        mc.parent(self.ik_joint_2, self.ik_joint_1)
        mc.parent(self.ik_joint_1, self.ik_jnt_group)

        # Parent IK and FK chains groups to the rig groups
        mc.parent(self.fk_jnt_group, self.rig_jnt_group)
        mc.parent(self.ik_jnt_group, self.rig_jnt_group)

        mc.select(cl=True)

        # Creating blend color nodes

        self.root_blend_color = mc.createNode(
            'blendColors', name='{}_{}_{}_BLENDECOLOR'.format(self.prefix, self.rigType, self.ROOT))
        self.mid_blend_color = mc.createNode(
            'blendColors', name='{}_{}_{}_BLENDECOLOR'.format(self.prefix, self.rigType, self.MID))
        self.end_blend_color = mc.createNode(
            'blendColors', name='{}_{}_{}_BLENDECOLOR'.format(self.prefix, self.rigType, self.END))

        print(self.root_blend_color)

        # Connecting IKFK blender root
        rotate = 'rotate'
        mc.connectAttr(
            ('{}.{}'.format(self.fk_joint_1[0], rotate)),
            '{}.color1'.format(self.root_blend_color))
        mc.connectAttr(
            ('{}.{}'.format(self.ik_joint_1[0], rotate)),
            '{}.color2'.format(self.root_blend_color))
        mc.connectAttr(
            ('{}.output'.format(self.root_blend_color)),
            '{}.{}'.format(self.bn_joint_1[0], rotate))

        # Connecting IKFK blender mid
        mc.connectAttr(
            ('{}.{}'.format(self.fk_joint_2[0], rotate)),
            '{}.color1'.format(self.mid_blend_color))
        mc.connectAttr(
            ('{}.{}'.format(self.ik_joint_2[0], rotate)),
            '{}.color2'.format(self.mid_blend_color))
        mc.connectAttr(
            ('{}.output'.format(self.mid_blend_color)),
            '{}.{}'.format(self.bn_joint_2[0], rotate))

        # Connecting IKFK blender end
        mc.connectAttr(
            ('{}.{}'.format(self.fk_joint_3[0], rotate)),
            '{}.color1'.format(self.end_blend_color))
        mc.connectAttr(
            ('{}.{}'.format(self.ik_joint_3[0], rotate)),
            '{}.color2'.format(self.end_blend_color))
        mc.connectAttr(
            ('{}.output'.format(self.end_blend_color)),
            '{}.{}'.format(self.bn_joint_3[0], rotate))

    # Creaing FK controls
    def create_fk_controls(self):

        # Create FK Controls
        self.fk_controls_group = mc.createNode(
            'transform', name='{}_{}_FKControls_{}'.format(
                self.prefix, self.rigType, self.GROUP))

        # Color controlers
        mc.setAttr((self.fk_controls_group + '.overrideEnabled'), 1)

        if 'L_' in (self.fk_controls_group):
            mc.setAttr((self.fk_controls_group + '.overrideColor'), 6)
        elif 'R_' in (self.fk_controls_group):
            mc.setAttr((self.fk_controls_group + '.overrideColor'), 13)
        else:
            mc.setAttr((self.fk_controls_group + '.overrideColor'), 17)

        # Variable for correcting control shape depending on joint orientation
        if self.jointOrientation[0] == 'x':
            self.fk_control_shape_orientation = (1, 0, 0)
        elif self.jointOrientation[0] == 'y':
            self.fk_control_shape_orientation = (0, 1, 0)
        elif self.jointOrientation[0] == 'z':
            self.fk_control_shape_orientation = (0, 0, 1)

        # Root node group and control
        self.root_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.ROOT, self.OFFSET), parent=self.fk_controls_group)
        self.root_controls_sdk = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.ROOT, self.SDK), parent=self.root_controls_offset)

        self.root_control = mc.circle(
            name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.ROOT, self.CONTROL), nr=self.fk_control_shape_orientation)[0]
        mc.parent(self.root_control, self.root_controls_sdk)
        mc.xform(self.fk_controls_group, m=self.Bnd1_mat, ws=True)

        # Mid node group and control
        self.mid_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.MID, self.OFFSET), parent=self.root_control)
        self.mid_controls_sdk = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.MID, self.SDK), parent=self.mid_controls_offset)

        self.mid_control = mc.circle(
            name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.MID, self.CONTROL), nr=self.fk_control_shape_orientation)[0]

        mc.parent(self.mid_control, self.mid_controls_sdk)
        mc.xform(self.mid_controls_offset, m=self.Bnd2_mat, ws=True)
        mc.xform(self.mid_control, m=self.Bnd2_mat, ws=True)

        # End node group and control
        self.end_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.END, self.OFFSET), parent=self.mid_control)
        self.end_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.END, self.SDK), parent=self.end_controls_offset)
        self.end_control = mc.circle(name='{}_{}_{}_{}'.format(
            self.prefix, self.rigType, self.END, self.CONTROL), nr=self.fk_control_shape_orientation)[0]

        mc.parent(self.end_control, self.end_controls_offset)
        mc.xform(self.end_controls_offset, m=self.Bnd3_mat, ws=True)
        mc.xform(self.end_control, m=self.Bnd3_mat, ws=True)

        # Parenting contorls to joints
        mc.parentConstraint(self.root_control, self.fk_joint_1, mo=True)
        mc.parentConstraint(self.mid_control, self.fk_joint_2, mo=True)
        mc.parentConstraint(self.end_control, self.fk_joint_3, mo=True)

        # Parenting groups into main heirarchy
        mc.parent(self.fk_controls_group, self.rig_con_group)

    def create_ik_controls(self):

        # Create groups
        self.IK_wrist_GRP = mc.createNode(
            'transform', name='{}_{}_IKControls_{}'.format(
                self.prefix, self.rigType, self.GROUP))
        self.IK_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.WRIST, self.OFFSET, self.GROUP), parent=self.IK_wrist_GRP)

        # Color controlers

        mc.setAttr((self.IK_wrist_GRP + '.overrideEnabled'), 1)

        if 'L_' in (self.IK_wrist_GRP):
            mc.setAttr((self.IK_wrist_GRP + '.overrideColor'), 6)
        elif 'R_' in self.IK_wrist_GRP:
            mc.setAttr((self.IK_wrist_GRP + '.overrideColor'), 13)
        else:
            mc.setAttr((self.IK_wrist_GRP + '.overrideColor'), 17)

    # Create IK Handle
        self.IKR_Handle = mc.ikHandle(
            name='{}_{}_IKR'.format(
                self.prefix, self.rigType), sol='ikRPsolver', sj=self.ik_joint_1[0], ee=self.ik_joint_3[0])[0]

        # Create Control
        self.IKR_wrist_control = mc.curve(n='{}_{}_{}'.format(
            self.prefix, self.rigType, self.CONTROL), d=1, p=zbw_con.shapes['cube'])

        # Parenting
        mc.xform(self.IK_wrist_GRP, m=self.Bnd3_mat, ws=True)
        mc.xform(self.IKR_wrist_control, m=self.Bnd3_mat, ws=True)
        mc.parent(self.IK_wrist_GRP, self.rig_con_group)
        mc.parent(self.IKR_wrist_control, self.IK_controls_offset)
        mc.parent(self.IKR_Handle, self.IKR_wrist_control)

    # Creating pole target
    def create_pole_target(self, distance=1.0):

        root_joint_pos = mc.xform(self.ik_joint_1, q=1, ws=1, t=1)
        mid_joint_pos = mc.xform(self.ik_joint_2, q=1, ws=1, t=1)
        end_joint_pos = mc.xform(self.ik_joint_3, q=1, ws=1, t=1)

        # Create locator at the vector position and create pole vector constraint
        def create_pv(pos):

            # create pole vector shape
            pv_group = mc.createNode('transform', name='{}_{}_PV_{}'.format(
                self.prefix, self.rigType, self.GROUP))

            self.pv_control = mc.curve(n='{}_{}_PV_{}'.format(
                self.prefix, self.rigType, self.CONTROL), d=1, p=zbw_con.shapes['cube'])

            # Color controlers
            mc.setAttr((pv_group + '.overrideEnabled'), 1)
            if 'L_' in ('{}_{}_PV_{}'.format(self.prefix, self.rigType, self.GROUP)):
                mc.setAttr((pv_group + '.overrideColor'), 6)
            elif 'R_' in ('{}_{}_PV_{}'.format(self.prefix, self.rigType, self.GROUP)):
                mc.setAttr((pv_group + '.overrideColor'), 13)
            else:
                mc.setAttr((pv_group + '.overrideColor'), 17)

            # Parent and move controll
            mc.parent(self.pv_control, pv_group)
            mc.move(pos.x, pos.y, pos.z, pv_group)
            mc.poleVectorConstraint(
                self.pv_control, self.IKR_Handle)
            mc.parent(pv_group, self.rig_con_group)

        # Get pole vector position
        def get_pole_vec_pos(root_pos, mid_pos, end_pos):

            root_joint_vec = om.MVector(root_pos[0], root_pos[1], root_pos[2])
            mid_joint_vec = om.MVector(mid_pos[0], mid_pos[1], mid_pos[2])
            end_joint_vec = om.MVector(end_pos[0], end_pos[1], end_pos[2])

            # Getting vectors of the joint chain
            line = (end_joint_vec - root_joint_vec)
            point = (mid_joint_vec - root_joint_vec)

            # MVector automatically does the dot product((line.length*point.length)cos theta)
            # MVector adds the cos automatically
            scale_value = (line*point) / (line * line)
            proj_vec = line * scale_value + root_joint_vec

            root_to_mid_len = (mid_joint_vec - root_joint_vec).length()
            mid_to_end_len = (end_joint_vec - mid_joint_vec).length()
            total_len = (root_to_mid_len + mid_to_end_len)

            pole_vec_pos = (mid_joint_vec - proj_vec).normal() * \
                distance * total_len + mid_joint_vec

            create_pv(pole_vec_pos)

        get_pole_vec_pos(root_joint_pos, mid_joint_pos, end_joint_pos)

    # Create twist joints for the skin joints

    def create_twist_joints(self):

        # If twist is set to 1, add  twist joints to the chain
        if self.twist == 1:

            # Throw an error if twist_joint_count is less than 1 of greater than 5
            if self.twistJointCount < 1 or self.twistJointCount > 5:
                om.MGlobal_displayError(
                    'IKFK Tool: Too many or too few twist joints. 1-5 only')

        # Vector values for twist joints
        root_twist_xform = mc.xform(
            self.Init_JNT[0], q=True, ws=True, t=True)
        mid_twist_xform = mc.xform(
            self.Init_JNT[1], q=True, ws=True, t=True)
        end_twist_xform = mc.xform(
            self.Init_JNT[2], q=True, ws=True, t=True)

        root_twist_vec = om.MVector(
            root_twist_xform[0], root_twist_xform[1], root_twist_xform[2])
        mid_twist_vec = om.MVector(
            mid_twist_xform[0], mid_twist_xform[1], mid_twist_xform[2])
        end_twist_vec = om.MVector(
            end_twist_xform[0], end_twist_xform[1], end_twist_xform[2])

        self.twist_joint_rtm_ik_1 = mc.joint(n='{}_{}_{}_Twist_Skin{}_{}'.format(
            self.prefix, self.rigType, self.RTM, self.ROOT, self.JOINT), rad=self.joint_radius*2)
        self.twist_joint_rtm_ik_2 = mc.joint(n='{}_{}_{}_Twist_Skin{}_{}'.format(
            self.prefix, self.rigType, self.RTM, self.MID, self.JOINT), rad=self.joint_radius*2)
        mc.select(cl=True)
        self.twist_joint_mte_ik_1 = mc.joint(n='{}_{}_{}_Twist_Skin{}_{}'.format(
            self.prefix, self.rigType, self.MTE, self.MID, self.JOINT), rad=self.joint_radius*2)
        self.twist_joint_mte_ik_2 = mc.joint(n='{}_{}_{}_Twist_Skin{}_{}'.format(
            self.prefix, self.rigType, self.MTE, self.END, self.JOINT), rad=self.joint_radius*2)

        mc.xform(self.twist_joint_rtm_ik_1, m=self.Bnd1_mat, ws=True)
        mc.xform(self.twist_joint_rtm_ik_2, m=self.Bnd1_mat, ws=True)
        mc.xform(self.twist_joint_rtm_ik_2, t=self.Bnd2_pos, ws=True)
        mc.select(cl=True)

        mc.xform(self.twist_joint_mte_ik_1, m=self.Bnd2_mat, ws=True)
        mc.xform(self.twist_joint_mte_ik_2, m=self.Bnd3_mat, ws=True)
        # mc.xform(self.twist_joint_mte_ik_2, t=end_pos, ws=True)

        # Get the vector from root joint to mid joint
        root_to_mid_vec = mid_twist_vec - root_twist_vec
        mid_to_end_vec = end_twist_vec - mid_twist_vec

        # Create multiplier to iterate through move than one twist joint
        tJC = self.twistJointCount + 1
        rtm_multiple = self.twistJointCount
        mte_multiple = self.twistJointCount
        root_to_mid_joint_locations = []
        mid_to_end_joint_locations = []

        # Get positions of the twist joints from the root to mid.
        # Dependent on the specified number of twist joints
        for i in range(self.twistJointCount):

            # Interate through positions depending of the amount of twist joints.
            # Cycle through the positions
            joint_location = (
                (root_to_mid_vec - ((root_to_mid_vec/tJC)
                                    * rtm_multiple)) + root_twist_vec
            )

            root_to_mid_joint_locations.append(joint_location)
            rtm_multiple = rtm_multiple - 1

        # Get positions of the twist joints from the mid to end.
        # Dependent on the specified number of twist joints
        for i in range(self.twistJointCount):

            # Interate through positions depending of the amount of twist joints.
            # Cycle through the positions
            joint_location = (
                (mid_to_end_vec - ((mid_to_end_vec/tJC)
                                   * mte_multiple)) + mid_twist_vec
            )

            mid_to_end_joint_locations.append(joint_location)
            mte_multiple = mte_multiple - 1

        rtm_twist_joints = []
        mte_twist_joints = []

        rtm_multiple = self.twistJointCount
        mte_multiple = self.twistJointCount

        # Create joints from the root to mid
        for i in root_to_mid_joint_locations:

            jnt = mc.joint(n='{}_{}_{}_Twist_Skin{}_{}'.format(
                self.prefix, self.rigType, self.RTM, rtm_multiple, self.JOINT))
            mc.xform(jnt, m=self.Bnd1_mat, ws=True)
            mc.move(i.x, i.y, i.z, jnt)
            rtm_multiple = rtm_multiple + 1
            mc.select(cl=True)
            rtm_twist_joints.append(jnt)

        # Create joints from the mid to end
        for i in mid_to_end_joint_locations:

            jnt = mc.joint(n='{}_{}_{}_Twist_Skin{}_{}'.format(
                self.prefix, self.rigType, self.MTE, mte_multiple, self.JOINT))
            mc.xform(jnt, m=self.Bnd2_mat, ws=True)
            mc.move(i.x, i.y, i.z, jnt)
            mte_multiple = mte_multiple + 1
            mc.select(cl=True)
            mte_twist_joints.append(jnt)

        for i in rtm_twist_joints:
            # Need to fix naming error before I can parent joints to root
            mc.parent(i, self.Init_JNT[0])
            pass

    # Create container as an asset and add IKFK switch attribute to the asset
    def create_asset_and_attributes(self):

        self.ikfk_attributes_Grp = mc.createNode(
            'transform', name='{}_{}_ATRIBUTES_GRP'.format(self.prefix, self.rigType))
        mc.addAttr(ln='IKFK_Switch', at='float',
                   k=True,  min=0, max=1)

        self.arm_attributes_asset = mc.container(
            name='{}_{}_ASSET'.format(self.prefix, self.rigType))

        mc.parent(self.ikfk_attributes_Grp, self.rigPart)
        mc.container(self.arm_attributes_asset, e=True, ish=True,
                     f=True, an=self.ikfk_attributes_Grp)

    # Make connections from the asset to the asset
    def make_connections(self):

        # IKFK switch
        IKFK_reverse = mc.createNode(
            'reverse', n='{}_{}_IKFK_reverse'.format(self.prefix, self.rigType))

        # Add controls to the asset
        mc.container(self.arm_attributes_asset, edit=True,
                     addNode=self.root_control)
        mc.container(self.arm_attributes_asset, edit=True,
                     addNode=self.mid_control)
        mc.container(self.arm_attributes_asset, edit=True,
                     addNode=self.end_control)
        mc.container(self.arm_attributes_asset, edit=True,
                     addNode=self.IKR_wrist_control)
        mc.container(self.arm_attributes_asset, edit=True,
                     addNode=self.pv_control)

        # Publish name 'IKFK Switch'
        mc.container(self.arm_attributes_asset, e=True, pn=('IKFK_Switch'))

        # Bind ikfk attribute from the group to the container asset
        mc.container(self.arm_attributes_asset, e=True, ba=(
            self.ikfk_attributes_Grp + '.IKFK_Switch', 'IKFK_Switch'))

        # Connect attribute to the reverse
        mc.connectAttr(self.ikfk_attributes_Grp + '.IKFK_Switch',
                       IKFK_reverse + '.input.inputX')

        # Connect the reverse to the blend color nodes
        mc.connectAttr(IKFK_reverse + '.input.inputX',
                       self.root_blend_color + '.blender')
        mc.connectAttr(IKFK_reverse + '.input.inputX',
                       self.mid_blend_color + '.blender')
        mc.connectAttr(IKFK_reverse + '.input.inputX',
                       self.end_blend_color + '.blender')

        # Create visibility depending on ik or fk
        self.arm_control_vis_condition = mc.shadingNode(
            'condition', n='{}_{}_control_vis_condition'.format(self.prefix, self.rigType), au=True)
        mc.setAttr(self.arm_control_vis_condition + '.colorIfTrueR', 0)
        mc.setAttr(self.arm_control_vis_condition + '.colorIfTrueG', 1)
        mc.setAttr(self.arm_control_vis_condition + '.colorIfTrueB', 0)
        mc.setAttr(self.arm_control_vis_condition + '.colorIfFalseR', 1)
        mc.setAttr(self.arm_control_vis_condition + '.colorIfFalseG', 0)
        mc.setAttr(self.arm_control_vis_condition + '.colorIfFalseB', 0)
        mc.setAttr(self.arm_control_vis_condition + '.secondTerm', 1)

        mc.connectAttr(self.arm_attributes_asset + '.IKFK_Switch',
                       self.arm_control_vis_condition + '.firstTerm')

        mc.connectAttr(self.arm_control_vis_condition + '.outColor.outColorR',
                       self.IKR_wrist_control + '.visibility')

        mc.connectAttr(self.arm_control_vis_condition + '.outColor.outColorR',
                       self.pv_control + '.visibility')

        mc.connectAttr(self.arm_control_vis_condition + '.outColor.outColorG', 
                       self.root_control + '.visibility')
        mc.connectAttr(self.arm_control_vis_condition + '.outColor.outColorG',
                       self.mid_control + '.visibility')
        mc.connectAttr(self.arm_control_vis_condition + '.outColor.outColorG',
                       self.end_control + '.visibility')

    def IKFK_snap_expression(self):  # NOT WORKING

        self.init_dist = 200
        scale_distance_node = mc.createNode(
            'distanceBetween', n='{}_{}_distanceBetween'.format(self.prefix, self.rigType))
        mc.addAttr(self.IKR_wrist_control, at='float',
                   ln='Stretch', k=True, min=0, max=1)
        mc.addAttr(self.IKR_wrist_control, at='float',
                   ln='ShortArm', k=True)
        mc.expression(n='{}_{}_IkfkSnap'.format(self.prefix, self.rigType), ae=True, s='''
                      $distance = {0}.distance ;
                      $initialDis = {1};
                      $factor = $distance/$initialDis ;
                      {2}_{3}_IK1_{4}.scaleX = $factor ;
                      {2}_{3}_IK2_{4}.scaleX = $factor ;
                      $envelope = {5}.Stretch ;
                      $switch = (1-{5}.ShortArm) ;
                      {2}_{3}_IK1_{4}.scaleX = (1-$envelope)+(clamp($switch,10,$factor)*$envelope) ;
                      {2}_{3}_IK2_{4}.scaleX = (1-$envelope)+(clamp($switch,10,$factor)*$envelope) ;'''.format(
            scale_distance_node, self.init_dist, self.prefix, self.rigType, self.JOINT, self.IKR_wrist_control))

    # IKFK Build Methods-----------------------------------|

    # Build guides
    def build_guides(self):

        self.create_guides()

    # Build joints
    def build_joints(self):

        self.createHierarchy()
        self.create_joints()

    # Build Rig
    def build_rig(self):
        self.get_bnd_joint_data()
        self.ikfkProcessdure()

        # If twist is checked, create twist joints for the IKFK chain
        if self.twist == 1:
            self.create_twist_joints()

        self.create_fk_controls()
        self.create_ik_controls()
        self.create_pole_target()
        self.create_asset_and_attributes()
        self.make_connections()
        # FIXME self.IKFK_snap_expression()
        # TODO: self.create_ribbon_bend_joints()
        # TODO: self.create_stretch()

        # If mirror is checked, mirror the rig across the YZ plain.
        if self.mirror == 1:

            # Throw an error if anyhting other than 'L' equal self.prefix
            if self.prefix == 'L':
                pass
            else:
                om.MGlobal_displayError(
                    'IKFK Tool: mirroring only supported for left (L) to right (R)')
                return

            # Start building the mirror
            self.createHierarchy(mirroring=1)
            self.mirroring_joints()
            self.get_bnd_joint_data(mirroring=1)
            self.ikfkProcessdure(mirroring=1)

            # If twist is checked, create twist joints for the IKFK chain
            if self.twist == 1:
                self.create_twist_joints()

            self.create_fk_controls()
            self.create_ik_controls()
            self.create_pole_target()
            self.create_asset_and_attributes()
            self.make_connections()
            self.prefix = self.orig_prefix