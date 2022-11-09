import maya.cmds as mc

bnselection = []

sel = mc.ls(type='joint')

for i in sel:
    if 'BN' in i:
        bnselection.append(i)
        
mc.select(bnselection[:])