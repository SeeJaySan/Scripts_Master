###
#
# load scripts into
#
#
###

# Imports
import sys
import os
import importlib
import maya.cmds as mc


# module path(s)
path = r"C:\Users\cjnowacek\Desktop\important files\scripts\myScript\live"

# TODO write a custom path widow if the path isn't found

if path == bool(os.path.exists(path)):
    pass
else:
    # TODO write a custom path widow if the path isn't found -- get the code from the geoExporter
    pass

# cycle through all moduals and reload them - TODO
for module_name in list(sys.modules.keys()):
    top_module = module_name.split(".")[0]
    print(top_module)

    # reloading for modules

    if top_module == "AnimOps_Macros":
        importlib.reload((sys.modules[module_name]))

    if top_module == "BfaOps_AnimExportPrep":
        importlib.reload((sys.modules[module_name]))

    if top_module == "BfaOps_AnimExporter":
        importlib.reload((sys.modules[module_name]))

    if top_module == "RigOps_CreateContols":
        importlib.reload((sys.modules[module_name]))

    if top_module == "RigOp_ArmIKFKSwitch":
        importlib.reload((sys.modules[module_name]))

    if top_module == "RigOp_LegIKFKSwitch":
        importlib.reload((sys.modules[module_name]))

    if top_module == "RigOps_MirrorJnts":
        importlib.reload((sys.modules[module_name]))

    if top_module == "ToolOps_CharaterTemplate":
        importlib.reload((sys.modules[module_name]))

    if top_module == "ToolOps_BatchGeoExporter":
        importlib.reload((sys.modules[module_name]))

    if top_module == "ToolOps_CharacterExporter":
        importlib.reload((sys.modules[module_name]))

    if top_module == "ToolOps_ControlCreator":
        importlib.reload((sys.modules[module_name]))

    if top_module == "SkinOps_Painter":
        importlib.reload((sys.modules[module_name]))


# making sure the path is correct so we can import
if path not in sys.path:
    sys.path.append(path)

# importing modules
import AnimOps_Macros  # type: ignore
import BfaOps_AnimExportPrep  # type: ignore
import BfaOps_AnimExporter  # type: ignore
import RigOps_CreateContols  # type: ignore
import RigOp_ArmIKFKSwitch  # type: ignore
import RigOp_LegIKFKSwitch  # type: ignore
import RigOps_MirrorJnts  # type: ignore
import ToolOps_CharaterTemplate  # type: ignore
import ToolOps_BatchGeoExporter  # type: ignore
import ToolOps_CharacterExporter  # type: ignore
import ToolOps_ControlCreator  # type: ignore
import rig.wip.Tool_SkinPainter as Tool_SkinPainter


class ToolOps_Menu(object):

    # constructor
    def __init__(self):

        self.window = "ToolOps_Menu"
        self.title = "Tools Menu"
        self.height = 80
        self.width = 120

        # close old window is open
        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window, window=True)

        # create new window
        self.window = mc.window(self.window, title=self.title)

        mc.columnLayout(adjustableColumn=True)
        mc.text(self.title)
        mc.separator(height=20)

        self.options_menu = mc.optionMenu("this", label="Ops")
        mc.menuItem(label="__________AnimOps____________", enable=False)
        mc.menuItem(label="AnimOps_Macros", parent=self.options_menu)
        mc.menuItem(label="__________BfaOps____________", enable=False)
        # mc.menuItem( label='BfaOps_AnimExportPrep', parent = self.options_menu )
        mc.menuItem(label="BfaOps_AnimExporter", parent=self.options_menu)
        mc.menuItem(label="__________RigOps____________", enable=False)
        mc.menuItem(label="RigOps_CreateContols", parent=self.options_menu)
        mc.menuItem(label="RigOp_ArmIKFKSwitch", parent=self.options_menu)
        mc.menuItem(label="RigOp_LegIKFKSwitch", parent=self.options_menu)
        mc.menuItem(label="RigOps_MirrorJnts", parent=self.options_menu)
        mc.menuItem(label="__________ToolOps____________", enable=False)
        mc.menuItem(label="ToolOps_CharaterTemplate", parent=self.options_menu)
        mc.menuItem(label="ToolOps_BatchGeoExporter", parent=self.options_menu)
        mc.menuItem(label="ToolOps_CharacterExporter", parent=self.options_menu)
        mc.menuItem(label="ToolOps_ControlCreator", parent=self.options_menu)
        mc.menuItem(label="__________SkinOps____________", enable=False)
        mc.menuItem(label="SkinOps_Painter", parent=self.options_menu)

        mc.optionMenu(self.options_menu, e=True, sl=2)

        self.Execute_bn = mc.button(label="Execute", command=self.Execute)
        mc.setParent("..")

        # display new window
        mc.showWindow()
        mc.window(
            self.window,
            e=True,
            height=self.height,
            width=self.width,
            mnb=False,
            mxb=False,
        )

    def Execute(self, *args):

        # getting file type and options
        commandOption = str(mc.optionMenu(self.options_menu, q=True, value=True))

        if commandOption == "AnimOps_Macros":
            AnimOps_Macros.AnimOps_Macros()
        if commandOption == "BfaOps_AnimExportPrep":
            BfaOps_AnimExportPrep.BfaOps_AnimExportPrep()
        if commandOption == "BfaOps_AnimExporter":
            BfaOps_AnimExporter.BfaOps_AnimExporter()
        if commandOption == "RigOps_CreateContols":
            RigOps_CreateContols.RigOps_CreateContols()
        if commandOption == "RigOp_ArmIKFKSwitch":
            RigOp_ArmIKFKSwitch.RigOp_ArmIKFKSwitch()
        if commandOption == "RigOp_LegIKFKSwitch":
            RigOp_LegIKFKSwitch.RigOp_LegIKFKSwitch()
        if commandOption == "RigOps_MirrorJnts":
            RigOps_MirrorJnts.RigOps_MirrorJnts()
        if commandOption == "ToolOps_CharaterTemplate":
            ToolOps_CharaterTemplate.ToolOps_CharaterTemplate()
        if commandOption == "ToolOps_BatchGeoExporter":
            ToolOps_BatchGeoExporter.ToolOps_BatchGeoExporter()
        if commandOption == "ToolOps_CharacterExporter":
            ToolOps_CharacterExporter.ToolOps_CharacterExporter()
        if commandOption == "ToolOps_ControlCreator":
            ToolOps_ControlCreator.ToolOps_ControlCreator()
        if commandOption == "SkinOps_Painter":
            Tool_SkinPainter.SkinOps_Painter()


# myWindow = ToolOps_Menu()
