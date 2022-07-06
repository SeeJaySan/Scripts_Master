from lib2to3.pgen2.token import NAME
import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm
import pprint as pp
import maya.OpenMaya as om
from third_party import zbw_controlShapes as zbw_con

# object constants
GROUP = 'GRP'
JOINT = 'JNT'
GUIDE = 'GUIDE'
OFFSET = 'OFF'
CONTROL = 'CON'

# arm constants
ARM = 'ARM'
CLAVICLE = 'CLAVICLE'
SHOULDER = 'SHOULDER'

ELBOW = 'ELBOW'
WRIST = 'WRIST'

# hand constants
THUMB = 'THUMB'
INDEX = 'INDEX'
MIDDLE = 'MIDDLE'
RING = 'RING'
PINKY = 'PINKY'


# side constants
which_side = 1

if which_side == 1:
    SIDE = 'L'
if which_side == 0:
    SIDE = 'C'
if which_side == -1:
    SIDE = 'R'





class TwoBoneIKFK:


    def __init__(self, SIDE='center'):
        self.SIDE = SIDE
        pass

    def build_guides(self):

        # build guide group
        arm_guide_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(self.SIDE, ARM, GUIDE, GROUP))
        arm_guide_up_group = mc.createNode(
            'transform', name='{}_{}_UP_{}_{}'.format(SIDE, ARM, GUIDE, GROUP), parent=arm_guide_group)
        mc.hide(arm_guide_up_group)
        arm_guide_loc_group = mc.createNode(
            'transform', name='{}_{}_LOC_{}_{}'.format(SIDE, ARM, GUIDE, GROUP), parent=arm_guide_group)
        arm_guide_control_group = mc.createNode(
            'transform', name='{}_{}_{}_{}_{}'.format(SIDE, ARM, GUIDE, CONTROL, GROUP), parent=arm_guide_group)

        # build locators for the arm
        loc_list = list()
        shoulder_loc = mc.spaceLocator(
            name='{}_{}_Shoulder_{}'.format(SIDE, ARM, GUIDE))[0]
        elbow_loc = mc.spaceLocator(
            name='{}_{}_Elbow_{}'.format(SIDE, ARM, GUIDE))[0]
        wrist_loc = mc.spaceLocator(
            name='{}_{}_Wrist_{}'.format(SIDE, ARM, GUIDE))[0]

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
            shoulder_loc, n=shoulder_loc.replace('Shoulder', 'Shoulder_up'))[0]
        elbow_up = mc.duplicate(
            elbow_loc, n=elbow_loc.replace('Elbow', 'Elbow_up'))[0]
        wrist_up = mc.duplicate(
            wrist_loc, n=wrist_loc.replace('Wrist', 'Wrist_up'))[0]

        # create locator offset
        mc.setAttr('{}.t'.format(shoulder_up),
                0, 2, 0)
        mc.setAttr('{}.t'.format(elbow_up),
                5, 2, 0)
        mc.setAttr('{}.t'.format(wrist_up),
                10, 2, 0)

        # create controls to move locators
        shoulder_loc_control = mc.circle(
            name='{}_{}_{}_{}'.format(SIDE, SHOULDER, GUIDE, CONTROL), r=2, nr=(1, 0, 0))[0]
        shoulder_PC = mc.parentConstraint(shoulder_loc, shoulder_loc_control)
        mc.delete(shoulder_PC)

        elbow_loc_control = mc.circle(
            name='{}_{}_{}_{}'.format(SIDE, ELBOW, GUIDE, CONTROL), r=2, nr=(1, 0, 0))[0]
        elbow_PC = mc.parentConstraint(elbow_loc, elbow_loc_control)
        mc.setAttr(elbow_loc_control + '.rx', lock=True)
        mc.setAttr(elbow_loc_control + '.rz', lock=True)
        mc.setAttr(elbow_loc_control + '.ty', lock=True)

        mc.delete(elbow_PC)

        wrist_loc_control = mc.circle(
            name='{}_{}_{}_{}'.format(SIDE, WRIST, GUIDE, CONTROL), r=2, nr=(1, 0, 0))[0]
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
        """_summary_

        Returns:
            _type_: _description_
        """

        grp = '{}_{}_LOC_{}_{}'.format(SIDE, ARM, GUIDE, GROUP)

        return [loc for loc in mc.listRelatives(grp) if mc.objExists(grp)]





    # return the joints in the joint group
    def arm_joints(self):

        grp = '{}_{}_{}_{}'.format(SIDE, ARM, JOINT, GROUP)

        return [jnt for jnt in mc.listRelatives(grp, ad=True) if mc.objExists(grp)]


    def createHierarchy(self):
        arm_group = mc.createNode(
            'transform', name='{}_{}_{}'.format(SIDE, ARM, GROUP))

        mc.parent('{}_{}_{}_{}'.format(SIDE, ARM, GUIDE, GROUP), arm_group)
        arm_jnt_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(SIDE, ARM, JOINT, GROUP), parent=arm_group)

        arm_con_group = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(SIDE, ARM, CONTROL, GROUP), parent=arm_group)

        fk_jnt_group = mc.createNode(
            'transform', name='{}_{}_FK_{}_{}'.format(SIDE, ARM, JOINT, GROUP), parent=arm_group)

        ik_jnt_group = mc.createNode(
            'transform', name='{}_{}_IK_{}_{}'.format(SIDE, ARM, JOINT, GROUP), parent=arm_group)

        mc.select(cl=True)


    def createJoints(self, jointOrientation='xyz', secondAxisOrientation='zup'):
        multiple = 1
        for guide in self.arm_guides():
            pp.pprint(guide)
            mat = mc.xform(
                guide, q=True, m=True, ws=True)
            jnt = mc.joint(
                name='{}_{}_Skin{}_{}'.format(SIDE, ARM, multiple, JOINT))
            mc.setAttr('{}.radius'.format(jnt), 0.5)
            mc.xform(jnt, m=mat, ws=True)
            mc.parent(jnt, '{}_{}_{}_{}'.format(SIDE, ARM, JOINT, GROUP))
            multiple = multiple + 1

        joint_group = self.arm_joints()
        mc.parent(joint_group[2], joint_group[1])
        mc.parent(joint_group[1], joint_group[0])

        mc.makeIdentity(joint_group[0], a=True, t=0, r=1, s=0, n=0, pn=True)
        mc.makeIdentity(joint_group[1], a=True, t=0, r=1, s=0, n=0, pn=True)
        mc.makeIdentity(joint_group[2], a=True, t=0, r=1, s=0, n=0, pn=True)

        # orient the shoulder and the elbow
        mc.select(joint_group[0])
        mc.joint(edit=True, oj=jointOrientation, sao=secondAxisOrientation, ch=True, zso=True)

        mc.select(joint_group[1])
        mc.joint(edit=True, oj=jointOrientation, sao=secondAxisOrientation, ch=True, zso=True)

        # orient the wrist to the world
        mc.select(joint_group[2])
        mc.joint(edit=True, oj='none')

        mc.delete('{}_{}_{}_{}'.format(SIDE, ARM, GUIDE, GROUP))


    def ikfkProcessdure(self):
        joint_list = mc.listRelatives(
            '{}_{}_{}_{}'.format(SIDE, ARM, JOINT, GROUP), ad=True)
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

        mc.parent(fk_joint_1, '{}_{}_FK_{}_{}'.format(SIDE, ARM, JOINT, GROUP))
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

        mc.parent(ik_joint_1, '{}_{}_IK_{}_{}'.format(SIDE, ARM, JOINT, GROUP))
        mc.parent(ik_joint_2, ik_joint_1)
        mc.parent(ik_joint_3, ik_joint_2)

        mc.parent('{}_{}_FK_{}_{}'.format(SIDE, ARM, JOINT, GROUP),
                '{}_{}_{}_{}'.format(SIDE, ARM, JOINT, GROUP))
        mc.parent('{}_{}_IK_{}_{}'.format(SIDE, ARM, JOINT, GROUP),
                '{}_{}_{}_{}'.format(SIDE, ARM, JOINT, GROUP))

        shoulder_blend_color = mc.createNode(
            'blendColors', name='{}_{}_{}_BLENDECOLOR'.format(SIDE, ARM, SHOULDER))
        elbow_blend_color = mc.createNode(
            'blendColors', name='{}_{}_{}_BLENDECOLOR'.format(SIDE, ARM, ELBOW))
        wrist_blend_color = mc.createNode(
            'blendColors', name='{}_{}_{}_BLENDECOLOR'.format(SIDE, ARM, WRIST))

        mc.connectAttr(
            ('{}.rotate'.format(fk_joint_1)), '{}.color1'.format(shoulder_blend_color))
        mc.connectAttr(
            ('{}.rotate'.format(ik_joint_1)), '{}.color2'.format(shoulder_blend_color))
        mc.connectAttr(
            ('{}.output'.format(shoulder_blend_color)), '{}.rotate'.format(joint_list[0]))

        mc.connectAttr(
            ('{}.rotate'.format(fk_joint_2)), '{}.color1'.format(elbow_blend_color))
        mc.connectAttr(
            ('{}.rotate'.format(ik_joint_2)), '{}.color2'.format(elbow_blend_color))
        mc.connectAttr(
            ('{}.output'.format(elbow_blend_color)), '{}.rotate'.format(joint_list[1]))

        mc.connectAttr(
            ('{}.rotate'.format(fk_joint_3)), '{}.color1'.format(wrist_blend_color))
        mc.connectAttr(
            ('{}.rotate'.format(ik_joint_3)), '{}.color2'.format(wrist_blend_color))
        mc.connectAttr(
            ('{}.output'.format(wrist_blend_color)), '{}.rotate'.format(joint_list[2]))


    def create_fk_controls(self):

        # Create FK Controls
        fk_controls_group = mc.createNode(
            'transform', name='{}_{}_FKControls_{}'.format(SIDE, ARM, GROUP))
        mc.setAttr((fk_controls_group + '.overrideEnabled'), 1)
        if 'L_' in ('{}_{}_FKControls_{}'.format(SIDE, ARM, GROUP)):
            mc.setAttr((fk_controls_group + '.overrideColor'), 6)
        else:
            mc.setAttr((fk_controls_group + '.overrideColor'), 13)

        shoulder_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}'.format(SIDE, SHOULDER, OFFSET), parent=fk_controls_group)
        shoulder_control = mc.circle(
            name='{}_{}_{}'.format(SIDE, SHOULDER, CONTROL), nr=(1, 0, 0))[0]
        mc.parent(shoulder_control, shoulder_controls_offset)
        shoulder_mat = mc.xform('{}_{}_Skin1_{}'.format(
            SIDE, ARM, JOINT), q=True, m=True, ws=True)
        mc.xform(fk_controls_group, m=shoulder_mat, ws=True)

        elbow_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}'.format(SIDE, ELBOW, OFFSET), parent=shoulder_control)
        elbow_control = mc.circle(
            name='{}_{}_{}'.format(SIDE, ELBOW, CONTROL), nr=(1, 0, 0))[0]
        elbow_mat = mc.xform(
            '{}_{}_Skin2_{}'.format(SIDE, ARM, JOINT), q=True, m=True, ws=True)
        mc.parent(elbow_control, elbow_controls_offset)
        mc.xform(elbow_controls_offset, m=elbow_mat, ws=True)
        mc.xform(elbow_control, m=elbow_mat, ws=True)

        wrist_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}'.format(SIDE, WRIST, OFFSET), parent=elbow_control)
        wrist_control = mc.circle(name='{}_{}_{}'.format(
            SIDE, WRIST, CONTROL), nr=(1, 0, 0))[0]
        wrist_mat = mc.xform('{}_{}_Skin3_{}'.format(
            SIDE, ARM, JOINT), q=True, m=True, ws=True)

        mc.parent(wrist_control, wrist_controls_offset)
        mc.xform(wrist_controls_offset, m=wrist_mat, ws=True)
        mc.xform(wrist_control, m=wrist_mat, ws=True)

        mc.parentConstraint(shoulder_control, '{}_{}_FK1_{}'.format(
            SIDE, ARM, JOINT), mo=True)
        mc.parentConstraint(elbow_control, '{}_{}_FK2_{}'.format(
            SIDE, ARM, JOINT), mo=True)
        mc.parentConstraint(wrist_control, '{}_{}_FK3_{}'.format(
            SIDE, ARM, JOINT), mo=True)

        mc.parent('{}_{}_FKControls_{}'.format(SIDE, ARM, GROUP),
                '{}_{}_{}_{}'.format(SIDE, ARM, CONTROL, GROUP))


    def create_ik_controls(self):

        # Create groups

        IK_wrist_GRP = mc.createNode(
            'transform', name='{}_{}_IKControls_{}'.format(SIDE, ARM, GROUP))
        IK_controls_offset = mc.createNode(
            'transform', name='{}_{}_{}_{}'.format(SIDE, WRIST, OFFSET, GROUP), parent=IK_wrist_GRP)

        # Create IK Handle

        IKR_Handle = mc.ikHandle(
            name='{}_{}_IKS'.format(SIDE, ARM), sol='ikRPsolver',
            sj='{}_{}_IK1_{}'.format(SIDE, ARM, JOINT), ee='{}_{}_IK3_{}'.format(SIDE, ARM, JOINT))[0]

        # Create Control
        IKR_wrist_control = cubeShape()

        # move things into position
        IK_wrist_mat = mc.xform(
            '{}_{}_Skin3_{}'.format(SIDE, ARM, JOINT), q=True, m=True, ws=True)

        mc.xform(IK_wrist_GRP, m=IK_wrist_mat, ws=True)
        mc.xform(IKR_wrist_control, m=IK_wrist_mat, ws=True)
        mc.parent(IKR_wrist_control, IK_controls_offset)
        pp.pprint(IKR_wrist_control)
        mc.parent(IKR_Handle, IKR_wrist_control)

        mc.parent(IK_wrist_GRP, '{}_{}_{}_{}'.format(SIDE, ARM, CONTROL, GROUP))
        
    def create_pole_target(distance=0.5):

        def create_loc (pos):
            loc = mc.spaceLocator()
            mc.move(pos.x, pos.y, pos.z, loc)
        

        def get_pole_vec_pos(root_pos, mid_pos, end_pos):
            
            root_joint_vec = om.MVector(root_pos[0], root_pos[1], root_pos[2])
            mid_joint_vec = om.MVector(mid_pos[0], mid_pos[1], mid_pos[2])
            end_joint_vec = om.MVector(end_pos[0], end_pos[1], end_pos[2])
            
            line = (end_joint_vec - root_joint_vec)
            point = (mid_joint_vec - root_joint_vec)

            #MVector automatically: does the dot product((line.length*point.length)cos theta)
            # MVector adds the cos automatically
            scale_value = (line*point) / (line * line)
            proj_vec = line * scale_value + root_joint_vec
            
            root_to_mid_len = (mid_joint_vec - root_joint_vec).length()
            mid_to_end_len = (end_joint_vec - mid_joint_vec).length()
            total_len = (root_to_mid_len + mid_to_end_len)
            
            pole_vec_pos = (mid_joint_vec - proj_vec).normal()* 0.5 * total_len + mid_joint_vec
            
            create_loc(pole_vec_pos)
        
        
        

        root_joint_pos = mc.xform('{}_{}_IK1_{}'.format(SIDE, ARM, JOINT), q=1, ws=1,t=1)
        mid_joint_pos = mc.xform('{}_{}_IK2_{}'.format(SIDE, ARM, JOINT), q=1, ws=1,t=1)
        end_joint_pos = mc.xform('{}_{}_IK3_{}'.format(SIDE, ARM, JOINT), q=1, ws=1,t=1)

        get_pole_vec_pos(root_joint_pos, mid_joint_pos, end_joint_pos)


    # NOT WORKING

    def create_arm_asset(self):
        arm_atributes_Grp = mc.createNode(
            'transform', name='{}_{}_ATRIBUTES_GRP'.format(SIDE, ARM))
        mc.addAttr(ln = 'IKFK_Switch', at = 'float', min = 0, max = 1, )
        mc.select(arm_atributes_Grp)
        arm_atributes = mc.container(
            name='{}_{}_ASSET'.format(SIDE, ARM))
        mc.parent(arm_atributes, '{}_{}_{}'.format(SIDE, ARM, GROUP))

        return(arm_atributes)


    def make_connections(self):
        # IKFK switch
        container = self.create_arm_asset()

        # THERE IS A WEIRD ISSUE WHERE I CAN'T ADD THE ATRIBUTE TO THE CURVES OFF THE CONTAINER. NEED INTERNET TO FIGURE OUT
        mc.addAttr('{}_{}_ATRIBUTES'.format(SIDE, ARM), ln='IKFKSwitch',
                sn='IKFK', at='double',  dv=0, min=0, max=1)

        mc.container(container, edit=True,
                    addNode='{}_{}_{}'.format(SIDE, SHOULDER, CONTROL))

        mc.container(container, edit=True,
                    addNode='{}_{}_{}'.format(SIDE, ELBOW, CONTROL))

        mc.container(container, edit=True,
                    addNode='{}_{}_{}'.format(SIDE, WRIST, CONTROL))

        shoulder_bc = '{}_{}_{}_blendColor'.format(SIDE, ARM, SHOULDER)
        mc.container(container, edit=True,
                    pb=('IKFKSwitch', '{}.Blender'.format(shoulder_bc)))

        elbow_bc = '{}_{}_{}_blendColor'.format(SIDE, ARM, ELBOW)
        mc.container(container, edit=True,
                    pb=('IKFKSwitch', '{}.Blender'.format(elbow_bc)))

        wrist_bc = '{}_{}_{}_blendColor'.format(SIDE, ARM, WRIST)
        mc.container(container, edit=True,
                    pb=('IKFKSwitch', '{}.Blender'.format(wrist_bc)))
        # ----------
        #
        # Add pole target follow
        #
        # ----------

    def build_joints(self):
        self.createHierarchy()
        self.createJoints()

    def build_rig(self):
        self.ikfkProcessdure()
        self.create_fk_controls()
        self.create_ik_controls()

def cubeShape(CRVname='test', *args):
    cube_control = []
    curve = mc.curve(n=CRVname, d=1, p=[(-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1), (-1, -1, -1),
                                        (-1, -1, 1), (-1, -1, -1), (1, -1, -1), (1, -1, 1), (1, 1, 1), (1, 1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1)],
                    k=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])

    cube_control.append(str(curve))
    mc.select(cl=True)
    return cube_control

that = mc.curve(n='this', d=1, p=zbw_con.shapes['cube'])