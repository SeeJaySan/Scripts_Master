from maya import cmds as mc
from maya import mel as mel


class jointCreateAndOrientator(object):

    def __init__(self):
        self.baseJnt = []
        self.endJnt = []

    def createBaseJoint(self):

        sel = mc.ls(sl=1)
        clstr = mc.cluster()
        mc.select(cl=1)
        self.baseJnt = mc.joint(rad=1)
        mc.select(cl=1)
        const = mc.parentConstraint(clstr, self.baseJnt, mo=0)
        mc.delete(const, clstr)
        mc.select(sel)
        mc.hilite(sel, tgl=1)

    def endBaseJoint(self):

        clstr = mc.cluster()
        mc.select(cl=1)
        self.endJnt = mc.joint(rad=1)
        mc.select(cl=1)
        const = mc.parentConstraint(clstr, self.endJnt, mo=0)
        mc.delete(const, clstr)
        self.parentAndOrient()

    def parentAndOrient(self):

        mc.parent(self.endJnt, self.baseJnt)

        mc.joint(self.baseJnt, e=True, oj="xyz", secondaryAxisOrient="zup", ch=True)

        mc.joint(self.endJnt, e=True, oj="none", ch=True)
        
    def turnOnJointAxisVis(self):
    # bm_axisDisplay
    # Forces the Local Rotation Axis display on or off for all joints or for the selected joints
        # if no joints are selected, do it for all the joints in the scene
        
        if len(mc.ls(sl=1, type="joint")) == 0:
            jointList = mc.ls(type="joint")
        else:
            jointList = mc.ls(sl=1, type="joint")
        # set the displayLocalAxis attribute to what the user specifies.
        for jnt in jointList:
            mc.setAttr(jnt + ".displayLocalAxis", 1)
            
    def turnOffJointAxisVis(self):
    # bm_axisDisplay
    # Forces the Local Rotation Axis display on or off for all joints or for the selected joints
        # if no joints are selected, do it for all the joints in the scene
        
        if len(mc.ls(sl=1, type="joint")) == 0:
            jointList = mc.ls(type="joint")
        else:
            jointList = mc.ls(sl=1, type="joint")
        # set the displayLocalAxis attribute to what the user specifies.
        for jnt in jointList:
            mc.setAttr(jnt + ".displayLocalAxis", 0)
            
    def createControl(self):
        print("this is a placeholder")
