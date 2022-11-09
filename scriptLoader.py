import sys
import os
import importlib

#module path(s)
path = r'C:\Users\CJ Nowacek\Dropbox\My PC (DESKTOP-7N81176)\Documents\~CJ\[Scripts]\Scripts_Master\live'

for module_name in list(sys.modules.keys()):
    top_module = module_name.split('.')[0]
    print (top_module)
    
    #reloading for modules
    
    if top_module == 'rigOps_createContols':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'ArmOps_IKFKSwitch':
        importlib.reload((sys.modules[module_name]))
        
    if top_module == 'ArmOps_IKFKSwitch':
        importlib.reload((sys.modules[module_name]))
        
    if top_module == 'rigOps_Mirror':
        importlib.reload((sys.modules[module_name]))

    if top_module == 'ToolOps_charaterTemplate':
        importlib.reload((sys.modules[module_name]))
        
# making sure the path is correct so we can import        
if path not in sys.path:
    sys.path.append(path)

# importing modules
import rigOps_createContols
import ArmOps_IKFKSwitch
import rigOps_Mirror
import ToolOps_charaterTemplate

print ('LOADED: ' + str(rigOps_createContols))
print ('LOADED: ' + str(ArmOps_IKFKSwitch))
print ('LOADED: ' + str(rigOps_Mirror))
print ('LOADED: ' + str(ToolOps_charaterTemplate))

print ('\n-------------------------------------------------Tools------------------------------------------------|')
print ('------------------------------------------------------------------------------------------------------|')
print ('\nrigOps_createContols -- rigOps_createContols.rigOps_createContols()\n')
print ('ArmOps_IKFKSwitch -- ArmOps_IKFKSwitch.ArmOps_IKFKSwitch(side="L")\n')
print ('rigOps_Mirror -- rigOps_Mirror.rigOps_Mirror(mirrorbehaviour = True)\n')
print ('ToolOps_charaterTemplate -- ToolOps_charaterTemplate.ToolOps_charaterTemplate(charactername = "template")\n')
print ('------------------------------------------------------------------------------------------------------|')
