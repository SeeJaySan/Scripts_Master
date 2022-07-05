import sys
import pprint as pp

#path of the module
path = r'C:\Users\CJ Nowacek\Dropbox\My PC (DESKTOP-7N81176)\Documents\~CJ\Scipts__Maya\arm_utils'

for module_name in sys.modules.keys():
    top_module = module_name.split('.')[0]
    print (top_module)
    
    if top_module == 'arm_utils':
        del(sys.modules[module_name])
        
if path not in sys.path:
    sys.path.append(path)

import arm_utils
print (arm_utils)

arm_utils.build_guides()

arm_utils.build_joints()

arm_utils.build_rig()