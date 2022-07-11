import sys
import importlib

#path of the module
path = r'C:\Users\CJ Nowacek\Dropbox\My PC (DESKTOP-7N81176)\Documents\~CJ\Scipts__Maya\Git\rigging'

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


auto_rig.rig.build_guides()

auto_rig.rig.build_joints()

auto_rig.rig.build_rig()