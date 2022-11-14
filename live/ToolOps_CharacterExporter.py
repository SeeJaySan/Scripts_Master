__author__ = "CJ Nowacek"
__credits__ = "CJ Nowacek"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "CJ Nowacek"
__email__ = "cj.nowacek@gmail.com"
__status__ = "Production"

import maya.cmds as mc

#TODO add different export types
#TODO add options for animation?

class ToolOps_CharacterExporter(object):
        
    #constructor
    def __init__(self):
            
        self.window = "ToolOps_CharacterExporter"
        self.title = "Character Exporter"
        self.size = (400, 80)
            
        # close old window is open
        if mc.window(self.window, exists = True):
            mc.deleteUI(self.window, window=True)
            
        #create new window
        self.window = mc.window(self.window, title=self.title, widthHeight=(self.size))
        
        mc.columnLayout(adjustableColumn = True)
        
        mc.text(self.title)
        mc.separator(height = 20)
        
        self.export_bn = mc.button( label='Export', command=self.fbxExporter)
    
    def fbxExporter():
        exportList = []

        mc.select('GEO')

        mc.select('GEO')
        this = mc.listRelatives(c = True)
        mc.select(this)
        geo = mc.ls(sl = 1)

        for each in geo:
            exportList.append(each)

        exportList.append('Root')

        for each in exportList:
            mc.parent(each, w = 1)

        #for i, 'SKL_' in exportList:
        #    mc.parent(i, 'GEO')

        #map(lambda i:if 'SKL' in exportList: mc.parent(i, 'GEO'), exportList)

        #map(lambda i:if i.startswith('SKL') print(i), exportList)

        a = list(map(lambda i : mc.parent(i, 'GEO') if i.startswith('SKL')\
        else (mc.parent(i, 'SKL') if i.startswith('Root') else None), exportList))
        
myWindow = ToolOps_CharacterExporter()