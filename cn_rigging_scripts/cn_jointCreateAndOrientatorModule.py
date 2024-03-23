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
        self.baseJnt = mc.joint(rad=10)
        mc.select(cl=1)
        const = mc.parentConstraint(clstr, self.baseJnt, mo=0)
        mc.delete(const, clstr)
        mc.select(sel)
        mc.hilite(sel, tgl=1)

    def endBaseJoint(self):

        clstr = mc.cluster()
        mc.select(cl=1)
        self.endJnt = mc.joint(rad=10)
        mc.select(cl=1)
        const = mc.parentConstraint(clstr, self.endJnt, mo=0)
        mc.delete(const, clstr)
        self.parentAndOrient()

    def parentAndOrient(self):

        mc.parent(self.endJnt, self.baseJnt)

        mc.joint(self.baseJnt, e=True, oj="xyz", secondaryAxisOrient="zdown", ch=True)

        mc.joint(self.endJnt, e=True, oj="none", ch=True)
