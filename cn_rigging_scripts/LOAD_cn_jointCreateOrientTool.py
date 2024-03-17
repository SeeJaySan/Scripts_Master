"""
File: LOAD_cn_autoRig.py
Author: CJ Nowacek
Date: 2024-03-20
Description: Reload cn_autoRig.py and run
"""

import sys
import importlib

# path of the module
path = r'C:\Users\cjnowacek\Desktop\important files\scripts\myScript\cn_rigging_scripts'


# Reload system modules keys
for module_name in sys.modules.keys():
    top_module = module_name.split('.')[0]
    print(top_module)

    # force reload if module is already loaded
    if top_module == 'cn_jointCreateOrientTool':
        sys.modules.pop(module_name)


if path not in sys.path:
    sys.path.append(path)

# reimport autoRigQWidget
import cn_jointCreateOrientTool 

if __name__ == '__main__':

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass

    test_dialog = cn_jointCreateOrientTool.TabWidgetDialog()
    test_dialog.show()
