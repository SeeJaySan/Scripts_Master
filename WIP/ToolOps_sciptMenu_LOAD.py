import sys
import importlib

#path of the module
path = r'C:\Users\CJ Nowacek\Dropbox\My PC (DESKTOP-7N81176)\Documents\~CJ\Maya\Scripts\WIP'

for module_name in list(sys.modules.keys()):
    top_module = module_name.split('.')[0]
    print (top_module)
    
    if top_module == 'ToolOps_scriptMenu':
        importlib.reload((sys.modules[module_name]))
        
if path not in sys.path:
    sys.path.append(path)

import ToolOps_scriptMenu
print (ToolOps_scriptMenu)

auto_rig = ToolOps_scriptMenu.ToolOps_scriptMenuUI()

if __name__ == '__main__':

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass
    
    test_dialog = ToolOps_scriptMenu.ToolOps_scriptMenuUI()
    test_dialog.show()