"""
File: ToolsetMasterLoader.py
Author: CJ Nowacek
Date: 2024-03-17
Description: Loads ToolsetMaster
"""

import sys
import importlib

# path of the module
path = r"C:\Users\cjnowacek\Desktop\important files\scripts\myScript"


# Reload system modules keys
for module_name in sys.modules.keys():
    top_module = module_name.split(".")[0]
    print(top_module)
# else:
    # force reload if module is already loaded
    if top_module == "ToolsetMaster":
        sys.modules.pop(module_name)


if path not in sys.path:
    sys.path.append(path)

# reimport autoRigQWidget
import ToolsetMaster

if __name__ == "__main__":

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass

    test_dialog = ToolsetMaster.TabWidgetDialog()
    test_dialog.show()
