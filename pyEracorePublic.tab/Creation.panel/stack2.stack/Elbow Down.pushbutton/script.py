__title__ = "Elbow Down"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script creates a vertical conduit segment with an elbow going downward from the end of each selected conduit that is closest to the picked point.

2. Steps to use:

    - Select one or more conduits in the model.
    
    - Run the script.
    
    - Pick a point in the model where you want the conduits to elbow down.

3. Result:
The script will add a vertical segment at the nearest end of each selected conduit, creating an elbow that bends downward toward the picked point.
"""

import clr, os, traceback
from pyrevit import revit
from Autodesk.Revit.DB import Transaction

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application


t = Transaction(doc, __title__)
t.Start()
try:

    check = LicenseChecker.CheckLicenseGranted(app)
    if check:
        elements = revit.get_selection().elements
        point = revit.pick_elementpoint(world=True)

        for element in elements:
            CustomFunctions.ElbowDown(element, point, doc, app)


    t.Commit()
except Exception as e:
    t.RollBack()
    tb_str = traceback.format_exc()
    print("IronPython Traceback:")
    print(tb_str)