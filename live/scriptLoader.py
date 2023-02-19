import sys
import os
import importlib
import maya.cmds as mc

#module path(s)
path = r'C:\Dropbox\Scripts\Scripts_Master\live'

# TODO write a custom path widow if the path isn't found

if path == bool(os.path.exists(path)):
    pass
else:
    # TODO write a custom path widow if the path isn't found -- get the code from the geoExporter
    pass

for module_name in list(sys.modules.keys()):
    top_module = module_name.split('.')[0]
    print (top_module)
    
    #reloading for modules
    
    if top_module == 'BfaOps_AnimExportPrep':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'BfaOps_AnimExporter':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'RigOps_CreateContols':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'RigOp_ArmIKFKSwitch':
        importlib.reload((sys.modules[module_name]))
        
    if top_module == 'RigOp_LegIKFKSwitch':
        importlib.reload((sys.modules[module_name]))
         
    if top_module == 'RigOps_MirrorJnts':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'ToolOps_CharaterTemplate':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'ToolOps_BatchGeoExporter':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'ToolOps_CharacterExporter':
        importlib.reload((sys.modules[module_name]))
        
    if top_module == 'ToolOps_ControlCreator':
        importlib.reload((sys.modules[module_name]))


    if top_module == 'FootOps_ReverseFoot':
        importlib.reload((sys.modules[module_name]))
        
# making sure the path is correct so we can import        
if path not in sys.path:
    sys.path.append(path)

# importing modules
import BfaOps_AnimExportPrep
import BfaOps_AnimExporter
import RigOps_CreateContols
import RigOp_ArmIKFKSwitch
import RigOp_LegIKFKSwitch
import RigOps_MirrorJnts
import ToolOps_CharaterTemplate
import ToolOps_BatchGeoExporter
import ToolOps_CharacterExporter
import ToolOps_ControlCreator
#import FootOps_ReverseFoot
class ToolOps_Menu(object):
        
    #constructor
    def __init__(self):
            
        self.window = "ToolOps_Menu"
        self.title = "Tools Menu"
        self.size = (400, 120)
            
        # close old window is open
        if mc.window(self.window, exists = True):
            mc.deleteUI(self.window, window=True)
            
        #create new window
        self.window = mc.window(self.window, title=self.title)
        
        mc.columnLayout(adjustableColumn = True)
        
        mc.text(self.title)
        mc.separator(height = 20)
            
        self.options_menu = mc.optionMenu('this', label='Ops')
        mc.menuItem( label='__________BfaOps____________', enable=False)
        #mc.menuItem( label='BfaOps_AnimExportPrep', parent = self.options_menu )
        mc.menuItem( label='BfaOps_AnimExporter', parent = self.options_menu )
        mc.menuItem( label='__________RigOps____________')
        mc.menuItem( label='RigOps_CreateContols', parent = self.options_menu )
        mc.menuItem( label='RigOp_ArmIKFKSwitch', parent = self.options_menu )
        mc.menuItem( label='RigOp_LegIKFKSwitch', parent = self.options_menu )
        mc.menuItem( label='RigOps_MirrorJnts', parent = self.options_menu )
        mc.menuItem( label='__________ToolOps____________')
        mc.menuItem( label='ToolOps_CharaterTemplate', parent = self.options_menu )
        mc.menuItem( label='ToolOps_BatchGeoExporter', parent = self.options_menu )
        mc.menuItem( label='FootOps_ReverseFoot', parent = self.options_menu )
        mc.menuItem( label='ToolOps_CharacterExporter', parent = self.options_menu )
        mc.menuItem( label='ToolOps_ControlCreator', parent = self.options_menu )
        
        self.Execute_bn = mc.button( label='Execute', command=self.Execute)
        mc.setParent( '..' )

        #display new window
        mc.showWindow()
    
    def Execute(self, *args):

        # getting file type and options
        commandOption =  str(mc.optionMenu(self.options_menu, q = True, value = True))
        
        if commandOption == 'BfaOps_AnimExportPrep':
            BfaOps_AnimExportPrep.BfaOps_AnimExportPrep()
        if commandOption == 'BfaOps_AnimExporter':
            BfaOps_AnimExporter.BfaOps_AnimExporter()
        if commandOption == 'RigOps_CreateContols':
            RigOps_CreateContols.RigOps_CreateContols()
        if commandOption == 'RigOp_ArmIKFKSwitch':
            RigOp_ArmIKFKSwitch.RigOp_ArmIKFKSwitch()
        if commandOption == 'RigOp_LegIKFKSwitch':
            RigOp_LegIKFKSwitch.RigOp_LegIKFKSwitch()
        if commandOption == 'RigOps_MirrorJnts':
            RigOps_MirrorJnts.RigOps_MirrorJnts()
        if commandOption == 'ToolOps_CharaterTemplate':
            ToolOps_CharaterTemplate.ToolOps_CharaterTemplate()
        if commandOption == 'ToolOps_BatchGeoExporter':
            ToolOps_BatchGeoExporter.ToolOps_BatchGeoExporter()
        #if commandOption == 'FootOps_ReverseFoot':
            #FootOps_ReverseFoot.FootOps_ReverseFoot()
        if commandOption == 'ToolOps_CharacterExporter':
            ToolOps_CharacterExporter.ToolOps_CharacterExporter()
        if commandOption == 'ToolOps_ControlCreator':
            ToolOps_ControlCreator.ToolOps_ControlCreator()
            
