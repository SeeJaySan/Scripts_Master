from maya import cmds as mc
import maya.mel as mel
import subprocess
import os

def main():
    ToolOps_CharaterExporter()

path = r"C:\Dropbox\BFA\Artwork\Character\Robin\RIG"

fileName = "SKL_Robin"


def ToolOps_CharaterExporter():
    exportList = []
    mc.select("GEO")
    this = mc.listRelatives(c=True)
    mc.select(this)
    geo = mc.ls(sl=1)

    for each in geo:
        exportList.append(each)

    exportList.append("Root")

    for each in exportList:
        mc.parent(each, w=1)

    # pop the skeleton out of the selection. We only need the geo. The skeleton comes with it
    exportList.pop(-1)

    # select the nodes need to export the fbx
    mc.select(exportList)

    mel.eval("FBXExportBakeComplexAnimation -v 1")

    # exporting
    mc.file(
        "{}{}{}{}".format(path, "\\", fileName, ".fbx"),
        f=True,
        options="v=0;",
        typ="FBX export",
        pr=True,
        es=True,
    )

    # reparentingobject back to where they belong
    # a = list(map(lambda i : mc.parent(i, 'GEO') if i.startswith('SKL')\
    # else (mc.parent(i, 'SKL') if i.startswith('Root') else None), exportList))

    # we can't view the model in windows 3d viewer. Mother fucker breaks but for some reason in works when I import it back into maya and unreal
    # subprocess.run(['explorer', os.path.realpath('{}{}{}{}'.format(path, '\\', fileName, '.fbx'))])
