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

class ToolOps_BatchGeoExporter(object):
        
    #constructor
    def __init__(self):
            
        self.window = "ToolOps_BatchGeoExporter"
        self.title = "Mesh Exporter"
        self.size = (400, 80)
            
        # close old window is open
        if mc.window(self.window, exists = True):
            mc.deleteUI(self.window, window=True)
            
        #create new window
        self.window = mc.window(self.window, title=self.title, widthHeight=(self.size))
        
        mc.columnLayout(adjustableColumn = True)
        
        mc.text(self.title)
        mc.separator(height = 20)
        
        self.name = mc.textFieldGrp(label = 'path:')
        self.export_bn = mc.button( label='Export', command=self.exportStuff)
        mc.setParent( '..' )

        #display new window
        mc.showWindow()
    
    def exportStuff(self, *args):
        sel = mc.ls(sl=1)
        
        
        # getting input path
        path = mc.textFieldGrp(self.name, q = True, text=True)
        newpath = str(path.replace('"', ''))
        
        
        for i in sel:
            
            # get objects from list
            mc.select(i)
            
            #checking if there is a parent
            parentNode = mc.listRelatives(p = True)
            hasParent = bool(mc.listRelatives(i, parent=True))
            if hasParent:
                mc.parent(i, world = True)
            
            #exporting
            mc.file('{}{}{}{}'.format(newpath, '\\', i, '.fbx'), f = True, options = 'v=0;', typ = "FBX export", pr = True, es = True)
            
            # reparenting
            if hasParent:
                mc.parent(i, parentNode)
                                   
#myWindow = ToolOps_BatchGeoExporter()