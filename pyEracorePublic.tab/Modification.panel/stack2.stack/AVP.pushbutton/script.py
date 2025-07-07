__title__ = "AVP"
__author__ = "pyEracore"
__doc__ = """
This plugin aligns elements vertically based on a point selected in the model. Each element's center is moved to the closest vertical position relative to the screen, matching the selected point's vertical screen alignment.
"""


from Autodesk.Revit.DB import Transaction, ElementTransformUtils, LocationPoint, LocationCurve, Plane, XYZ, SketchPlane, Element
from Autodesk.Revit.DB.Electrical import Conduit
from pyrevit import revit
import traceback, os, clr

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)
from RevitPluginLib import CustomFunctions, LicenseChecker
from System.Collections.Generic import List


uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application



check = LicenseChecker.CheckLicenseGranted(app)
if check:

    t = Transaction(doc, __title__)
    t.Start()
    try:

        view = doc.ActiveView
        CustomFunctions.WorkPlaneByScreen(uidoc, app)
        elements = revit.get_selection().elements
        point = revit.pick_point()

        elements_cs = List[Element]()
        for el in elements:
            elements_cs.Add(el)


        CustomFunctions.AlignScreenVertical(uidoc, elements_cs, point, app)


        t.Commit()
    except Exception as e:
        t.RollBack()
        tb_str = traceback.format_exc()
        print("IronPython Traceback:")
        print(tb_str)

