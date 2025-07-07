__title__ = "Multi-Trim"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script trims multiple selected conduits so they intersect or meet cleanly, similar to a trim operation in CAD.

2. Steps to use:

    - Select at least two conduit elements in the model.
    
    - Run the script.
    
    - The script will automatically trim the selected conduits where they intersect.

3. Result:
The selected conduits will be trimmed to intersect or align precisely at their nearest points, cleaning up overlapping geometry.
"""

from Autodesk.Revit.DB import Transaction
from pyrevit import revit
import traceback
import clr, os


dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bin", "RevitPluginLib.dll"))
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

        if len(elements) >= 2:
            CustomFunctions.TrimConduits(doc, elements, app)




    t.Commit()
except Exception as e:
    t.RollBack()
    tb_str = traceback.format_exc()
    print("IronPython Traceback:")
    print(tb_str)

