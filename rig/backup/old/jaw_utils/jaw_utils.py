import maya.cmds as mc
import pprint as pp

# onject constants
GROUP = 'GRP'
JOINT = 'JNT'
GUIDE = 'GUIDE'
JAW = 'jaw'

# side constants
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'


def addOffset(dst, suffix='OFF'):
    """_summary_
    """

    grp_offset = mc.createNode('transform', name='{}_{}'.format(dst, suffix))
    dst_mat = mc.xform(dst, q=True, m=True, ws=True)
    mc.xform(grp_offset, m=dst_mat, ws=True)

    dst_parent = mc.listRelatives(dst, parent=True)
    if dst_parent:
        mc.parent(grp_offset, dst_parent)
    mc.parent(dst, grp_offset)

    return grp_offset


def createGuides(number=10):
    """_summary_

    Args:
        number (int, optional): _description_. Defaults to 8.
    """

    jaw_guide_grp = mc.createNode(
        'transform', name='{}_{}_{}_{}'.format(CENTER, JAW, GUIDE, GROUP))
    loc_grp = mc.createNode('transform', name='{}_{}_lip_{}_{}'.format(
        CENTER, JAW, GUIDE, GROUP), parent=jaw_guide_grp)
    lip_loc_grp = mc.createNode('transform', name='{}_{}_lipMinor_{}_{}'.format(
        CENTER, JAW, GUIDE, GROUP), parent=loc_grp)

    # create locators
    for part in ['Upper', 'Lower']:

        part_mult = 1 if part == 'Upper' else -1

        mid_data = (0, part_mult, 0)

        mid_loc = mc.spaceLocator(
            name='{}_{}{}_Lip_{}'.format(CENTER, JAW, part, GUIDE))[0]
        mc.parent(mid_loc, lip_loc_grp)

        for side in [LEFT, RIGHT]:
            for x in range(number):
                multiplier = x+1 if side == LEFT else -(x+1)
                loc_data = (multiplier, part_mult, 0)
                loc = mc.spaceLocator(name='{}_{}{}_Lip_{:02d}_{}'.format(
                    side, JAW, part, x+1, GUIDE))[0]
                mc.parent(loc, lip_loc_grp)

                # set data
                mc.setAttr('{}.t'.format(loc), *loc_data)

        # set data
        mc.setAttr('{}.t'.format(mid_loc), *mid_data)

    # create corners
    left_corner_loc = mc.spaceLocator(
        name='{}_{}Corner_Lip_{}'.format(LEFT, JAW, GUIDE))[0]
    right_corner_loc = mc.spaceLocator(
        name='{}_{}Corner_Lip_{}'.format(RIGHT, JAW, GUIDE))[0]

    mc.parent(left_corner_loc, lip_loc_grp)
    mc.parent(right_corner_loc, lip_loc_grp)

    mc.setAttr('{}.t'.format(left_corner_loc), *(number+1, 0, 0))
    mc.setAttr('{}.t'.format(right_corner_loc), *(-(number+1), 0, 0))

    mc.select(clear=True)

    # create jaw base

    jaw_base_guide_grp = mc.createNode('transform', name='{}_{}_base_{}_{}'.format(
        CENTER, JAW, GUIDE, GROUP), parent=jaw_guide_grp)
    jaw_guide = mc.spaceLocator(name='{}_{}_{}'.format(CENTER, JAW, GUIDE))[0]
    inverse_jaw_guide = mc.spaceLocator(
        name='{}_{}inverse_{}'.format(CENTER, JAW, GUIDE))[0]

    # set data
    mc.setAttr('{}.t'.format(jaw_guide), *(0, -1, -number))
    mc.setAttr('{}.t'.format(inverse_jaw_guide), *(0, 1, -number))

    mc.parent(jaw_guide, jaw_base_guide_grp)
    mc.parent(inverse_jaw_guide, jaw_base_guide_grp)

    mc.select(clear=True)


def lip_guides():
    """_summary_

    Returns:
        _type_: _description_
    """

    grp = '{}_{}_lipMinor_{}_{}'.format(CENTER, JAW, GUIDE, GROUP)

    return [loc for loc in mc.listRelatives(grp) if mc.objExists(grp)]


def jaw_guides():
    """_summary_
    """

    grp = '{}_{}_base_{}_{}'.format(CENTER, JAW, GUIDE, GROUP)

    return [loc for loc in mc.listRelatives(grp) if mc.objExists(grp)]


def build():
    """

    Call methods to build joints on guide locators

    """
    createHierarchy()
    createMinorJoints()
    createBroadJoints()
    createJawBase()
    constaintBroadJoints()
    createSeal('upper')
    createSeal('lower')
    createJawAttrs()
    createConstraints()


