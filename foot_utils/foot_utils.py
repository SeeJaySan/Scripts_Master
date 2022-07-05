import maya.cmds as mc
import pprint as pp

SPINE_LENGTH = 5

# object constants
GROUP = 'GRP'
JOINT = 'JNT'
GUIDE = 'GUIDE'
OFFSET = 'OFF'
CONTROLS = 'CON'
RIBBON = 'RIBBON'

# spine constants
SPINE = 'SPINE'
CENTER = 'C'


def createGuides():
    spine_group = mc.createNode(
        'transform', name='{}_{}_{}'.format(CENTER, SPINE, GROUP))

    spine_guide_group = mc.createNode(
        'transform', name='{}_{}_{}_{}'.format(CENTER, SPINE, GUIDE, GROUP), parent=spine_group)

    for number in range(SPINE_LENGTH):
        number = number + 1
        loc = mc.spaceLocator(
            name='{}_{}{}_{}'.format(CENTER, SPINE, number, GUIDE))[0]
        mc.setAttr(
            '{}.t'.format(loc), 0, number, 0)
        mc.parent(
            loc, spine_guide_group)


def build_hierarchy():

    spine_joint_group = mc.createNode(
        'transform', name='{}_{}_{}_{}'.format(CENTER, SPINE, JOINT, GROUP),
        parent='{}_{}_{}'.format(CENTER, SPINE, GROUP))
    ribbon_spine_group = mc.createNode(
        'transform', name='{}_{}_{}_{}'.format(CENTER, SPINE, RIBBON, GROUP),
        parent='{}_{}_{}'.format(CENTER, SPINE, GROUP))


def spine_guides():

    grp = '{}_{}_{}_{}'.format(CENTER, SPINE, GUIDE, GROUP)

    return [jnt for jnt in mc.listRelatives(grp) if mc.objExists(grp)]


def group_selection(sel):

    selXform = mc.xform(
        sel, q=True, m=True, ws=True)

    GRP = mc.createNode(
        'transform', name=str(sel) + '_GRP')
    mc.xform(
        GRP, m=selXform)

    if mc.listRelatives(
            sel, p=True):
        mc.select(
            sel)
        target = mc.pickWalk(
            d='UP')
        mc.parent(
            GRP, target)
        mc.parent(
            sel, GRP)
    else:
        mc.parent(
            sel, GRP)

    return(GRP)


def create_parent_structure():

    groups = list()

    for loc in spine_guides():
        GRP = group_selection(loc)
        groups.append(GRP)

    mc.pointConstraint(
        '{}_{}1_{}'.format(CENTER, SPINE, GUIDE), '{}_{}5_{}'.format(CENTER, SPINE, GUIDE), groups[2], mo=True)
    mc.pointConstraint(
        '{}_{}1_{}'.format(CENTER, SPINE, GUIDE), '{}_{}3_{}'.format(CENTER, SPINE, GUIDE), groups[1], mo=True)
    mc.pointConstraint(
        '{}_{}3_{}'.format(CENTER, SPINE, GUIDE), '{}_{}5_{}'.format(CENTER, SPINE, GUIDE), groups[3], mo=True)


def build_joints():

    joint_list = list()
    number = 0

    for loc in spine_guides():
        number = number + 1
        rel = mc.listRelatives(loc)[0] 
        mat = mc.xform(
            rel, q=True, m=True, ws=True)
        jnt = mc.joint(
            n='{}_{}{}_{}'.format(CENTER, SPINE, number, JOINT))
        mc.setAttr(
            '{}.radius'.format(jnt), 0.5)
        mc.xform(
            jnt, m=mat, ws = True)
        mc.parent(jnt, '{}_{}_{}_{}'.format(CENTER, SPINE, JOINT, GROUP))
        joint_list.append(jnt)


    print(joint_list)

    mc.parent(joint_list[4], joint_list[3])
    mc.parent(joint_list[3], joint_list[2])
    mc.parent(joint_list[2], joint_list[1])
    mc.parent(joint_list[1], joint_list[0])



