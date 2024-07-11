from maya import cmds as mc

# snap
# 6 is blue
# 13 is red
# 17 is yellow


def main():
    ToolOps_CharacterTemplate()
    
    

sel = mc.ls(sl = 1)

for i in sel:
    mc.setAttr(i + '.overrideEnabled', 1)
    mc.setAttr((i + '.overrideColor'), 17)