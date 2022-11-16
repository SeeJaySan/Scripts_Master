__author__ = "CJ Nowacek"
__credits__ = "CJ Nowacek"
__license__ = "GPL"
__version__ = "1.0.2"
__maintainer__ = "CJ Nowacek"
__email__ = "cj.nowacek@gmail.com"
__status__ = "Production"

import maya.cmds as mc
import os

#TODO add different export types
#TODO add options for animation?

class ToolOps_BatchGeoExporter(object):
        
    #constructor
    def __init__(self):
            
        self.window = "ToolOps_BatchGeoExporter"
        self.title = "Mesh Exporter"
        self.size = (400, 120)
            
        # close old window is open
        if mc.window(self.window, exists = True):
            mc.deleteUI(self.window, window=True)
            
        #create new window
        self.window = mc.window(self.window, title=self.title)
        
        mc.columnLayout(adjustableColumn = True)
        
        mc.text(self.title)
        mc.separator(height = 20)
            
        self.options_menu = mc.optionMenu('this', label='Export Type')
        mc.menuItem( label='obj', parent = self.options_menu )
        mc.menuItem( label='fbx', parent = self.options_menu )
        mc.menuItem( label='stl', parent = self.options_menu )

        self.name = mc.textFieldGrp(label = 'path:')
        self.export_bn = mc.button( label='Export', command=self.exportStuff)
        mc.setParent( '..' )

        

        #display new window
        mc.showWindow()
    
    def exportStuff(self, *args):
        sel = mc.ls(sl=1)
        
        typeOption = ''
        

        # getting input path
        path = mc.textFieldGrp(self.name, q = True, text=True)
        if path == '':
            mc.error('Please input a path')
        correctedPath = str(path.replace('"', ''))

        # getting file type and options
        exportType =  str(mc.optionMenu(self.options_menu, q = True, value = True))

        objOptions = "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1"
        fbxOptions = "v=0;"
        stlOptions = "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1"

        if 'obj' in exportType:
            typeOption = "OBJexport"
            options = objOptions
        elif 'stl' in exportType:
            typeOption = "STLexport"
            options = stlOptions
            exportType = exportType
        elif 'fbx' in exportType:
            typeOption = "FBX EXPORT"
            options = fbxOptions
        else:
            mc.error('Please select geometry')
        
        # run through list of objects
        for i in sel:
            
            # get objects from list
            mc.select(i)
            
            #checking if there is a parent
            parentNode = mc.listRelatives(p = True)
            hasParent = bool(mc.listRelatives(i, parent=True))
            if hasParent:
                mc.parent(i, world = True)
            
            
            #exporting
            mc.file('{}{}{}{}'.format(correctedPath, '\\', i, '.' + exportType), f = True, options = options, typ = typeOption, pr = True, es = True)
            if exportType == 'stl':

                mc.confirmDialog(t='STL Warning', m="stl export doesn't name files correctly. Add the .stl suffix to stl file exports", db='ok')
            
            # reparenting
            if hasParent:
                mc.parent(i, parentNode)
                                   
myWindow = ToolOps_BatchGeoExporter()