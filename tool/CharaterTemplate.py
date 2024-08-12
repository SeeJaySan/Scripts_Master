import maya.cmds as mc
import maya.mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui

def main():
    ToolOps_CharacterTemplate()

def ToolOps_CharacterTemplate(charactername="template"):
    mc.createNode("transform", n="GEO")
    mc.createNode("transform", n="SKL")
    mc.createNode("transform", n="RIG")
    mc.createNode("transform", n="CON")
    mc.select(cl=1)

    mc.createNode("transform", n="{}_Grp".format(charactername))
    mc.select(cl=1)

    mc.parent("GEO", "SKL", "RIG", "CON", "{}_Grp".format(charactername))