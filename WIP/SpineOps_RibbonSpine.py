from maya import cmds as mc
import maya.mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui

mc.createNode('transform', n = 'RibbonSpine_System')

bnList = []
follower = []
driver = []
jointControls = []
matList = []

bnList.append('Pelvis_BN_JNT')
bnList.append('Spine1_BN_JNT')
bnList.append('Spine2_BN_JNT')
bnList.append('Spine3_BN_JNT')
bnList.append('Chest_BN_JNT')

PelvisPos = mc.xform('Pelvis_BN_JNT', t=True, ws=True, q=True)
Spine1Pos = mc.xform('Spine1_BN_JNT', t=True, ws=True, q=True)
Spine2Pos = mc.xform('Spine2_BN_JNT', t=True, ws=True, q=True)
Spine3Pos = mc.xform('Spine3_BN_JNT', t=True, ws=True, q=True)
ChestPos = mc.xform('Chest_BN_JNT', t=True, ws=True, q=True)

PelvisMat = mc.xform('Pelvis_BN_JNT', m=True, ws=True, q=True)
Spine1Mat = mc.xform('Spine1_BN_JNT', m=True, ws=True, q=True)
Spine2Mat = mc.xform('Spine2_BN_JNT', m=True, ws=True, q=True)
Spine3Mat = mc.xform('Spine3_BN_JNT', m=True, ws=True, q=True)
ChestMat = mc.xform('Chest_BN_JNT', m=True, ws=True, q=True)
matList.append(PelvisMat)
matList.append(Spine1Mat)
matList.append(Spine2Mat)
matList.append(Spine3Mat)
matList.append(ChestMat)


def buildSurface():
    
    crvs = mc.curve(d=3, p=[(PelvisPos[0], PelvisPos[1], PelvisPos[2]), (Spine1Pos[0], Spine1Pos[1], Spine1Pos[2]), (Spine2Pos[0], Spine2Pos[1], Spine2Pos[2]), (Spine3Pos[0], Spine3Pos[1], Spine3Pos[2]), (ChestPos[0], ChestPos[1], ChestPos[2])], k = [0, 0, 0, 1, 2])
    mc.xform( crvs, t = [.1,0,0], os = True)
    dup = mc.duplicate(crvs)
    mc.xform( dup, t = [-1,0,0], os = True)
    mc.loft(dup, crvs, n = 'Ribbon_Spline_CRVS', rb = True)
    mc.parent('Ribbon_Spline_CRVS', 'RibbonSpine_System')
    #mc.delete(dup, crvs)

def dupJoints():
    
    group = mc.createNode('transform', n = 'RS_followers')
    mc.parent(group, 'RibbonSpine_System')
    
    for i in range(len(bnList)):
        dup = mc.duplicate(bnList[i], n = bnList[i].replace('BN', 'follower'), po = True)[0]
        mc.parent(dup, 'RS_followers')
        follower.append(dup)

def createDrivers():
    
    group = mc.createNode('transform', n = 'RS_drivers')
    mc.parent(group, 'RibbonSpine_System')
    
    for i in range(len(follower)):
        dup = mc.duplicate(follower[i], n = follower[i].replace('follower', 'driver'), po = True)[0]
        mc.parent(dup, 'RS_drivers')
        driver.append(dup)
    
    for i in range(len(follower)):
        mc.connectAttr(follower[i] + '.translate', driver[i] + '.translate')
        mc.connectAttr(follower[i] + '.rotate', driver[i] + '.rotate')
        mc.connectAttr(follower[i] + '.scale', driver[i] + '.scale')

'''def constrainSuface():
    
    constList = []
    constList.append('Ribbon_Spline_CRVS')
    
    for i in range(len(follower)):
        constList.append(follower[i])
    print (constList)
    
    sel = mc.select(constList[:])
    mc.UVPin(sel)'''
    
def createHair():
    pass
    
    
        
        
        
    
def doit():
    buildSurface()
    #dupJoints()
    #createDrivers()
    #constrainSuface()
    
doit()