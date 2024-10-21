import os
import sys
import importlib

# Define the path to the module directory
module_path = r"C:\Scripts_Master"

# Check and reload the 'ToolsetMaster' module if it exists in sys.modules
for module_name in list(sys.modules.keys()):
    top_module = module_name.split(".")[0]

    if top_module == "ToolsetMaster":
        importlib.reload(sys.modules[module_name])
        break

# Add the module path to sys.path if not already present
if module_path not in sys.path:
    sys.path.append(module_path)

# Import the ToolsetMaster module
import ToolsetMaster

if __name__ == "__main__":
    # Attempt to close any existing instance of TM_TabWindow
    try:
        TM.close()
        TM.deleteLater()
    except NameError:
        pass  # Ignore if TM is not defined

    # Initialize and display the TM_TabWindow
    TM = ToolsetMaster.TM_TabWindow()
    TM.show()