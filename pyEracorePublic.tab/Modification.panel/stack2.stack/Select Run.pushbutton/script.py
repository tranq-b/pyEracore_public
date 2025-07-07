__title__ = "Select Run"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script highlights and selects the entire conduit run starting from the selected conduits or bends (elbows). It processes conduits and conduit fittings that are identified as part of bends.

2. Steps to use:

    - Select one or more conduits or elbows in the model.
    
    - Run the script.
    
    - The script will automatically find and select the full connected conduit run.

3. Result:
The entire conduit run connected to the selected elements will be highlighted and selected, making it easy to review or manipulate the full pathway.
"""

from Autodesk.Revit.DB import ElementId, Transaction, Element
from System.Collections.Generic import List
from pyrevit import revit
import traceback, os, clr

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)
from RevitPluginLib import CustomFunctions, LicenseChecker

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


check = LicenseChecker.CheckLicenseGranted(app)
if check:
    t = Transaction(doc, __title__)
    t.Start()
    try:
        elements = revit.get_selection().elements

        elements_cs = List[Element]()
        for el in elements:
            if el.Category.Name == "Conduits":
                elements_cs.Add(el)
            elif el.Category.Name == "Conduit Fittings":
                name = el.Name
                family = el.Symbol.Family.Name
                if (
                        "elbow" in name.lower() or
                        "bend" in name.lower() or
                        "elbow" in family.lower() or
                        "bend" in family.lower()
                ):
                    elements_cs.Add(el)

        CustomFunctions.SelectRun(uidoc, doc, elements_cs, app)

        t.Commit()
    except Exception:
        t.RollBack()
        print("IronPython Traceback:")
        print(traceback.format_exc())