'''
# return the locators in the loc group
def spine_guides():
    """_summary_

    Returns:
        _type_: _description_
    """

    grp = '{}_{}_{}_{}'.format(LEFT, ARM, GUIDE, GROUP)

    return [loc for loc in mc.listRelatives(grp) if mc.objExists(grp)]


# return the joints in the joint group
def spine_joints():

    grp = '{}_{}_{}_{}'.format(LEFT, ARM, JOINT, GROUP)

    return [jnt for jnt in mc.listRelatives(grp, ad=True) if mc.objExists(grp)]


def createHierarchy():
    arm_group = mc.createNode(
        'transform', name='{}_{}_{}'.format(LEFT, ARM, GROUP))

    mc.parent('{}_{}_{}_{}'.format(LEFT, ARM, GUIDE, GROUP), arm_group)
    arm_jnt_group = mc.createNode(
        'transform', name='{}_{}_{}_{}'.format(LEFT, ARM, JOINT, GROUP), parent=arm_group)

    arm_con_group = mc.createNode(
        'transform', name='{}_{}_{}_{}'.format(LEFT, ARM, CONTROLS, GROUP), parent=arm_group)

    fk_jnt_group = mc.createNode(
        'transform', name='{}_{}_FK_{}_{}'.format(LEFT, ARM, JOINT, GROUP), parent=arm_group)
    fk_control_group = mc.createNode(
        'transform', name='{}_{}_FK_{}_{}'.format(LEFT, ARM, CONTROLS, GROUP), parent=arm_con_group)

    ik_jnt_group = mc.createNode(
        'transform', name='{}_{}_IK_{}_{}'.format(LEFT, ARM, JOINT, GROUP), parent=arm_group)
    ik_control_group = mc.createNode(
        'transform', name='{}_{}_IK_{}_{}'.format(LEFT, ARM, CONTROLS, GROUP), parent=arm_con_group)


def createJoints():
    multiple = 1
    for guide in arm_guides():
        mat = mc.xform(
            guide, q=True, m=True, ws=True)
        jnt = mc.joint(
            name='{}_{}_Skin{}_{}'.format(LEFT, ARM, multiple, JOINT))
        mc.setAttr('{}.radius'.format(jnt), 0.5)
        mc.xform(jnt, m=mat, ws=True)
        mc.parent(jnt, '{}_{}_{}_{}'.format(LEFT, ARM, JOINT, GROUP))
        multiple = multiple + 1
        mc.delete(guide)

    joint_group = arm_joints()
    mc.parent(joint_group[2], joint_group[1])
    mc.parent(joint_group[1], joint_group[0])


def ikfkProcessdure():
    joint_list = mc.listRelatives(
        '{}_{}_{}_{}'.format(LEFT, ARM, JOINT, GROUP), ad=True)
    joint_list.reverse()

    fk_joint_1 = mc.duplicate(
        joint_list[0], n='{}'.format(joint_list[0]).replace('Skin', 'FK'), po=True)[0]
    fk_joint_2 = mc.duplicate(
        joint_list[1], n='{}'.format(joint_list[1]).replace('Skin', 'FK'), po=True)[0]
    fk_joint_3 = mc.duplicate(
        joint_list[2], n='{}'.format(joint_list[2]).replace('Skin', 'FK'), po=True)[0]
    mc.parent(fk_joint_1, '{}_{}_FK_{}_{}'.format(LEFT, ARM, JOINT, GROUP))
    mc.parent(fk_joint_2, fk_joint_1)
    mc.parent(fk_joint_3, fk_joint_2)

    ik_joint_1 = mc.duplicate(
        joint_list[0], n='{}'.format(joint_list[0]).replace('Skin', 'IK'), po=True)[0]
    ik_joint_2 = mc.duplicate(
        joint_list[1], n='{}'.format(joint_list[1]).replace('Skin', 'IK'), po=True)[0]
    ik_joint_3 = mc.duplicate(
        joint_list[2], n='{}'.format(joint_list[2]).replace('Skin', 'IK'), po=True)[0]
    mc.parent(ik_joint_1, '{}_{}_IK_{}_{}'.format(LEFT, ARM, JOINT, GROUP))
    mc.parent(ik_joint_2, ik_joint_1)
    mc.parent(ik_joint_3, ik_joint_2)

    shoulder_blend_color = mc.createNode(
        'blendColors', name='{}_{}_{}_blendColor'.format(LEFT, ARM, SHOULDER))
    elbow_blend_color = mc.createNode(
        'blendColors', name='{}_{}_{}_blendColor'.format(LEFT, ARM, ELBOW))
    wrist_blend_color = mc.createNode(
        'blendColors', name='{}_{}_{}_blendColor'.format(LEFT, ARM, WRIST))

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


def createControls():
    shoulder_controls_group = mc.createNode(
        'transform', name='{}_{}_FKControls_{}'.format(LEFT, ARM, GROUP))

    shoulder_controls_offset = mc.createNode(
        'transform', name='{}_{}_{}'.format(LEFT, SHOULDER, OFFSET), parent=shoulder_controls_group)
    shoulder_control = mc.circle(
        name='{}_{}_{}'.format(LEFT, SHOULDER, CONTROLS), nr=(0, 1, 0))[0]
    mc.parent(shoulder_control, shoulder_controls_offset)
    shoulder_mat = mc.xform(
        '{}_{}_Skin1_{}'.format(LEFT, ARM, JOINT), q=True, m=True, ws=True)
    mc.xform(shoulder_controls_group, m=shoulder_mat, ws=True)

    elbow_controls_offset = mc.createNode(
        'transform', name='{}_{}_{}'.format(LEFT, ELBOW, OFFSET), parent=shoulder_control)
    elbow_control = mc.circle(
        name='{}_{}_{}'.format(LEFT, ELBOW, CONTROLS), nr=(0, 1, 0))[0]
    elbow_mat = mc.xform(
        '{}_{}_Skin2_{}'.format(LEFT, ARM, JOINT), q=True, m=True, ws=True)
    mc.parent(elbow_control, elbow_controls_offset)
    mc.xform(elbow_controls_offset, m=elbow_mat, ws=True)
    mc.xform(elbow_control, m=elbow_mat, ws=True)

    wrist_controls_offset = mc.createNode(
        'transform', name='{}_{}_{}'.format(LEFT, WRIST, OFFSET), parent=elbow_control)
    wrist_control = mc.circle(
        name='{}_{}_{}'.format(LEFT, WRIST, CONTROLS), nr=(0, 1, 0))[0]
    wrist_mat = mc.xform(
        '{}_{}_Skin3_{}'.format(LEFT, ARM, JOINT), q=True, m=True, ws=True)
    mc.parent(
        wrist_control, wrist_controls_offset)
    mc.xform(
        wrist_controls_offset, m=wrist_mat, ws=True)
    mc.xform(
        wrist_control, m=wrist_mat, ws=True)

    mc.parentConstraint(
        shoulder_control, '{}_{}_FK1_{}'.format(LEFT, ARM, JOINT), mo=True)
    mc.parentConstraint(
        elbow_control, '{}_{}_FK2_{}'.format(LEFT, ARM, JOINT), mo=True)
    mc.parentConstraint(
        wrist_control, '{}_{}_FK3_{}'.format(LEFT, ARM, JOINT), mo=True)

    # ----------
    #
    # ADD IK CONTROLS
    IKr = mc.ikHandle(
        name='{}_{}_IKS'.format(LEFT, ARM), sol='ikRPsolver',
        sj='{}_{}_IK3_{}'.format(LEFT, ARM, JOINT), ee='{}_{}_IK3_{}'.format(LEFT, ARM, JOINT))
    #
    # ----------
def create_arm_asset():
    arm_atributes = mc.container(
        name='{}_{}_ATRIBUTES'.format(LEFT, ARM))

    return(arm_atributes)

def make_connections():
    #IKFK switch
    contrainer = mc.select(
        create_arm_asset())
    mc.addAttr(
        ln = 'IKFKSwitch', sn = 'IKFK', dv =  0, min = 0, max = 1)
    mc.container(
        contrainer, edit=True,
        publishName='ikfkSwitch',
        addNode=(
            '{}_{}_{}'.format(LEFT, SHOULDER, CONTROLS),
            '{}_{}_{}'.format(LEFT, ELBOW, CONTROLS),
            '{}_{}_{}'.format(LEFT, WRIST, CONTROLS)))

    #----------
    #
    # Add pole target follow
    #
    #----------
    
'''
