import sys
import os
import importlib

#module path(s)
path = r'C:\Users\CJ Nowacek\Dropbox\My PC (DESKTOP-7N81176)\Documents\~CJ\[Scripts]\Scripts_Master\live'

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
    
    if top_module == 'rigOps_createContols':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'ArmOps_IKFKSwitch':
        importlib.reload((sys.modules[module_name]))
        
    if top_module == 'LegOps_IKFKSwitch':
        importlib.reload((sys.modules[module_name]))
        
    if top_module == 'rigOps_Mirror':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'ToolOps_charaterTemplate':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'ToolOps_BatchGeoExporter':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'ToolOps_CharacterExporter':
        importlib.reload((sys.modules[module_name]))

    #if top_module == 'FootOps_ReverseFoot':
        #importlib.reload((sys.modules[module_name]))
        
# making sure the path is correct so we can import        
if path not in sys.path:
    sys.path.append(path)

# importing modules
import rigOps_createContols
import ArmOps_IKFKSwitch
import LegOps_IKFKSwitch
import rigOps_Mirror
import ToolOps_charaterTemplate
import ToolOps_BatchGeoExporter
import ToolOps_CharacterExporter
#import FootOps_ReverseFoot

print ('LOADED: ' + str(rigOps_createContols))
print ('LOADED: ' + str(ArmOps_IKFKSwitch))
print ('LOADED: ' + str(LegOps_IKFKSwitch))
print ('LOADED: ' + str(rigOps_Mirror))
print ('LOADED: ' + str(ToolOps_BatchGeoExporter))
print ('LOADED: ' + str(ToolOps_charaterTemplate))
print ('LOADED: ' + str(ToolOps_CharacterExporter))
#print ('LOADED: ' + str(FootOps_ReverseFoot))

print ('\n-------------------------------------------------Tools------------------------------------------------|')
print ('------------------------------------------------------------------------------------------------------|')
print ('\nrigOps_createContols -- rigOps_createContols.rigOps_createContols()\n')
print ('ArmOps_IKFKSwitch -- ArmOps_IKFKSwitch.ArmOps_IKFKSwitch(side="L")\n')
print ('LegOps_IKFKSwitch -- LegOps_IKFKSwitch.LegOps_IKFKSwitch(side="L")\n')
print ('rigOps_Mirror -- rigOps_Mirror.rigOps_Mirror(mirrorbehaviour = True)\n')
print ('ToolOps_charaterTemplate -- ToolOps_charaterTemplate.ToolOps_charaterTemplate(charactername = "template")\n')
print ('ToolOps_BatchGeoExporter -- ToolOps_BatchGeoExporter.ToolOps_BatchGeoExporter()\n')
print ('FootOps_ReverseFoot -- FootOps_ReverseFoot.FootOps_ReverseFoot(self.side = "L")\n')
print ('ToolOps_CharacterExporter -- ToolOps_CharacterExporter.ToolOps_CharacterExporter()\n')
print ('------------------------------------------------------------------------------------------------------|')
