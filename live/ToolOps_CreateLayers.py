import maya.cmds as mc

sklname = 'SKL_lyr'
geoname = 'GEO_lyr'
bnJoints = []
geo = []

jointsel = mc.ls(type='joint')
geosel = mc.ls(type='mesh')

for i in jointsel:
    if 'BN_JNT' in i:
        bnJoints.append(i)
        
for i in geosel:
    if 'SKL_' in i:
        geo.append(i)
        
print(bnJoints)

lyrs = mc.ls(type = 'displayLayer')

mc.select(bnJoints)
if sklname in lyrs:
    mc.editDisplayLayerMembers(sklname, bnJoints[:], nr = True)
else:
    mc.createDisplayLayer (n = sklname, num = 1, e = True)
    mc.editDisplayLayerMembers(sklname, bnJoints[:], nr = True)
    
mc.select(geo)
if geoname in lyrs:
    mc.editDisplayLayerMembers(geoname, geo[:], nr = True)
else:
    mc.createDisplayLayer (n = geoname, num = 1, e = True)
    mc.editDisplayLayerMembers(geoname, geo[:], nr = True)

mc.layerButton(sklname, ls = 'template')
mc.layerButton(geoname, ls = 'reference')