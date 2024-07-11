import maya.cmds as mc
import maya.mel as mel


def main():
    AnimOps_CopyPasteKeys()


class AnimOps_CopyPasteKeys(object):

    sel = cmds.ls (sl=True)
    mc.cutKey (sel[0], animation='objects', option='keys')
    mc.pasteKey (sel[1], animation='objects', option='replaceCompletely')