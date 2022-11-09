'''
#-------------------------------------------------------------#
#Leg Auto rig

Builds out the rig on top of existing BN joints as a base

Current feature are:
Auto IKFK Switch
Auto Pole Vector

Future Plans:
Auto Roll Joints
#-------------------------------------------------------------#
'''

import maya.cmds as mc
import maya.mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui

rigType = 'Leg'
side = 'R_'
name = side + rigType
controlerSize = 6

ROOT = ''
MID = ''
END = ''

sel = mc.ls(sl=True)
rigGroup = mc.group(em=True, n=name + 'Grp')

# getting xform data from bind joints
xform0 = mc.xform('R_Thigh_BN_JNT', q=True, m=True, ws=True)
xform1 = mc.xform('R_Calf_BN_JNT', q=True, m=True, ws=True)
xform2 = mc.xform('R_Ankle_BN_JNT', q=True, m=True, ws=True)

# getting xform data from bind joints
BN0_mat = mc.xform('R_Thigh_BN_JNT', q=True, m=True, ws=True)
BN1_mat = mc.xform('R_Calf_BN_JNT', q=True, m=True, ws=True)
BN2_mat = mc.xform('R_Ankle_BN_JNT', q=True, m=True, ws=True)

BN0_pos = mc.xform('R_Thigh_BN_JNT', q=True, t=True, ws=True)
BN1_pos = mc.xform('R_Calf_BN_JNT', q=True, t=True, ws=True)
BN2_pos = mc.xform('R_Ankle_BN_JNT', q=True, t=True, ws=True)

# Duplicate Base Arm

mc.duplicate('R_Thigh_BN_JNT', n='R_Thigh_BN_JNT'.replace('BN', 'DRIVER'), po=True)[0]
mc.duplicate('R_Calf_BN_JNT', n='R_Calf_BN_JNT'.replace('BN', 'DRIVER'), po=True)[0]
mc.duplicate('R_Ankle_BN_JNT', n='R_Ankle_BN_JNT'.replace('BN', 'DRIVER'), po=True)[0]

mc.duplicate('R_Thigh_BN_JNT', n='R_Thigh_BN_JNT'.replace('BN', 'FK'), po=True)[0]
mc.duplicate('R_Calf_BN_JNT', n='R_Calf_BN_JNT'.replace('BN', 'FK'), po=True)[0]
mc.duplicate('R_Ankle_BN_JNT', n='R_Ankle_BN_JNT'.replace('BN', 'FK'), po=True)[0]

mc.duplicate('R_Thigh_BN_JNT', n='R_Thigh_BN_JNT'.replace('BN', 'IK'), po=True)[0]
mc.duplicate('R_Calf_BN_JNT', n='R_Calf_BN_JNT'.replace('BN', 'IK'), po=True)[0]
mc.duplicate('R_Ankle_BN_JNT', n='R_Ankle_BN_JNT'.replace('BN', 'IK'), po=True)[0]

mc.parent('R_Ankle_BN_JNT'.replace('BN', 'DRIVER'), 'R_Calf_BN_JNT'.replace('BN', 'DRIVER'))
mc.parent('R_Calf_BN_JNT'.replace('BN', 'DRIVER'), 'R_Thigh_BN_JNT'.replace('BN', 'DRIVER'))
mc.parent('R_Thigh_BN_JNT'.replace('BN', 'DRIVER'), rigGroup)
mc.parent('R_Ankle_BN_JNT'.replace('BN', 'FK'), 'R_Calf_BN_JNT'.replace('BN', 'FK'))
mc.parent('R_Calf_BN_JNT'.replace('BN', 'FK'), 'R_Thigh_BN_JNT'.replace('BN', 'FK'))
mc.parent('R_Thigh_BN_JNT'.replace('BN', 'FK'), rigGroup)
mc.parent('R_Ankle_BN_JNT'.replace('BN', 'IK'), 'R_Calf_BN_JNT'.replace('BN', 'IK'))
mc.parent('R_Calf_BN_JNT'.replace('BN', 'IK'), 'R_Thigh_BN_JNT'.replace('BN', 'IK'))
mc.parent('R_Thigh_BN_JNT'.replace('BN', 'IK'), rigGroup)