myWindow = ToolOps_Menu()

'''
print ('LOADED: ' + str(BfaOps_AnimExportPrep))
print ('LOADED: ' + str(BfaOps_AnimExporter))
print ('LOADED: ' + str(RigOps_CreateContols))
print ('LOADED: ' + str(RigOp_ArmIKFKSwitch))
print ('LOADED: ' + str(RigOp_LegIKFKSwitch))
print ('LOADED: ' + str(RigOps_MirrorJnts))
print ('LOADED: ' + str(ToolOps_BatchGeoExporter))
print ('LOADED: ' + str(ToolOps_CharaterTemplate))
print ('LOADED: ' + str(ToolOps_CharacterExporter))
print ('LOADED: ' + str(ToolOps_ControlCreator))
#print ('LOADED: ' + str(FootOps_ReverseFoot))


print ('\n[BfaOps]')
print ('---------------------------------------------------------------------------------------------------------------------|')
print ('BfaOps_AnimExportPrep -- BfaOps_AnimExportPrep.BfaOps_AnimExportPrep()\n')
print ('BfaOps_AnimExportPrep -- BfaOps_AnimExportPrep.BfaOps_AnimExporter()\n')

print ('\n[RigOps]')
print ('---------------------------------------------------------------------------------------------------------------------|')
print ('RigOps_CreateContols -- RigOps_CreateContols.RigOps_CreateContols()\n')
print ('RigOp_ArmIKFKSwitch -- RigOp_ArmIKFKSwitch.RigOp_ArmIKFKSwitch(side="L")\n')
print ('RigOp_LegIKFKSwitch -- RigOp_LegIKFKSwitch.RigOp_LegIKFKSwitch(side="L")\n')
print ('RigOps_MirrorJnts -- RigOps_MirrorJnts.RigOps_MirrorJnts(mirrorbehaviour = True)')

print ('\n[ToolOps]')
print ('---------------------------------------------------------------------------------------------------------------------|')
print ('ToolOps_CharaterTemplate -- ToolOps_CharaterTemplate.ToolOps_CharaterTemplate(charactername = "template")\n')
print ('ToolOps_BatchGeoExporter -- ToolOps_BatchGeoExporter.ToolOps_BatchGeoExporter()\n')
print ('FootOps_ReverseFoot -- FootOps_ReverseFoot.FootOps_ReverseFoot(self.side = "L")\n')
print ('ToolOps_CharacterExporter -- ToolOps_CharacterExporter.ToolOps_CharacterExporter()\n')
print ('ToolOps_ControlCreator -- ToolOps_ControlCreator.ToolOps_ControlCreator()\n')
print ('---------------------------------------------------------------------------------------------------------------------|')
'''