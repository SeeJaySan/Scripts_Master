
from maya import cmds as mc
from maya import mel as mel

# create sphere

def main(*args):
    MeshOps_createSphere(*args)


class MeshOps_createSphere(object):
    mel.eval('polySphere -r 1 -sx 20 -sy 20 -ax 0 1 0 -cuv 2 -ch 1;')