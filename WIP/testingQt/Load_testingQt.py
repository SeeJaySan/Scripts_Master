"""
File: LOAD_cn_autoRig.py
Author: CJ Nowacek
Date: 2024-03-20
Description: file for testing new qt dialogues
"""

import sys
import importlib

# path of the module
path = r"C:\Users\cjnowacek\Desktop\important files\scripts\myScript\testingQt"


# Reload system modules keys
for module_name in sys.modules.keys():
    top_module = module_name.split(".")[0]
    print(top_module)

    # force reload if module is already loaded
    if top_module == "testingQt":
        sys.modules.pop(module_name)


if path not in sys.path:
    sys.path.append(path)

# reimport autoRigQWidget
import testingQt

if __name__ == "__main__":

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass

    test_dialog = testingQt.TabWidgetDialog()
    test_dialog.show()
