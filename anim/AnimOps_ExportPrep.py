import maya.cmds as mc
import maya.mel as mel


def main():
    AnimOps_ExportPrep()


class AnimOps_ExportPrep(object):

    SKLsel = []
    GEOsel = []
    FINALsel = []

    # namespace check

    defaults = ['UI', 'shared']
    namespaces = mc.namespaceInfo(lon=True)[0]
    if mc.namespaceInfo(lon=True) != defaults:
        mc.namespace(removeNamespace = mc.namespaceInfo(lon=True)[0], mergeNamespaceWithParent = True)

    # selecting SKL_lyr and GEO_lyr

    a = mc.select('SKL_lyr')
    SKLsel = mc.listConnections('SKL_lyr')
    SKLsel.pop(0)
    print ('SKL : ' + str(SKLsel))


    a = mc.select('GEO_lyr')

    GEOsel = mc.listConnections('GEO_lyr')
    GEOsel.pop(0)
    print ('GEO : ' + str(GEOsel))

    # compiling lists to make on selection

    for i in range(len(GEOsel)):
        
        FINALsel.append(GEOsel[i])
        
    for i in range(len(SKLsel)):
        
        FINALsel.append(SKLsel[i])

    # final selection
    print ('complete selection : ' + str(FINALsel))
    mc.select(FINALsel[:])