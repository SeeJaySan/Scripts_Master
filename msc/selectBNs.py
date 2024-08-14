import maya.cmds as mc


def selectBNs():
    
    bnselection = []

    sel = mc.ls(type="joint")

    for i in sel:
        if "BN" in i:
            bnselection.append(i)

    mc.select(bnselection[:])