def createHierarchy():
    """_summary_
    """

    main_grp = mc.createNode(
        'transform', name='{}_{}_rig_{}'.format(CENTER, JAW, GROUP))
    lip_grp = mc.createNode('transform', name='{}_{}Lip_{}'.format(
        CENTER, JAW, GROUP), parent=main_grp)
    base_grp = mc.createNode('transform', name='{}_{}Base_{}'.format(
        CENTER, JAW, GROUP), parent=main_grp)

    lip_minor_grp = mc.createNode('transform', name='{}_{}Lip_minor_{}'.format(
        CENTER, JAW, GROUP), parent=lip_grp)
    lip_broad_grp = mc.createNode('transform', name='{}_{}Lip_broad_{}'.format(
        CENTER, JAW, GROUP), parent=lip_grp)

    mc.select(clear=True)


def createMinorJoints():
    """
    """
    minor_joints = list()

    for guide in lip_guides():
        mat = mc.xform(guide, q=True, m=True, ws=True)
        jnt = mc.joint(name=guide.replace(GUIDE, JOINT))
        mc.setAttr('{}.radius'.format(jnt), 0.5)
        mc.xform(jnt, m=mat, ws=True)
        mc.parent(jnt, '{}_{}Lip_minor_{}'.format(CENTER, JAW, GROUP))

        minor_joints.append(jnt)

    return minor_joints


def createBroadJoints():
    """_summary_
    """

    upper_joint = mc.joint(
        name='{}_{}_broadUpper_{}'.format(CENTER, JAW, JOINT))
    mc.select(clear=True)
    lower_joint = mc.joint(
        name='{}_{}_broadLower_{}'.format(CENTER, JAW, JOINT))
    mc.select(clear=True)
    left_joint = mc.joint(name='{}_{}_broadCorner_{}'.format(LEFT, JAW, JOINT))
    mc.select(clear=True)
    right_joint = mc.joint(
        name='{}_{}_broadCorner_{}'.format(RIGHT, JAW, JOINT))
    mc.select(clear=True)

    # parent joints under broad group
    mc.parent([upper_joint, lower_joint, left_joint, right_joint],
              '{}_{}Lip_broad_{}'.format(CENTER, JAW, GROUP))

    # get guide positions
    upper_pos = mc.xform('{}_{}Upper_Lip_{}'.format(
        CENTER, JAW, GUIDE), q=True, m=True, ws=True)
    lower_pos = mc.xform('{}_{}Lower_Lip_{}'.format(
        CENTER, JAW, GUIDE), q=True, m=True, ws=True)
    left_pos = mc.xform('{}_{}Corner_Lip_{}'.format(
        LEFT, JAW, GUIDE), q=True, m=True, ws=True)
    right_pos = mc.xform('{}_{}Corner_Lip_{}'.format(
        RIGHT, JAW, GUIDE), q=True, m=True, ws=True)

    # set guide positions
    mc.xform(upper_joint, m=upper_pos)
    mc.xform(lower_joint, m=lower_pos)
    mc.xform(left_joint, m=left_pos)
    mc.xform(right_joint, m=right_pos)

    mc.select(clear=True)


def createJawBase():
    """_summary_
    """

    jaw_jnt = mc.joint(name='{}_{}_{}'.format(CENTER, JAW, JOINT))
    jaw_inverse_jnt = mc.joint(
        name='{}_inverse_{}_{}'.format(CENTER, JAW, JOINT))

    jaw_mat = mc.xform(jaw_guides()[0], q=True, m=True, ws=True)
    jaw_inverse_mat = mc.xform(jaw_guides()[1], q=True, m=True, ws=True)

    mc.xform(jaw_jnt, m=jaw_mat, ws=True)
    mc.xform(jaw_inverse_jnt, m=jaw_inverse_mat, ws=True)

    mc.parent(jaw_jnt, '{}_{}Base_{}'.format(CENTER, JAW, GROUP))
    mc.parent(jaw_inverse_jnt, '{}_{}Base_{}'.format(CENTER, JAW, GROUP))

    # add offsets

    addOffset(jaw_jnt, suffix='OFF')
    addOffset(jaw_inverse_jnt, suffix='OFF')

    mc.select(clear=True)


