import sys

#path of the module
path = r'C:\Users\CJ Nowacek\Dropbox\My PC (DESKTOP-7N81176)\Documents\~CJ\Scipts__Maya\jaw_utils'

for module_name in sys.modules.keys():
    top_module = module_name.split('.')[0]
    print (top_module)
    
    if top_module == 'jaw_utils':
        del(sys.modules[module_name])
        
if path not in sys.path:
    sys.path.append(path)
    
import jaw_utils
print (jaw_utils)

jaw_utils.createGuides()
jaw_utils.lip_guides()
jaw_utils.jaw_guides()

jaw_utils.build()
jaw_utils.getLipParts()
print(lookup)