# Create FK chain list

chainList = []
chainList.append('R_Thigh_BN_JNT'.replace('BN', 'FK'))
chainList.append('R_Calf_BN_JNT'.replace('BN', 'FK'))
chainList.append('R_Ankle_BN_JNT'.replace('BN', 'FK'))
mc.select(cl=True)


newchainList = []
topnode = []
controlList = []

sdkcheck = 0
offcheck = 0

for i in chainList:

    if 'BN_JNT' in i:
        namereplace = 'BN_JNT'
    elif 'FK_JNT' in i:
        namereplace = 'FK_JNT'
    elif 'IK_JNT' in i:
        namereplace = 'IK_JNT'

    con = mc.circle(n=i.replace(namereplace, 'CON'),
                    nr=[1, 0, 0], sw=360, r=controlerSize)
    if sdkcheck:
        sdkgrp = mc.group(n=i.replace(namereplace, 'SDK_GRP'))
    if offcheck:
        offgrp = mc.group(n=i.replace(namereplace, 'OFF_GRP'))
    grp = mc.group(n=i.replace(namereplace, 'GRP'))
    const = mc.parentConstraint(i, grp, mo=0)
    mc.delete(const)
    mc.parentConstraint(con, i, mo=True)

    newchainList.append(grp)
    newchainList.append(con[0])
    controlList.append(con[0])
    topnode.append(grp)

# connect fk controls

newchainList.pop(0)

for i in range(int(len(newchainList)/2)):
    i = i * 2
    mc.parent(newchainList[i+1], newchainList[i])

mc.parent(topnode[0], rigGroup)

# create ik
IKR_GRP = mc.createNode('transform', name='{}_IKR_GRP'.format(name))

IKR_Handle = mc.ikHandle(
    name='{}_IKR'.format(name), sol='ikRPsolver', sj='R_Thigh_BN_JNT'.replace('BN', 'IK'), ee='R_Ankle_BN_JNT'.replace('BN', 'IK'))[0]

# Create Control
IKR_ankle_control = mc.curve(n='{}_ik_control'.format(
    name), d=1, p=[[-0.989623460780981, 1.0031016006564133, 1.0031016006564133],
                   [-0.989623460780981, 1.0031016006564133, -1.0031016006564133],
                   [-0.989623460780981, -1.0031016006564133, -1.0031016006564133],
                   [-0.989623460780981, -1.0031016006564133, 1.0031016006564133],
                   [-0.989623460780981, 1.0031016006564133, 1.0031016006564133],
                   [0.989623460780981, 1.0031016006564133, 1.0031016006564133],
                   [0.989623460780981, -1.0031016006564133, 1.0031016006564133],
                   [-0.989623460780981, -1.0031016006564133, 1.0031016006564133],
                   [0.989623460780981, -1.0031016006564133, 1.0031016006564133],
                   [0.989623460780981, -1.0031016006564133, -1.0031016006564133],
                   [0.989623460780981, 1.0031016006564133, -1.0031016006564133],
                   [-0.989623460780981, 1.0031016006564133, -1.0031016006564133],
                   [-0.989623460780981, -1.0031016006564133, -1.0031016006564133],
                   [0.989623460780981, -1.0031016006564133, -1.0031016006564133],
                   [0.989623460780981, 1.0031016006564133, -1.0031016006564133],
                   [0.989623460780981, 1.0031016006564133, 1.0031016006564133]])

# Parenting
mc.xform(IKR_ankle_control, m=xform2, ws=True)
mc.parent(IKR_Handle, IKR_ankle_control)
mc.parent(IKR_ankle_control, IKR_GRP)
mc.parent(IKR_GRP, rigGroup)

# Orient constraint to the ik wrist

mc.orientConstraint(IKR_ankle_control, 'R_Ankle_BN_JNT'.replace('BN', 'IK'))


# Create Blend Colors

