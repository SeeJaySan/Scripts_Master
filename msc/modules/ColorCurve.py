from maya import cmds as mc

# 6 is blue
# 13 is red
# 17 is yellow


def main(*args):
    ColorCurves()


def ColorCurves():
    CurveSelection = mc.ls(sl=1)

    for currentCurve in CurveSelection:
        mc.setAttr(f"{currentCurve}.overrideEnabled", 1)
        mc.setAttr((f"{currentCurve}.overrideColor"), 17)