import sys
import importlib

#path of the module
path = r'C:\Users\CJ Nowacek\Dropbox\My PC (DESKTOP-7N81176)\Documents\~CJ\Scipts__Maya\Git\rigging'

for module_name in sys.modules.keys():
    top_module = module_name.split('.')[0]
    print (top_module)
    
    if top_module == 'cn_reverse_foot':
        importlib.reload((sys.modules[module_name]))
        
if path not in sys.path:
    sys.path.append(path)

import cn_reverse_foot
print (cn_reverse_foot)

auto_rig = cn_reverse_foot.ReverseFootUI()

if __name__ == '__main__':

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass
    
    test_dialog = cn_reverse_foot.ReverseFootUI()
    test_dialog.show()