root_blend_color = mc.createNode(
    'blendColors', name='{}_Thigh_BLENDECOLOR'.format(name))
mid_blend_color = mc.createNode(
    'blendColors', name='{}_Knee_BLENDECOLOR'.format(name))
end_blend_color = mc.createNode(
    'blendColors', name='{}_Ankle_BLENDECOLOR'.format(name))

blenderList = []
blenderList.append(root_blend_color)
blenderList.append(mid_blend_color)
blenderList.append(end_blend_color)


# Connecting IKFK blender root
mc.connectAttr(
    ('{}.rotate'.format('R_Thigh_BN_JNT'.replace('BN', 'FK'))), '{}.color1'.format(root_blend_color))
mc.connectAttr(
    ('{}.rotate'.format('R_Thigh_BN_JNT'.replace('BN', 'IK'))), '{}.color2'.format(root_blend_color))
mc.connectAttr(
    ('{}.output'.format(root_blend_color)),'{}.rotate'.format('R_Thigh_BN_JNT'.replace('BN', 'DRIVER')))

# Connecting IKFK blender mid
mc.connectAttr(
    ('{}.rotate'.format('R_Calf_BN_JNT'.replace('BN', 'FK'))), '{}.color1'.format(mid_blend_color))
mc.connectAttr(
    ('{}.rotate'.format('R_Calf_BN_JNT'.replace('BN', 'IK'))), '{}.color2'.format(mid_blend_color))
mc.connectAttr(
    ('{}.output'.format(mid_blend_color)), '{}.rotate'.format('R_Calf_BN_JNT'.replace('BN', 'DRIVER')))

# Connecting IKFK blender end
mc.connectAttr(
    ('{}.rotate'.format('R_Ankle_BN_JNT'.replace('BN', 'FK'))), '{}.color1'.format(end_blend_color))
mc.connectAttr(
    ('{}.rotate'.format('R_Ankle_BN_JNT'.replace('BN', 'IK'))), '{}.color2'.format(end_blend_color))
mc.connectAttr(
    ('{}.output'.format(end_blend_color)), '{}.rotate'.format('R_Ankle_DRIVER_JNT'.replace('BN', 'DRIVER')))

# Create Parent Constraints--------------------------------------------------------|

#mc.parentConstraint('R_Thigh_BN_JNT'.replace('BN', 'FK'), 'R_Thigh_BN_JNT', mo=True)
mc.parentConstraint('R_Thigh_BN_JNT'.replace('BN', 'DRIVER'), 'R_Thigh_BN_JNT', mo=True)
mc.parentConstraint('R_Calf_BN_JNT'.replace('BN', 'DRIVER'), 'R_Calf_BN_JNT', mo=True)
mc.parentConstraint('R_Ankle_BN_JNT'.replace('BN', 'DRIVER'), 'R_Ankle_BN_JNT', mo=True)

# Create Container----------------------------------------------------------------|

ikfk_attributes_Grp = mc.createNode(
    'transform', name='{}_ATRIBUTES_GRP'.format(name))
mc.addAttr(ln='IKFK_Switch', at='float', k=True,  min=0, max=1)

arm_attributes_asset = mc.container(name='{}_ASSET'.format(name))
mc.container(arm_attributes_asset, e=True, ish=True,
             f=True, an=ikfk_attributes_Grp)

IKFK_reverse = mc.createNode('reverse', n='{}_IKFK_reverse'.format(name))

# Connect attribute to the reverse
mc.connectAttr(ikfk_attributes_Grp + '.IKFK_Switch',
               IKFK_reverse + '.input.inputX')

# Connect the reverse to the blend color nodes
mc.connectAttr(IKFK_reverse + '.input.inputX', root_blend_color + '.blender')
mc.connectAttr(IKFK_reverse + '.input.inputX', mid_blend_color + '.blender')
mc.connectAttr(IKFK_reverse + '.input.inputX', end_blend_color + '.blender')

# Add controls to the asset

for i in controlList, blenderList:

    mc.container(arm_attributes_asset, edit=True, addNode=i)
