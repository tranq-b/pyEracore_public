__title__ = "Select Run"
__author__ = "MyPy"
__doc__ = """
SAMPLE TEXT
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
            elements_cs.Add(el)

        CustomFunctions.SelectRun(uidoc, doc, elements_cs, app)

        t.Commit()
    except Exception:
        t.RollBack()
        print("IronPython Traceback:")
        print(traceback.format_exc())
