# IMPORT_Python
import sys
import pprint as pp
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

# IMPORT_maya
import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omui # e402

# IMPORT_Third-Party
from third_party import zbw_controlShapes as zbw_con

# REDOING THE CODE


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class TwoBoneIKFKUI(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TwoBoneIKFKUI, self).__init__(parent)

        self.setWindowTitle("IKFK_v01")
        self.setMinimumSize(100, 50)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        # getting rid of the question mark
        if sys.version_info.major >= 3:
            return self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        else:
            return self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

    def create_widgets(self):
        self.side_le = QtWidgets.QLineEdit('L')
        self.type_le = QtWidgets.QLineEdit('Arm')

        self.orientation_cb = QtWidgets.QComboBox()
        self.orientation_cb.addItems(
            ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx'])
            
        self.jointOrientation_X_rb = QtWidgets.QRadioButton('X')
        self.jointOrientation_Y_rb = QtWidgets.QRadioButton('Y')
        self.jointOrientation_Z_rb = QtWidgets.QRadioButton('Z')

        self.secondaryOrientationUP_X_rb = QtWidgets.QRadioButton('X')
        self.secondaryOrientationUP_Y_rb = QtWidgets.QRadioButton('Y')
        self.secondaryOrientationUP_Z_rb = QtWidgets.QRadioButton('Z')

        self.jointOrientation_reverse_ckb = QtWidgets.QCheckBox('Reverse')
        self.secondaryOrientationUP_reverse_ckb = QtWidgets.QCheckBox(
            'Reverse')

        self.create_guides_btn = QtWidgets.QPushButton('Create Guides')
        self.create_joints_btn = QtWidgets.QPushButton('Create Joints')
        self.create_rig_btn = QtWidgets.QPushButton('Create Rig')

        self.mirror_ckb = QtWidgets.QCheckBox('Mirror')
        self.stretch_ckb = QtWidgets.QCheckBox('Stretch')
        self.twist_ckb = QtWidgets.QCheckBox('twist joints')

        self.rig = TwoBoneIKFK(orientation=self.orientation_cb)

    # Create Layouts
    def create_layout(self):
        # Create Sub Layouts
        box1 = QtWidgets.QVBoxLayout()

        general_layout = QtWidgets.QFormLayout()
        aim_form_layout = QtWidgets.QFormLayout()
        Up_form_layout = QtWidgets.QFormLayout()
        extra_options_form_layout = QtWidgets.QFormLayout()

        side_layout = QtWidgets.QVBoxLayout()
        general_layout.addRow('Side label:', side_layout)
        side_layout.addWidget(self.side_le)

        type_layout = QtWidgets.QVBoxLayout()
        general_layout.addRow('Rig Type:', type_layout)
        type_layout.addWidget(self.type_le)

        joint_aim_layout = QtWidgets.QHBoxLayout()
        aim_form_layout.addRow('Aim Axis:', joint_aim_layout)
        joint_aim_layout.addWidget(self.jointOrientation_X_rb)
        joint_aim_layout.addWidget(self.jointOrientation_Y_rb)
        joint_aim_layout.addWidget(self.jointOrientation_Z_rb)
        joint_aim_layout.addWidget(self.jointOrientation_reverse_ckb)

        joint_UP_layout = QtWidgets.QHBoxLayout()
        Up_form_layout.addRow('Up Axis: ', joint_UP_layout)
        joint_UP_layout.addWidget(self.secondaryOrientationUP_X_rb)
        joint_UP_layout.addWidget(self.secondaryOrientationUP_Y_rb)
        joint_UP_layout.addWidget(self.secondaryOrientationUP_Z_rb)
        joint_UP_layout.addWidget(self.secondaryOrientationUP_reverse_ckb)

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.create_guides_btn)
        button_layout.addWidget(self.create_joints_btn)
        button_layout.addWidget(self.create_rig_btn)
        # button_layout.addWidget(self.orientation_cb)

        extra_options_layout = QtWidgets.QHBoxLayout()
        extra_options_form_layout.addRow('EX: ', extra_options_layout)
        extra_options_layout.addWidget(self.mirror_ckb)
        extra_options_layout.addWidget(self.stretch_ckb)
        extra_options_layout.addWidget(self.twist_ckb)

        box1.addLayout(general_layout)

        # Create Main Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(box1)
        main_layout.addLayout(aim_form_layout)
        main_layout.addLayout(Up_form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(extra_options_form_layout)

    def create_connections(self):
        # update varible values
        self.side_le.textChanged.connect(self.rig.update_side)
        self.type_le.textChanged.connect(self.rig.update_type)
        self.mirror_ckb.toggled.connect(self.rig.update_mirror)

        self.orientation_cb.activated[str].connect(self.combo_box_print)

        # creates rig
        self.create_guides_btn.clicked.connect(self.rig.build_guides)
        self.create_joints_btn.clicked.connect(self.rig.build_joints)
        self.create_rig_btn.clicked.connect(self.rig.build_rig)

    def print_side_le(self):
        side_label = self.side_le.text()
        print(side_label)

    @QtCore.Slot(str)
    def combo_box_print(self, text):
        print(text)

    def mirror_check(self, mirror):
        if mirror:
            print('something is happening')


class TwoBoneIKFK(object):  # not working

    def __init__(self, orientation):
        self.rigType = 'arm'
        self.side = None
        self.prefix = 'L'
        self.jointOrientation = orientation
        self.mirror = 0

        # object constants
        self.GROUP = 'GRP'
        self.JOINT = 'JNT'
        self.GUIDE = 'GUIDE'
        self.OFFSET = 'OFF'
        self.CONTROL = 'CON'

        # arm constants
        self.CLAVICLE = 'CLAVICLE'
        self.SHOULDER = 'SHOULDER'
        self.ELBOW = 'ELBOW'
        self.WRIST = 'WRIST'

        self.arm_names = {
            'ARM': ('CLAVICLE', 'SHOULDER', 'ELBOW', 'WRIST'), }
        self.hand_names = {
            'FINGERS': {'WRIST': 'WRIST',
                        'THUMB': ('THUMB1', 'THUMB2', 'THUMB3', 'THUMBEND'),
                        'INDEX': ('THUMB1', 'INDEX2', 'INDEX3', 'INDEXEND'),
                        'MIDDLE': ('MIDDLE1', 'MIDDLE2', 'MIDDLE3', 'MIDDLEEND'),
                        'RING': ('RING1', 'RING2', 'RING3', 'RINGEND'),
                        'PINKY': ('THUMB1', 'PINKY2', 'PINKY3', 'PINKYEND')}}

    # update the values from the ui window
    def update_side(self, text):
        self.prefix = text
        print(text)

    def update_type(self, rigtype):
        self.rigType = rigtype
        print(rigtype)

    def update_mirror(self, mirror):
        if mirror:
            self.mirror = 1
        else:
            self.mirror = 0
        print(self.mirror)

    def create_guides(self):

        # build guide group
        arm_guide_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.GROUP))
        arm_guide_up_group = mc.createNode(
            'transform', name='{}_{}_UP_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.GROUP), parent=arm_guide_group)
        mc.hide(arm_guide_up_group)
        arm_guide_loc_group = mc.createNode(
            'transform', name='{}_{}_LOC_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.GROUP), parent=arm_guide_group)
        arm_guide_control_group = mc.createNode(
            'transform', name='{}_{}_{}_{}_{}'.format(self.prefix, self.rigType, self.GUIDE, self.CONTROL, self.GROUP), parent=arm_guide_group)

        # build locators for the arm
        loc_list = list()
        shoulder_loc = mc.spaceLocator(
            name='{}_{}_Shoulder_{}'.format(self.prefix, self.rigType, self.GUIDE))[0]
        elbow_loc = mc.spaceLocator(
            name='{}_{}_Elbow_{}'.format(self.prefix, self.rigType, self.GUIDE))[0]
        wrist_loc = mc.spaceLocator(
            name='{}_{}_Wrist_{}'.format(self.prefix, self.rigType, self.GUIDE))[0]

        loc_list.append(shoulder_loc)
        loc_list.append(elbow_loc)
        loc_list.append(wrist_loc)

        # disable editing the locator
        for loc in loc_list:

            mc.setAttr((loc + '.overrideEnabled'), 1)
            mc.setAttr((loc + '.overrideDisplayType'), 2)

        # create locator offset
        mc.setAttr('{}.t'.format(shoulder_loc),
                   0, 0, 0)
        mc.setAttr('{}.t'.format(elbow_loc),
                   5, 0, 0)
        mc.setAttr('{}.t'.format(wrist_loc),
                   10, 0, 0)

        # duplicate locs for orientation
        shoulder_up = mc.duplicate(
            shoulder_loc, n=shoulder_loc.replace('self.SHOULDER', 'Shoulder_up'))[0]
        elbow_up = mc.duplicate(
            elbow_loc, n=elbow_loc.replace('self.ELBOW', 'Elbow_up'))[0]
        wrist_up = mc.duplicate(
            wrist_loc, n=wrist_loc.replace('self.WRIST', 'Wrist_up'))[0]

        # create locator offset
        mc.setAttr('{}.t'.format(shoulder_up),
                   0, 2, 0)
        mc.setAttr('{}.t'.format(elbow_up),
                   5, 2, 0)
        mc.setAttr('{}.t'.format(wrist_up),
                   10, 2, 0)

        # create controls to move locators
        shoulder_loc_control = mc.circle(
            name='{}_{}_{}_{}'.format(self.prefix, self.SHOULDER, self.GUIDE, self.CONTROL), r=2, nr=(1, 0, 0))[0]
        shoulder_PC = mc.parentConstraint(shoulder_loc, shoulder_loc_control)
        mc.delete(shoulder_PC)

        elbow_loc_control = mc.circle(
            name='{}_{}_{}_{}'.format(self.prefix, self.ELBOW, self.GUIDE, self.CONTROL), r=2, nr=(1, 0, 0))[0]
        elbow_PC = mc.parentConstraint(elbow_loc, elbow_loc_control)
        mc.setAttr(elbow_loc_control + '.rx', lock=True)
        mc.setAttr(elbow_loc_control + '.rz', lock=True)
        mc.setAttr(elbow_loc_control + '.ty', lock=True)

        mc.delete(elbow_PC)

        wrist_loc_control = mc.circle(
            name='{}_{}_{}_{}'.format(self.prefix, self.WRIST, self.GUIDE, self.CONTROL), r=2, nr=(1, 0, 0))[0]
        wrist_PC = mc.parentConstraint(wrist_loc, wrist_loc_control)
        mc.setAttr(wrist_loc_control + '.ty', lock=True)
        mc.delete(wrist_PC)

        # parenting
        mc.parent(shoulder_loc_control, arm_guide_control_group)
        mc.parent(elbow_loc_control, shoulder_loc_control)
        mc.parent(wrist_loc_control, elbow_loc_control)
        mc.parent(shoulder_loc, arm_guide_loc_group)
        mc.parent(elbow_loc, arm_guide_loc_group)
        mc.parent(wrist_loc, arm_guide_loc_group)
        mc.parent(shoulder_up, arm_guide_up_group)
        mc.parent(elbow_up, arm_guide_up_group)
        mc.parent(wrist_up, arm_guide_up_group)
        mc.parentConstraint(shoulder_loc_control, shoulder_loc, mo=True)
        mc.parentConstraint(elbow_loc_control, elbow_loc, mo=True)
        mc.parentConstraint(wrist_loc_control, wrist_loc, mo=True)
        mc.parentConstraint(shoulder_loc_control, shoulder_up, mo=True)
        mc.parentConstraint(elbow_loc_control, elbow_up, mo=True)
        mc.parentConstraint(wrist_loc_control, wrist_up, mo=True)

        mc.select(clear=True)

    # return the locators in the loc group
    def arm_guides(self):

        grp = '{}_{}_LOC_{}_{}'.format(
            self.prefix, self.rigType, self.GUIDE, self.GROUP)

        return [loc for loc in mc.listRelatives(grp) if mc.objExists(grp)]

    # return the joints in the joint group
    def arm_joints(self):

        grp = '{}_{}_{}_{}'.format(
            self.prefix, self.rigType, self.JOINT, self.GROUP)

        return [jnt for jnt in mc.listRelatives(grp, ad=True) if mc.objExists(grp)]

    # Create Hierarchy
    def createHierarchy(self):
        # if not self.rig_Group:
        #    self.rig_Group = mc.createNode()

        self.rigPart = mc.createNode(
            'transform', name='{}_{}_{}'.format(self.side, self.rigType, self.GROUP))
        mc.parent('{}_{}_{}_{}'.format(
            self.prefix, self.rigType, self.GUIDE, self.GROUP), self.rigPart)

        self.arm_jnt_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.JOINT, self.GROUP), parent=self.rigPart)

        self.arm_con_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(self.prefix, self.rigType, self.CONTROL, self.GROUP), parent=self.rigPart)

        self.fk_jnt_group = mc.createNode(
            'transform', name='{}_{}_FK_{}_{}'.format(self.prefix, self.rigType, self.JOINT, self.GROUP), parent=self.rigPart)

        self.ik_jnt_group = mc.createNode(
            'transform', name='{}_{}_IK_{}_{}'.format(self.prefix, self.rigType, self.JOINT, self.GROUP), parent=self.rigPart)

        mc.select(cl=True)

    # Create base joints for IKFK
    def createJoints(self, jointOrientation='xyz', secondAxisOrientation='zup'):
        multiple = 1
        for guide in self.arm_guides():
            pp.pprint(guide)
            mat = mc.xform(
                guide, q=True, m=True, ws=True)
            jnt = mc.joint(
                name='{}_{}_Skin{}_{}'.format(self.prefix, self.rigType, multiple, self.JOINT))
            mc.setAttr('{}.radius'.format(jnt), 0.5)
            mc.xform(jnt, m=mat, ws=True)
            mc.parent(jnt, '{}_{}_{}_{}'.format(
                self.prefix, self.rigType, self.JOINT, self.GROUP))
            multiple = multiple + 1

        joint_group = self.arm_joints()
        mc.parent(joint_group[2], joint_group[1])
        mc.parent(joint_group[1], joint_group[0])

        mc.makeIdentity(joint_group[0], a=True, t=0, r=1, s=0, n=0, pn=True)
        mc.makeIdentity(joint_group[1], a=True, t=0, r=1, s=0, n=0, pn=True)
        mc.makeIdentity(joint_group[2], a=True, t=0, r=1, s=0, n=0, pn=True)

        # orient the self.SHOULDER and the self.ELBOW
        mc.select(joint_group[0])
        mc.joint(edit=True, oj=jointOrientation,
                 sao=secondAxisOrientation, ch=True, zso=True)

        mc.select(joint_group[1])
        mc.joint(edit=True, oj=jointOrientation,
                 sao=secondAxisOrientation, ch=True, zso=True)

        # orient the self.WRIST to the world
        mc.select(joint_group[2])
        mc.joint(edit=True, oj='none')

        mc.delete('{}_{}_{}_{}'.format(
            self.prefix, self.rigType, self.GUIDE, self.GROUP))

    def ikfkProcessdure(self):
        joint_list = mc.listRelatives(
            '{}_{}_{}_{}'.format(self.prefix, self.rigType, self.JOINT, self.GROUP), ad=True)
        joint_list.reverse()

        shoulder_radius = mc.getAttr((joint_list[0] + '.radius'))
        new_radius = shoulder_radius

        # Create FK joints

        fk_joint_1 = mc.duplicate(
            joint_list[0], n='{}'.format(joint_list[0]).replace('Skin', 'FK'), po=True)[0]
        mc.setAttr(fk_joint_1 + '.radius', new_radius*1.5)
        fk_joint_2 = mc.duplicate(
            joint_list[1], n='{}'.format(joint_list[1]).replace('Skin', 'FK'), po=True)[0]
        mc.setAttr(fk_joint_2 + '.radius', new_radius*1.5)
        fk_joint_3 = mc.duplicate(
            joint_list[2], n='{}'.format(joint_list[2]).replace('Skin', 'FK'), po=True)[0]
        mc.setAttr(fk_joint_3 + '.radius', new_radius*1.5)

        mc.parent(fk_joint_1, '{}_{}_FK_{}_{}'.format(
            self.prefix, self.rigType, self.JOINT, self.GROUP))
        mc.parent(fk_joint_2, fk_joint_1)
        mc.parent(fk_joint_3, fk_joint_2)

        # Create ik joints

        ik_joint_1 = mc.duplicate(
            joint_list[0], n='{}'.format(joint_list[0]).replace('Skin', 'IK'), po=True)[0]
        mc.setAttr(ik_joint_1 + '.radius', new_radius*0.5)
        ik_joint_2 = mc.duplicate(
            joint_list[1], n='{}'.format(joint_list[1]).replace('Skin', 'IK'), po=True)[0]
        mc.setAttr(ik_joint_2 + '.radius', new_radius*0.5)
        ik_joint_3 = mc.duplicate(
            joint_list[2], n='{}'.format(joint_list[2]).replace('Skin', 'IK'), po=True)[0]
        mc.setAttr(ik_joint_3 + '.radius', new_radius*0.5)

        mc.parent(ik_joint_1, '{}_{}_IK_{}_{}'.format(
            self.prefix, self.rigType, self.JOINT, self.GROUP))
        mc.parent(ik_joint_2, ik_joint_1)
        mc.parent(ik_joint_3, ik_joint_2)

        mc.parent('{}_{}_FK_{}_{}'.format(self.prefix, self.rigType, self.JOINT, self.GROUP),
                  '{}_{}_{}_{}'.format(self.prefix, self.rigType, self.JOINT, self.GROUP))
        mc.parent('{}_{}_IK_{}_{}'.format(self.prefix, self.rigType, self.JOINT, self.GROUP),
                  '{}_{}_{}_{}'.format(self.prefix, self.rigType, self.JOINT, self.GROUP))

        self.shoulder_blend_color = mc.createNode(
            'blendColors', name='{}_{}_{}_BLENDECOLOR'.format(self.prefix, self.rigType, self.SHOULDER))
        self.elbow_blend_color = mc.createNode(
            'blendColors', name='{}_{}_{}_BLENDECOLOR'.format(self.prefix, self.rigType, self.ELBOW))
        self.wrist_blend_color = mc.createNode(
            'blendColors', name='{}_{}_{}_BLENDECOLOR'.format(self.prefix, self.rigType, self.WRIST))

        mc.connectAttr(
            ('{}.rotate'.format(fk_joint_1)), '{}.color1'.format(self.shoulder_blend_color))
        mc.connectAttr(
            ('{}.rotate'.format(ik_joint_1)), '{}.color2'.format(self.shoulder_blend_color))
        mc.connectAttr(
            ('{}.output'.format(self.shoulder_blend_color)), '{}.rotate'.format(joint_list[0]))

        mc.connectAttr(
            ('{}.rotate'.format(fk_joint_2)), '{}.color1'.format(self.elbow_blend_color))
        mc.connectAttr(
            ('{}.rotate'.format(ik_joint_2)), '{}.color2'.format(self.elbow_blend_color))
        mc.connectAttr(
            ('{}.output'.format(self.elbow_blend_color)), '{}.rotate'.format(joint_list[1]))

        mc.connectAttr(
            ('{}.rotate'.format(fk_joint_3)), '{}.color1'.format(self.wrist_blend_color))
        mc.connectAttr(
            ('{}.rotate'.format(ik_joint_3)), '{}.color2'.format(self.wrist_blend_color))
        mc.connectAttr(
            ('{}.output'.format(self.wrist_blend_color)), '{}.rotate'.format(joint_list[2]))

    def create_fk_controls(self):

        # Create FK Controls
        self.fk_controls_group = mc.createNode(
            'transform', name='{}_{}_FKControls_{}'.format(self.prefix, self.rigType, self.GROUP))
        mc.setAttr((self.fk_controls_group + '.overrideEnabled'), 1)
        if 'L_' in ('{}_{}_FKControls_{}'.format(self.prefix, self.rigType, self.GROUP)):
            mc.setAttr((self.fk_controls_group + '.overrideColor'), 6)
        else:
            mc.setAttr((self.fk_controls_group + '.overrideColor'), 13)

        shoulder_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}'.format(self.prefix, self.SHOULDER, self.OFFSET), parent=self.fk_controls_group)
        shoulder_control = mc.circle(
            name='{}_{}_{}'.format(self.prefix, self.SHOULDER, self.CONTROL), nr=(1, 0, 0))[0]
        mc.parent(shoulder_control, shoulder_controls_offset)
        shoulder_mat = mc.xform('{}_{}_Skin1_{}'.format(
            self.prefix, self.rigType, self.JOINT), q=True, m=True, ws=True)
        mc.xform(self.fk_controls_group, m=shoulder_mat, ws=True)

        elbow_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}'.format(self.prefix, self.ELBOW, self.OFFSET), parent=shoulder_control)
        elbow_control = mc.circle(
            name='{}_{}_{}'.format(self.prefix, self.ELBOW, self.CONTROL), nr=(1, 0, 0))[0]
        elbow_mat = mc.xform(
            '{}_{}_Skin2_{}'.format(self.prefix, self.rigType, self.JOINT), q=True, m=True, ws=True)
        mc.parent(elbow_control, elbow_controls_offset)
        mc.xform(elbow_controls_offset, m=elbow_mat, ws=True)
        mc.xform(elbow_control, m=elbow_mat, ws=True)

        wrist_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}'.format(self.prefix, self.WRIST, self.OFFSET), parent=elbow_control)
        wrist_control = mc.circle(name='{}_{}_{}'.format(
            self.prefix, self.WRIST, self.CONTROL), nr=(1, 0, 0))[0]
        wrist_mat = mc.xform('{}_{}_Skin3_{}'.format(
            self.prefix, self.rigType, self.JOINT), q=True, m=True, ws=True)

        mc.parent(wrist_control, wrist_controls_offset)
        mc.xform(wrist_controls_offset, m=wrist_mat, ws=True)
        mc.xform(wrist_control, m=wrist_mat, ws=True)

        mc.parentConstraint(shoulder_control, '{}_{}_FK1_{}'.format(
            self.prefix, self.rigType, self.JOINT), mo=True)
        mc.parentConstraint(elbow_control, '{}_{}_FK2_{}'.format(
            self.prefix, self.rigType, self.JOINT), mo=True)
        mc.parentConstraint(wrist_control, '{}_{}_FK3_{}'.format(
            self.prefix, self.rigType, self.JOINT), mo=True)

        mc.parent('{}_{}_FKControls_{}'.format(self.prefix, self.rigType, self.GROUP),
                  '{}_{}_{}_{}'.format(self.prefix, self.rigType, self.CONTROL, self.GROUP))

    def create_ik_controls(self):

        # Create groups

        IK_wrist_GRP = mc.createNode(
            'transform', name='{}_{}_IKControls_{}'.format(self.prefix, self.rigType, self.GROUP))
        IK_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(self.prefix, self.WRIST, self.OFFSET, self.GROUP), parent=IK_wrist_GRP)

        # Create IK Handle

        IKR_Handle = mc.ikHandle(
            name='{}_{}_IKS'.format(self.prefix, self.rigType), sol='ikRPsolver',
            sj='{}_{}_IK1_{}'.format(self.prefix, self.rigType, self.JOINT), ee='{}_{}_IK3_{}'.format(self.prefix, self.rigType, self.JOINT))[0]

        # Create Control
        self.IKR_wrist_control = mc.curve(n='{}_{}_{}'.format(
            self.prefix, self.rigType, self.CONTROL), d=1, p=zbw_con.shapes['cube'])
        print(self.IKR_wrist_control)

        # move things into position
        IK_wrist_mat = mc.xform(
            '{}_{}_Skin3_{}'.format(self.prefix, self.rigType, self.JOINT), q=True, m=True, ws=True)

        mc.xform(IK_wrist_GRP, m=IK_wrist_mat, ws=True)
        mc.xform(self.IKR_wrist_control, m=IK_wrist_mat, ws=True)
        mc.parent(self.IKR_wrist_control, IK_controls_offset)
        pp.pprint(self.IKR_wrist_control)
        mc.parent(IKR_Handle, self.IKR_wrist_control)

        mc.parent(IK_wrist_GRP, '{}_{}_{}_{}'.format(
            self.prefix, self.rigType, self.CONTROL, self.GROUP))

    def create_pole_target(self, distance=1.0):

        def create_loc(pos):
            #loc = mc.spaceLocator(n='{}_{}_PV_LOC'.format(self.prefix, self.rigType))
            #mc.move(pos.x, pos.y, pos.z, loc)

            # create pole vector shape
            pv_group = mc.createNode('transform', name='{}_{}_PV_{}'.format(
                self.prefix, self.rigType, self.GROUP))
            pv_control = mc.curve(n='{}_{}_PV_{}'.format(
                self.prefix, self.rigType, self.CONTROL), d=1, p=zbw_con.shapes['cube'])
            mc.parent(pv_control, pv_group)
            mc.move(pos.x, pos.y, pos.z, pv_group)
            mc.poleVectorConstraint(
                pv_control, '{}_{}_IKS'.format(self.prefix, self.rigType))
            mc.parent(pv_group, self.arm_con_group)

        def get_pole_vec_pos(root_pos, mid_pos, end_pos):

            root_joint_vec = om.MVector(root_pos[0], root_pos[1], root_pos[2])
            mid_joint_vec = om.MVector(mid_pos[0], mid_pos[1], mid_pos[2])
            end_joint_vec = om.MVector(end_pos[0], end_pos[1], end_pos[2])

            line = (end_joint_vec - root_joint_vec)
            point = (mid_joint_vec - root_joint_vec)

            # MVector automatically: does the dot product((line.length*point.length)cos theta)
            # MVector adds the cos automatically
            scale_value = (line*point) / (line * line)
            proj_vec = line * scale_value + root_joint_vec

            root_to_mid_len = (mid_joint_vec - root_joint_vec).length()
            mid_to_end_len = (end_joint_vec - mid_joint_vec).length()
            total_len = (root_to_mid_len + mid_to_end_len)

            pole_vec_pos = (mid_joint_vec - proj_vec).normal() * \
                distance * total_len + mid_joint_vec

            create_loc(pole_vec_pos)

        root_joint_pos = mc.xform('{}_{}_IK1_{}'.format(
            self.prefix, self.rigType, self.JOINT), q=1, ws=1, t=1)
        mid_joint_pos = mc.xform('{}_{}_IK2_{}'.format(
            self.prefix, self.rigType, self.JOINT), q=1, ws=1, t=1)
        end_joint_pos = mc.xform('{}_{}_IK3_{}'.format(
            self.prefix, self.rigType, self.JOINT), q=1, ws=1, t=1)

        get_pole_vec_pos(root_joint_pos, mid_joint_pos, end_joint_pos)

    def create_asset_and_atributes(self):
        self.arm_atributes_Grp = mc.createNode(
            'transform', name='{}_{}_ATRIBUTES_GRP'.format(self.prefix, self.rigType))
        mc.addAttr(ln='IKFK_Switch', at='float', k=True,  min=0, max=1)
        self.arm_atributes_asset = mc.container(
            name='{}_{}_ASSET'.format(self.prefix, self.rigType))
        mc.parent(self.arm_atributes_Grp, self.rigPart)
        mc.container(self.arm_atributes_asset, e=True, ish=True,
                     f=True, an=self.arm_atributes_Grp)

    def make_connections(self):  # FIXME
        # IKFK switch

        IKFK_reverse = mc.createNode('reverse', n='{}_{}_IKFK_reverse')

        mc.container(self.arm_atributes_asset, edit=True,
                     addNode='{}_{}_{}'.format(self.prefix, self.SHOULDER, self.CONTROL))

        mc.container(self.arm_atributes_asset, edit=True,
                     addNode='{}_{}_{}'.format(self.prefix, self.ELBOW, self.CONTROL))

        mc.container(self.arm_atributes_asset, edit=True,
                     addNode='{}_{}_{}'.format(self.prefix, self.WRIST, self.CONTROL))

        mc.container(self.arm_atributes_asset, edit=True,
                     addNode=self.IKR_wrist_control)

        mc.container(self.arm_atributes_asset, edit=True,
                     addNode='{}_{}_PV_{}'.format(self.prefix, self.rigType, self.CONTROL))

        mc.container(self.arm_atributes_asset, e=True, pn=('IKFK_Switch'))
        mc.container(self.arm_atributes_asset, e=True, ba=(
            self.arm_atributes_Grp + '.IKFK_Switch', 'IKFK_Switch'))

        mc.connectAttr(self.arm_atributes_Grp + '.IKFK_Switch',
                       IKFK_reverse + '.input.inputX')

        mc.connectAttr(IKFK_reverse + '.input.inputX',
                       self.shoulder_blend_color + '.blender')
        mc.connectAttr(IKFK_reverse + '.input.inputX',
                       self.elbow_blend_color + '.blender')
        mc.connectAttr(IKFK_reverse + '.input.inputX',
                       self.wrist_blend_color + '.blender')

    def IKFK_snap_expression(self):  # NOT WORKING
        self.init_dist = 200
        scale_distance_node = mc.createNode(
            'distanceBetween', n='{}_{}_distanceBetween'.format(self.prefix, self.rigType))
        mc.addAttr(self.IKR_wrist_control, at='float',
                   ln='Stretch', k=True, min=0, max=1)
        mc.addAttr(self.IKR_wrist_control, at='float', ln='ShortArm', k=True)
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

    # Build Methods

    def build_guides(self):

        self.create_guides()

    def build_joints(self):
        self.createHierarchy()
        self.createJoints()

    def build_rig(self):
        self.ikfkProcessdure()
        self.create_fk_controls()
        self.create_ik_controls()
        self.create_pole_target()
        self.create_asset_and_atributes()
        self.make_connections()
        # FIXME self.IKFK_snap_expression()
        # TODO: self.create_twist_joints()
        # TODO: self.create_bend_joints()
        # TODO: self.create_stretch()
