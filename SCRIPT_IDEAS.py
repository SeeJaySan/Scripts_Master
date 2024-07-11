from maya import mel as mel
from maya import cmds as mc
import pymel.core as pm

for item in pm.selected():
    
    getStringToReplace = "tmp"
    
    #item.rename(item.name().replace(getStringToReplace, 'jnt'))
    
    #add prefix
    item.rename("this" + "_" + item.name())
    
    #add suffix
    item.rename(item.name() + "_" + "this")
    

# mel version of 
mel.eval('searchReplaceNames "HummingBird_" "" "selected"')