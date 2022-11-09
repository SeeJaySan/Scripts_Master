import maya.cmds as mc

sel = cmds.ls (sl=True)
mc.cutKey (sel[0], animation='objects', option='keys')
mc.pasteKey (sel[1], animation='objects', option='replaceCompletely')