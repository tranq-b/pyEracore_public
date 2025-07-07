__title__ = "Split Conduits"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script splits selected conduit elements using a user-defined 3D box, cutting the conduits where they intersect the box.

2. Steps to use:

    - Run the script.
    
    - Draw a rectangle in the view to select conduit elements inside it.
    
    - Define a 3D split box in the model.
    
    - The script will process each selected conduit and split it at the intersection with the box.

3. Result:
All selected conduits that intersect the split box will be divided into separate segments at the intersection points.
"""


from Autodesk.Revit.DB import Transaction
from pyrevit import revit
import traceback
import clr, os


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
        elements = revit.pick_rectangle()
        elements = [i for i in elements if i.Category.Name == "Conduits"]
        box = CustomFunctions.PickSplitBox(uidoc)
        for element in elements:
            CustomFunctions.SplitConduit(doc, element, box, app)

    t.Commit()
except Exception as e:
    t.RollBack()
    tb_str = traceback.format_exc()
    print("IronPython Traceback:")
    print(tb_str)