def constaintBroadJoints():
    """
    """

    jaw_joint = '{}_{}_{}'.format(CENTER, JAW, JOINT)
    inverse_jaw_joint = '{}_inverse_{}_{}'.format(CENTER, JAW, JOINT)

    broad_upper = '{}_{}_broadUpper_{}'.format(CENTER, JAW, JOINT)
    broad_lower = '{}_{}_broadLower_{}'.format(CENTER, JAW, JOINT)
    broad_left = '{}_{}_broadCorner_{}'.format(LEFT, JAW, JOINT)
    broad_right = '{}_{}_broadCorner_{}'.format(RIGHT, JAW, JOINT)

    # add offset tp broad joints
    upper_off = addOffset(broad_upper)
    lower_off = addOffset(broad_lower)
    left_off = addOffset(broad_left)
    right_off = addOffset(broad_right)

    # create constaints to upper and lower
    mc.parentConstraint(jaw_joint, lower_off, mo=True)
    mc.parentConstraint(inverse_jaw_joint, upper_off, mo=True)

    # create constaints for corners
    mc.parentConstraint(upper_off, lower_off, left_off, mo=True)
    mc.parentConstraint(upper_off, lower_off, right_off, mo=True)

    mc.select(clear=True)


def getLipParts():
    """_summary_
    """

    upper_token = 'jawUpper'
    lower_token = 'jawLower'
    corner_token = 'jawCorner'

    C_upper = '{}_{}_broadUpper_{}'.format(CENTER, JAW, JOINT)
    C_lower = '{}_{}_broadLower_{}'.format(CENTER, JAW, JOINT)
    L_corner = '{}_{}_broadCorner_{}'.format(LEFT, JAW, JOINT)
    R_corner = '{}_{}_broadCorner_{}'.format(RIGHT, JAW, JOINT)

    sel = mc.listRelatives('{}_{}Lip_{}'.format(
        CENTER, JAW, GROUP), allDescendents=True)
    lip_joints = []
    for i in sel:
        if mc.objectType(i) == 'joint':
            lip_joints.append(i)

    lookup = {'C_upper': {}, 'C_lower': {},
              'L_upper': {}, 'L_lower': {},
              'R_upper': {}, 'R_lower': {},
              'L_corner': {}, 'R_corner': {}}

    for joint in lip_joints:

        if mc.objectType(joint) != 'joint':
            continue

        if joint.startswith('C') and upper_token in joint:
            lookup['C_upper'][joint] = [C_upper]

        if joint.startswith('C') and lower_token in joint:
            lookup['C_lower'][joint] = [C_lower]

        if joint.startswith('L') and upper_token in joint:
            lookup['L_upper'][joint] = [C_upper, L_corner]

        if joint.startswith('L') and lower_token in joint:
            lookup['L_lower'][joint] = [C_lower, L_corner]

        if joint.startswith('R') and upper_token in joint:
            lookup['R_upper'][joint] = [C_upper, R_corner]

        if joint.startswith('R') and lower_token in joint:
            lookup['R_lower'][joint] = [C_lower, R_corner]

        if joint.startswith('L') and corner_token in joint:
            lookup['L_corner'][joint] = [L_corner]

        if joint.startswith('R') and corner_token in joint:
            lookup['R_corner'][joint] = [R_corner]

    return lookup


def lipPart(part):
    """_summary_

    Args:
        part (_type_): _description_
    """

    lip_parts = [reversed(sorted(getLipParts()['L_{}'.format(part)].keys())), sorted(getLipParts()['C_{}'.format(part)].keys()),
                 sorted(getLipParts()['R_{}'.format(part)].keys())]

    return [joint for joint in lip_parts for joint in joint]


def createSeal(part):
    """_summary_

    Args:
        part (_type_): _description_
    """

    seal_name = '{}_seal_{}'.format(CENTER, GROUP)
    seal_parent = seal_name if mc.objExists(seal_name) else \
        mc.createNode(
            'transform', name=seal_name, parent='{}_{}_rig_{}'.format(CENTER, JAW, GROUP))

    part_grp = mc.createNode(
        'transform', name=seal_name.replace('seal', 'seal_{}'.format(part)), parent=seal_parent)

    l_corner = '{}_{}_broadCorner_{}'.format(LEFT, JAW, JOINT)
    r_corner = '{}_{}_broadCorner_{}'.format(RIGHT, JAW, JOINT)

    value = len(lipPart(part))

    for index, joint, in enumerate(lipPart(part)):
        node = mc.createNode(
            'transform', name=joint.replace('JNT', '{}_SEAL'.format(part)), parent=part_grp)
        mat = mc.xform(
            joint, q=True, m=True, ws=True)
        mc.xform(
            node, m=mat, ws=True)

        constraint = mc.parentConstraint(
            l_corner, r_corner, node, mo=True)[0]
        mc.setAttr(
            '{}.interpType'.format(constraint), 2)

        r_corner_value = float(index) / float(value - 1)
        l_corner_value = 1 - r_corner_value

        l_corner_attr = '{}.{}W0'.format(constraint, l_corner)
        r_corner_attr = '{}.{}W1'.format(constraint, r_corner)

        mc.setAttr(l_corner_attr, l_corner_value)
        mc.setAttr(r_corner_attr, r_corner_value)


