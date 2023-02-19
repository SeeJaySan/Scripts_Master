import maya.cmds as mc

SKLsel = []
GEOsel = []
FINALsel = []

# namespace check

defaults = ['UI', 'shared']
if mc.namespaceInfo(lon=True) != defaults:
    namespaces = (ns for ns in mc.namespaceInfo(lon=True) if ns not in defaults)
    mc.namespace(removeNamespace = ns, mergeNamespaceWithParent = True)

# 

a = mc.select('SKL_lyr')
SKLsel = mc.listConnections('SKL_lyr')
SKLsel.pop(0)
print ('SKL : ' + str(SKLsel))


a = mc.select('GEO_lyr')

GEOsel = mc.listConnections('GEO_lyr')
GEOsel.pop(0)
print ('GEO : ' + str(GEOsel))

for i in range(len(GEOsel)):
    
    FINALsel.append(GEOsel[i])
    
for i in range(len(SKLsel)):
    
    FINALsel.append(SKLsel[i])


print ('complete selection : ' + str(FINALsel))
mc.select(FINALsel[:])