mc.container(arm_attributes_asset, edit=True, addNode=IKR_ankle_control)

# Publish name 'IKFK Switch'
mc.container(arm_attributes_asset, e=True, pn=('IKFK_Switch'))

# Bind ikfk attribute from the group to the container asset
mc.container(arm_attributes_asset, e=True, ba=(
    ikfk_attributes_Grp + '.IKFK_Switch', 'IKFK_Switch'))


# Creating pole target--------------------------------------------------------------------|

distance = 1.0
root_joint_pos = mc.xform('R_Thigh_BN_JNT'.replace('BN', 'IK'), q=1, ws=1, t=1)
mid_joint_pos = mc.xform('R_Calf_BN_JNT'.replace('BN', 'IK'), q=1, ws=1, t=1)
end_joint_pos = mc.xform('R_Ankle_BN_JNT'.replace('BN', 'IK'), q=1, ws=1, t=1)

# Create locator at the vector position and create pole vector constraint


def create_pv(pos, IKR=IKR_Handle):

    # create pole vector shape
    pv_group = mc.createNode('transform', name='{}_PV_GRP'.format(name))

    pv_control = mc.curve(
        n='{}_PV_CON'.format(name), d=1, p=[[-0.989623460780981, 1.0031016006564133, 1.0031016006564133],
                                            [-0.989623460780981,
                                                1.0031016006564133, -1.0031016006564133],
                                            [-0.989623460780981, -
                                                1.0031016006564133, -1.0031016006564133],
                                            [-0.989623460780981, -
                                                1.0031016006564133, 1.0031016006564133],
                                            [-0.989623460780981, 1.0031016006564133,
                                                1.0031016006564133],
                                            [0.989623460780981, 1.0031016006564133,
                                                1.0031016006564133],
                                            [0.989623460780981, -1.0031016006564133,
                                                1.0031016006564133],
                                            [-0.989623460780981, -
                                                1.0031016006564133, 1.0031016006564133],
                                            [0.989623460780981, -1.0031016006564133,
                                                1.0031016006564133],
                                            [0.989623460780981, -
                                                1.0031016006564133, -1.0031016006564133],
                                            [0.989623460780981,
                                                1.0031016006564133, -1.0031016006564133],
                                            [-0.989623460780981,
                                                1.0031016006564133, -1.0031016006564133],
                                            [-0.989623460780981, -
                                                1.0031016006564133, -1.0031016006564133],
                                            [0.989623460780981, -
                                                1.0031016006564133, -1.0031016006564133],
                                            [0.989623460780981,
                                                1.0031016006564133, -1.0031016006564133],
                                            [0.989623460780981, 1.0031016006564133, 1.0031016006564133]])

    mc.setAttr((pv_group + '.overrideEnabled'), 1)
    if 'R_' in pv_control:
        mc.setAttr((pv_group + '.overrideColor'), 6)
    elif 'R_' in pv_control:
        mc.setAttr((pv_group + '.overrideColor'), 13)
    else:
        mc.setAttr((pv_group + '.overrideColor'), 17)

    # Parent and move controll
    mc.parent(pv_control, pv_group)
    mc.move(pos.x, pos.y, pos.z, pv_group)
    mc.poleVectorConstraint(pv_control, IKR)
    mc.parent(pv_group, rigGroup)
    mc.container(arm_attributes_asset, edit=True, addNode=pv_control)

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
    totaR_len = (root_to_mid_len + mid_to_end_len)

    pole_vec_pos = (mid_joint_vec - proj_vec).normal() * \
        distance * totaR_len + mid_joint_vec

    create_pv(pole_vec_pos)


get_pole_vec_pos(root_joint_pos, mid_joint_pos, end_joint_pos)

mc.parentConstraint('Pelvis_CON', rigGroup, mo = 1)
mc.addAttr('R_Leg_PV_CON', ln='SpaceSwitch', at='enum', en='world:leg:pelvis')
mc.setAttr('R_Leg_PV_CON.SpaceSwitch', e=1, k=1)