import sys
import importlib

#path of the module
path = r'C:\Dropbox\Scripts\Scripts_Master\other\cn_rigging_scripts'

for module_name in sys.modules.keys():
    top_module = module_name.split('.')[0]
    print (top_module)
    
    if top_module == 'cn_autoRig':
        importlib.reload((sys.modules[module_name]))
        
if path not in sys.path:
    sys.path.append(path)

import cn_autoRig
print (cn_autoRig)

auto_rig = cn_autoRig.TwoBoneIKFKUI()

if __name__ == '__main__':

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass
    
    test_dialog = cn_autoRig.TwoBoneIKFKUI()
    test_dialog.show()