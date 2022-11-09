# IMPORT Python
import sys
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


class ReverseFootUI(QtWidgets.QDialog):

    # Initiallizing window Variables
    def __init__(self, parent=maya_main_window()):
        super(ReverseFootUI, self).__init__(parent)

        self.setWindowTitle("cn_ReverseFoot_Tool_v01")
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
        self.side_le.setDisabled(True)

        self.type_lb = QtWidgets.QLabel('Rig Type:')
        self.type_le = QtWidgets.QLineEdit('Reverse Foot')
        self.type_le.setDisabled(True)

        self.orientation_lb = QtWidgets.QLabel('Aim Axis:')
        self.orientation_cb = QtWidgets.QComboBox()
        self.orientation_cb.addItems(
            ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx'])
        self.orientation_cb.setCurrentIndex(1)

        self.up_lb = QtWidgets.QLabel('Secondary Axis:')
        self.up_cb = QtWidgets.QComboBox()
        self.up_cb.addItems(
            ['xup', 'xdown', 'yup', 'ydown', 'zup', 'zdown'])
        self.up_cb.setCurrentIndex(1)

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
        self.twist_lb = QtWidgets.QLabel('#')
        self.stretch_ckb = QtWidgets.QCheckBox('Stretch')
        self.stretch_ckb.setMaximumWidth(55)
        self.bend_ckb = QtWidgets.QCheckBox('Bend')
        # self.bend_ckb.setMaximumWidth(44)
        self.bend_ckb.setMinimumWidth(1000)

        self.rig = ReverseFoot()

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
        self.mirror_ckb.toggled.connect(self.rig.update_mirror)
        # self.twist_ckb.toggled.connect(self.rig.update_twist)
        self.orientation_cb.currentIndexChanged.connect(
            self.rig.update_orientation)
        self.up_cb.currentIndexChanged.connect(
            self.rig.update_up)

        # Creates rig buttons
        self.create_guides_btn.clicked.connect(self.rig.build_guides)
        self.create_joints_btn.clicked.connect(self.rig.build_joints)
        self.create_rig_btn.clicked.connect(self.rig.build_rig)

# Instance IKFK Tool


class ReverseFoot(object):

    def __init__(self):
        self.prefix = 'L'
        self.rigType = 'foot'
        self.jointOrientation = 'yzx'
        self.orientationUp = 'xdown'

        # Rig name
        self.KNEE = 'KNEE'
        self.ROOT = 'ANKLE'
        self.MID = 'BALL'
        self.End = 'TOE'
        self.BACK_BANK = 'HEEL'
        self.OUTER_BANK = 'OUTER_BANK'
        self.INNER_BANK = 'INNER_BANK'

        # Object constants
        self.GROUP = 'GRP'
        self.JOINT = 'JNT'
        self.GUIDE = 'GUIDE'
        self.OFFSET = 'OFF'
        self.CONTROL = 'CON'
    
    def update_rig_type(self): # no ui for this currently
        if self.rig_type == 'foot':
            self.KNEE = 'KNEE'
            self.ROOT = 'ANKLE'
            self.MID = 'BALL'
            self.End = 'TOE'
            self.BACK_BANK = 'HEEL'
            self.OUTER_BANK = 'OUTER_BANK'
            self.INNER_BANK = 'INNER_BANK'
        
        if self.rig_type == 'hand':
            self.KNEE = 'ELBOW'
            self.ROOT = 'WRIST'
            self.MID = 'FINGERS'
            self.End = 'TIPS'
            self.BACK_BANK = 'HEEL'
            self.OUTER_BANK = 'OUTER_BANK'
            self.INNER_BANK = 'INNER_BANK'
        

    def update_mirror(self, mirror):

        if mirror:
            self.mirror = 1
        else:
            self.mirror = 0
        print(self.mirror)

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

    # Building rig

    def create_guides(self):



        # Building guide group
        self.arm_guide_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.GROUP))
        self.foot_guide_loc_group = mc.createNode(
            'transform', name='{}_{}_LOC_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.GROUP), parent=self.arm_guide_group)
        self.foot_guide_control_group = mc.createNode(
            'transform', name='{}_{}_{}_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.CONTROL, self.GROUP), parent=self.arm_guide_group)
        self.footbase_guide_control_group = mc.createNode(
            'transform', name='{}_{}_footbaseLOC_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.GROUP), parent=self.foot_guide_control_group)

        # Building Reverse Foot locators
        self.knee_loc = mc.spaceLocator(
            name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.KNEE, self.GUIDE))[0]
        self.ankle_loc = mc.spaceLocator(
            name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.ROOT, self.GUIDE))[0]
        self.ball_loc = mc.spaceLocator(
            name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.MID, self.GUIDE))[0]
        self.toe_loc = mc.spaceLocator(
            name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.End, self.GUIDE))[0]
        self.heel_loc = mc.spaceLocator(
            name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.BACK_BANK, self.GUIDE))[0]
        self.outer_bank_loc = mc.spaceLocator(
            name='{}_{}_OUTER_BANK_{}'.format(self.prefix, self.rigType, self.OUTER_BANK, self.GUIDE))[0]
        self.inner_bank_loc = mc.spaceLocator(
            name='{}_{}_INNER_BANK_{}'.format(self.prefix, self.rigType, self.INNER_BANK, self.GUIDE))[0]

                # Creating list of all the locators
        self.loc_list = list()
        self.loc_list.append(self.knee_loc)
        self.loc_list.append(self.ankle_loc)
        self.loc_list.append(self.ball_loc)
        self.loc_list.append(self.toe_loc)
        self.loc_list.append(self.heel_loc)
        self.loc_list.append(self.outer_bank_loc)
        self.loc_list.append(self.inner_bank_loc)

        # Disable editing the locator
        for loc in self.loc_list:

            mc.setAttr((loc + '.overrideEnabled'), 1)
            mc.setAttr((loc + '.overrideDisplayType'), 2)

        # Create locator offset
        mc.setAttr('{}.t'.format(self.knee_loc),
                   0, 5, 0)
        mc.setAttr('{}.t'.format(self.ankle_loc),
                   0, 1, 0)
        mc.setAttr('{}.t'.format(self.ball_loc),
                   0, 0, 2)
        mc.setAttr('{}.t'.format(self.toe_loc),
                   0, 0, 4)
        mc.setAttr('{}.t'.format(self.heel_loc),
                   0, 0, -1)
        mc.setAttr('{}.t'.format(self.outer_bank_loc),
                   1, 0, 3)
        mc.setAttr('{}.t'.format(self.inner_bank_loc),
                   -1, 0, 3)

        # create controls to move locators
        
        self.knee_loc_control = mc.curve(n='{}_{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.KNEE, self.GUIDE, self.CONTROL), d=1, p=zbw_con.shapes['cube'])
        pc7 = mc.parentConstraint(self.knee_loc, self.knee_loc_control)
        mc.delete(pc7)
        sel = mc.listRelatives(self.knee_loc_control)[0]
        mel.eval('scale -ws -r .2 .2 .2 ;')
        
        self.root_loc_control = mc.curve(n='{}_{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.ROOT, self.GUIDE, self.CONTROL), d=1, p=zbw_con.shapes['cube'])
        pc1 = mc.parentConstraint(self.ankle_loc, self.root_loc_control)
        mc.delete(pc1)
        sel = mc.listRelatives(self.root_loc_control)[0]
        mel.eval('scale -ws -r .2 .2 .2 ;')

        self.mid_loc_control = mc.curve(n='{}_{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.MID, self.GUIDE, self.CONTROL), d=1, p=zbw_con.shapes['cube'])
        pc2 = mc.parentConstraint(self.ball_loc, self.mid_loc_control)
        mc.delete(pc2)
        sel = mc.listRelatives(self.mid_loc_control)[0]
        mel.eval('scale -ws -r .2 .2 .2 ;')

        self.end_loc_control = mc.curve(n='{}_{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.End, self.GUIDE, self.CONTROL), d=1, p=zbw_con.shapes['cube'])
        pc3 = mc.parentConstraint(self.toe_loc, self.end_loc_control)
        mc.delete(pc3)
        sel = mc.listRelatives(self.end_loc_control)[0]
        mel.eval('scale -ws -r .2 .2 .2 ;')

        self.heel_loc_control = mc.curve(n='{}_{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.BACK_BANK, self.GUIDE, self.CONTROL), d=1, p=zbw_con.shapes['cube'])
        pc4 = mc.parentConstraint(self.heel_loc, self.heel_loc_control)
        mc.delete(pc4)
        sel = mc.listRelatives(self.heel_loc_control)[0]
        mel.eval('scale -ws -r .2 .2 .2 ;')

        self.outer_bank_loc_control = mc.curve(n='{}_{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.OUTER_BANK, self.GUIDE, self.CONTROL), d=1, p=zbw_con.shapes['cube'])
        pc5 = mc.parentConstraint(self.outer_bank_loc, self.outer_bank_loc_control)
        mc.delete(pc5)
        sel = mc.listRelatives(self.outer_bank_loc_control)[0]
        mel.eval('scale -ws -r .2 .2 .2 ;')

        self.inner_bank_loc_control = mc.curve(n='{}_{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.INNER_BANK, self.GUIDE, self.CONTROL), d=1, p=zbw_con.shapes['cube'])
        pc6 = mc.parentConstraint(self.inner_bank_loc, self.inner_bank_loc_control)
        mc.delete(pc6)
        sel = mc.listRelatives(self.inner_bank_loc_control)[0]
        mel.eval('scale -ws -r .2 .2 .2 ;')

        self.lower_foot_loc_control = mc.curve(n='{}_{}_{}_{}_{}'.format(
                self.prefix, self.rigType, 'LOWER_LOC', self.GUIDE, self.CONTROL), d=1, p=zbw_con.shapes['square'])
        pc6 = mc.parentConstraint(self.root_loc_control, self.mid_loc_control, self.heel_loc_control, self.lower_foot_loc_control)
        mc.delete(pc6)
        sel = mc.listRelatives(self.inner_bank_loc_control)[0]
        
        mel.eval('rotate -r -eu -fo 0 0 90 ;')
        mel.eval('scale -ws -r 1.5 1 3 ;')

        # parenting
        mc.parent(self.knee_loc_control, self.foot_guide_control_group)
        mc.parent(self.root_loc_control, self.foot_guide_control_group)
        mc.parent(self.mid_loc_control, self.footbase_guide_control_group)
        mc.parent(self.end_loc_control, self.footbase_guide_control_group)
        mc.parent(self.heel_loc_control, self.footbase_guide_control_group)
        mc.parent(self.outer_bank_loc_control, self.footbase_guide_control_group)
        mc.parent(self.inner_bank_loc_control, self.footbase_guide_control_group)
        mc.parent(self.lower_foot_loc_control, self.foot_guide_control_group)
        mc.matchTransform(self.lower_foot_loc_control, self.heel_loc, piv=True)
        mc.parent(self.ankle_loc, self.foot_guide_loc_group)
        mc.parent(self.ball_loc, self.foot_guide_loc_group)
        mc.parent(self.toe_loc, self.foot_guide_loc_group)
        mc.parent(self.heel_loc, self.foot_guide_loc_group)
        mc.parent(self.outer_bank_loc, self.foot_guide_loc_group)
        mc.parent(self.inner_bank_loc, self.foot_guide_loc_group)
        mc.parent(self.footbase_guide_control_group, self.lower_foot_loc_control)
        mc.parentConstraint(self.knee_loc_control, self.knee_loc)
        mc.parentConstraint(self.root_loc_control, self.ankle_loc)
        mc.parentConstraint(self.mid_loc_control, self.ball_loc)
        mc.parentConstraint(self.end_loc_control, self.toe_loc)
        mc.parentConstraint(self.heel_loc_control, self.heel_loc)
        mc.parentConstraint(self.outer_bank_loc_control, self.outer_bank_loc)
        mc.parentConstraint(self.inner_bank_loc_control, self.inner_bank_loc)
        mc.parentConstraint(self.lower_foot_loc_control, self.footbase_guide_loc_group)

    def create_hierarchy(self, mirroring=0):

        if mirroring == 1 and 'L_':
            self.orig_prefix = self.prefix
            self.prefix = self.MIRROR_PREFIX
        else:
            om.MGlobal_displayError(
                'Tool Error: mirroring only supported for left (L) to right (R)')
        
        # Create hierarchy
        self.rigPart = mc.createNode(
                'transform', name='{}_{}_{}'.format(self.prefix, self.rigType, self.GROUP))

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
        
    def create_joints(self, mirroring=0):

        # Creating list of all the locators
        self.loc_list = list()
        self.loc_list.append(self.knee_loc)
        self.loc_list.append(self.ankle_loc)
        self.loc_list.append(self.ball_loc)
        self.loc_list.append(self.toe_loc)
        self.loc_list.append(self.heel_loc)
        self.loc_list.append(self.outer_bank_loc)
        self.loc_list.append(self.inner_bank_loc)


        if mirroring == 0:
            self.Init_JNT = []
            multiple = 1
            for loc in self.loc_list:

                mat = mc.xform(loc, q=True, m=True, ws=True)
                jnt = mc.joint(name='{}_{}_Rev{}_{}'.format(
                    self.prefix, self.rigType, multiple, self.JOINT))
                mc.setAttr('{}.radius'.format(jnt), .5)
                mc.xform(jnt, m=mat, ws=True)
                self.Init_JNT.append(jnt)
                multiple = multiple + 1

            mc.makeIdentity(self.Init_JNT[0],
                            a=True, t=0, r=1, s=0, n=0, pn=True)
            mc.makeIdentity(self.Init_JNT[1],
                            a=True, t=0, r=1, s=0, n=0, pn=True)
            mc.makeIdentity(self.Init_JNT[2],
                            a=True, t=0, r=1, s=0, n=0, pn=True)

            self.foot_rev_knee = self.Init_JNT[0]
            self.foot_rev_ankle = self.Init_JNT[1]
            self.foot_rev_ball = self.Init_JNT[2]
            self.foot_rev_toe = self.Init_JNT[3]
            self.foot_rev_heel = self.Init_JNT[4]
            self.foot_rev_outer_bank = self.Init_JNT[5]
            self.foot_rev_inner_bank = self.Init_JNT[6]

            # Orient joints
            mc.joint(self.Init_JNT[0], edit=True, oj=self.jointOrientation,
                        sao=self.orientationUp, ch=True, zso=True)

            mc.joint(self.Init_JNT[1], edit=True, oj=self.jointOrientation,
                        sao=self.orientationUp, ch=True, zso=True)

            mc.joint(self.Init_JNT[2], edit=True, oj='none')

            mc.joint(self.Init_JNT[3], edit=True, oj='none')

            mc.joint(self.Init_JNT[4], edit=True, oj=self.jointOrientation,
                        sao=self.orientationUp, ch=True, zso=True)

            mc.joint(self.Init_JNT[5], edit=True, oj=self.jointOrientation,
                        sao=self.orientationUp, ch=True, zso=True)

            mc.joint(self.Init_JNT[6], edit=True, oj='none')

            # parent joint chain to joint group
            mc.parent(self.foot_rev_ankle, self.rig_jnt_group)
            mc.parent(self.foot_rev_ball, self.rig_jnt_group)
            mc.parent(self.foot_rev_toe, self.rig_jnt_group)
            mc.parent(self.foot_rev_heel, self.rig_jnt_group)
            mc.parent(self.foot_rev_outer_bank, self.rig_jnt_group)
            mc.parent(self.foot_rev_inner_bank, self.rig_jnt_group)

            self.foot_skin_ankle = mc.duplicate(self.foot_rev_ankle, n=self.foot_rev_ankle.replace('Rev1', 'Skin1'))
            self.foot_skin_ball = mc.duplicate(self.foot_rev_ball, n=self.foot_rev_ankle.replace('Rev1', 'Skin2'))
            self.foot_skin_toe = mc.duplicate(self.foot_rev_toe, n=self.foot_rev_ankle.replace('Rev1', 'Skin3'))

            # Parenting joints together
            mc.parent(self.foot_skin_toe, self.foot_skin_ball)
            mc.parent(self.foot_skin_ball, self.foot_skin_ankle)

            mc.parent(self.foot_rev_outer_bank, self.foot_rev_inner_bank)
            mc.parent(self.foot_rev_heel, self.foot_rev_outer_bank)
            mc.parent(self.foot_rev_toe, self.foot_rev_heel)
            mc.parent(self.foot_rev_ball, self.foot_rev_toe)
            mc.parent(self.foot_rev_ankle, self.foot_rev_ball)



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

    def create_reverse_foot(self):
                
        mc.select(cl=1)
        

        self.foot_fk_ankle = mc.duplicate(self.foot_rev_ankle, n=self.foot_rev_ankle.replace('Rev2', 'FK1'), po = 1)
        self.foot_fk_ball = mc.duplicate(self.foot_rev_ball, n=self.foot_rev_ankle.replace('Rev2', 'FK2'), po = 1)
        self.foot_fk_toe = mc.duplicate(self.foot_rev_toe, n=self.foot_rev_ankle.replace('Rev2', 'FK3'), po = 1)

        self.foot_ik_hip = mc.duplicate(self.foot_rev_knee, n=self.foot_rev_ankle.replace('Rev2', 'IK-1'), po = 1)
        self.foot_ik_knee = mc.duplicate(self.foot_rev_knee, n=self.foot_rev_ankle.replace('Rev2', 'IK0'), po = 1)
        self.foot_ik_ankle = mc.duplicate(self.foot_rev_ankle, n=self.foot_rev_ankle.replace('Rev2', 'IK1'), po = 1)
        self.foot_ik_ball = mc.duplicate(self.foot_rev_ball, n=self.foot_rev_ankle.replace('Rev2', 'IK2'), po = 1)
        self.foot_ik_toe = mc.duplicate(self.foot_rev_toe, n=self.foot_rev_ankle.replace('Rev2', 'IK3'), po = 1)


        mc.select(self.foot_ik_hip)
        mel.eval('move -r -os -wd 2 -5 ')


        mc.parent(self.foot_ik_hip, self.ik_jnt_group)
        mc.parent(self.foot_ik_knee, self.foot_ik_hip)
        mc.parent(self.foot_ik_ankle, self.foot_ik_knee)
        mc.parent(self.foot_ik_ball, self.foot_ik_ankle)
        mc.parent(self.foot_ik_toe, self.foot_ik_ball)

        mc.delete(self.Init_JNT[0])

        mc.parent(self.foot_fk_ankle, self.fk_jnt_group)
        mc.parent(self.foot_fk_ball, self.foot_fk_ankle)
        mc.parent(self.foot_fk_toe, self.foot_fk_ball)

        self.TtB_IKS = mc.ikHandle(
            name='{}_{}_TOE_IKS'.format(
                self.prefix, self.rigType), sol='ikSCsolver', sj=self.foot_ik_ball[0], ee=self.foot_ik_toe[0])[0]

        self.BtA_IKS = mc.ikHandle(
            name='{}_{}_BALL_IKS'.format(
                self.prefix, self.rigType), sol='ikSCsolver', sj=self.foot_ik_ankle[0], ee=self.foot_ik_ball[0])[0]

        self.AtK_IKS = mc.ikHandle(
            name='{}_{}_ANKLE_IKR'.format(
                self.prefix, self.rigType), sol='ikRPsolver', sj=self.foot_ik_hip[0], ee=self.foot_ik_ankle[0])[0]
        
        # Parent the iks to the rev foot
        mc.parent(self.TtB_IKS, self.foot_rev_toe)
        mc.parent(self.BtA_IKS, self.foot_rev_ball)
        mc.parent(self.AtK_IKS, self.foot_rev_ankle)

    def get_reverse_foot_data(self, mirroring=0):
        if mirroring == 0:
            self.ankle_pos = mc.xform(self.foot_skin_ankle, q=True, t=True, ws=True)
            self.ball_pos = mc.xform(self.foot_skin_ball, q=True, t=True, ws=True)
            self.toe_pos = mc.xform(self.foot_skin_toe, q=True, t=True, ws=True)
            
            self.ankle_pos = mc.xform(self.foot_skin_ankle, q=True, t=True, ws=True)
            self.ball_pos = mc.xform(self.foot_skin_ball, q=True, t=True, ws=True)
            self.toe_pos = mc.xform(self.foot_skin_toe, q=True, t=True, ws=True)

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
        self.ankle_offset = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.ROOT, self.OFFSET), parent=self.fk_controls_group)

        self.root_control = mc.circle(
            name='{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.ROOT, self.CONTROL), nr=self.fk_control_shape_orientation)[0]
        mc.parent(self.root_control, self.root_controls_offset)
        mc.xform(self.fk_controls_group, m=self.Bnd1_mat, ws=True)






                 
        pass
    def create_asset_and_attributes():
        pass
    def make_connections():
        pass



    # Building Methods
    
    def build_guides(self):
        self.create_guides()
        
    def build_joints(self):
        self.create_hierarchy()
        self.create_joints()
        self.create_reverse_foot()
        
    def build_rig(self):
        pass
        
        if self.mirroring == 0:
            pass