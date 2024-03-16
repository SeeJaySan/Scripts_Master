import sys
import importlib

#path of the module
path = r'C:\Users\cjnowacek\Desktop\important files\scripts\myScript\live'

for module_name in list(sys.modules.keys()):
    top_module = module_name.split('.')[0]
    print (top_module)
    
    #deletes the module for reload but causes an error becuase the dictorary changes size
    if top_module == 'scriptLoader':
        importlib.reload(sys.modules[module_name])
        
if path not in sys.path:
    sys.path.append(path)

import scriptLoader
print (scriptLoader)

if __name__ == '__main__':

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass
    
    test_dialog = scriptLoader.ToolOps_Menu()
    #test_dialog.show()