def createJawAttrs():
    """

    """
    node = mc.createNode('transform', name='jaw_atributes',
                         parent='{}_{}_rig_{}'.format(CENTER, JAW, GROUP))
    mc.addAttr(node, ln=sorted(getLipParts()['C_upper'].keys())[
               0], min=0, max=1, dv=0)
    mc.setAttr('{}.{}'.format(node, sorted(
        getLipParts()['C_upper'].keys())[0]), lock=1)

    for upper in sorted(getLipParts()['L_upper'].keys()):
        mc.addAttr(node, ln=upper, min=0, max=1, dv=0)

    mc.addAttr(node, ln=sorted(getLipParts()['L_corner'].keys())[
               0], min=0, max=1, dv=1)
    mc.setAttr('{}.{}'.format(node, sorted(
        getLipParts()['L_corner'].keys())[0]), lock=1)

    for lower in sorted(getLipParts()['L_lower'].keys())[::-1]:
        mc.addAttr(node, ln=lower, min=0, max=1, dv=0)

    mc.addAttr(node, ln=sorted(getLipParts()['C_lower'].keys())[
               0], min=0, max=1, dv=0)
    mc.setAttr('{}.{}'.format(node, sorted(
        getLipParts()['C_lower'].keys())[0]), lock=1)


def createConstraints():
    """_summary_
    """
    for value in getLipParts().values():
        for lip_jnt, broad_jnt in value.items():

            seal_token = 'upper_SEAL' if 'Upper' in lip_jnt else 'lower_SEAL'
            lip_seal = lip_jnt.replace(JOINT, seal_token)

            if mc.objExists(lip_seal):
                const = mc.parentConstraint(
                    broad_jnt, lip_seal, lip_jnt, mo=True)[0]
                mc.setAttr('{}.interpType'.format(const), 2)

                if len(broad_jnt) == 1:
                    seal_attr = '{}_parentConstraint1.{}W1'.format(
                        lip_jnt, lip_seal)
                    rev = mc.createNode(
                        'reverse', name=lip_jnt.replace(JOINT, 'REV'))
                    mc.connectAttr(
                        seal_attr, '{}.inputX'.format(rev))
                    mc.connectAttr(
                        '{}.outputX'.format(rev), '{}_parentConstraint1.{}W0'.format(lip_jnt, broad_jnt[0]))
                    mc.setAttr(seal_attr, 0)

                if len(broad_jnt) == 2:
                    seal_attr = '{}_parentConstraint1.{}W2'.format(
                        lip_jnt, lip_seal)
                    mc.setAttr(seal_attr, 0)

                    seal_rev = mc.createNode('reverse', name=lip_jnt.replace(
                        'JNT', 'seal_REV'))
                    jaw_attr_rev = mc.createNode('reverse', name=lip_jnt.replace(
                        'JNT', 'jaw_attr_REV'))
                    seal_mult = mc.createNode('multiplyDivide', name=lip_jnt.replace(
                        'JNT', 'seal_MULT'))

                    mc.connectAttr(seal_attr, '{}.inputX'.format(seal_rev))
                    mc.connectAttr('{}.outputX'.format(seal_rev),
                                   '{}.input2X'.format(seal_mult))
                    mc.connectAttr('{}.outputX'.format(seal_rev),
                                   '{}.input2Y'.format(seal_mult))

                    mc.connectAttr(
                        'jaw_atributes.{}'.format(
                            lip_jnt.replace(lip_jnt[0], 'L')),
                        '{}.input1Y'.format(seal_mult))

                    mc.connectAttr(
                        'jaw_atributes.{}'.format(
                            lip_jnt.replace(lip_jnt[0], 'L')),
                        '{}.inputX'.format(jaw_attr_rev))

                    mc.connectAttr(
                        '{}.outputX'.format(jaw_attr_rev)),
                    '{}.input1X'.format(seal_mult)

                    mc.connectAttr(
                        '{}.outputX'.format(seal_mult)),
                    '{}_parentConstraint1.{}W0'.format(lip_jnt, broad_jnt[0])

                    mc.connectAttr(
                        '{}.outputY'.format(seal_mult)),
                    '{}_parentConstraint1.{}W1'.format(lip_jnt, broad_jnt[1])

            else:
                const = mc.parentConstraint(
                    broad_jnt, lip_jnt, mo=True)[0]
                mc.setAttr(
                    '{}.interpType'.format(const), 2)
