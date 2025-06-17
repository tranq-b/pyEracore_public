__title__ = "Align By Bottom"

from Autodesk.Revit.DB import Transaction, ElementId, Element
from pyrevit import revit
import traceback, os, clr
from System.Collections.Generic import List

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)
from RevitPluginLib import CustomFunctions, LicenseChecker

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


check = LicenseChecker.CheckLicenseGranted(app)
if check:

    try:
        elements = revit.get_selection()
        trueElement = revit.pick_element_by_category("Conduits")
        parameters = trueElement.Parameters
        for parameter in parameters:
            if "Bottom Elevation" in parameter.Definition.Name:
                parameter_name = parameter.Definition.Name
                BOC = parameter.AsDouble()

        level = trueElement.ReferenceLevel




        # Start a transaction
        t = Transaction(doc, __title__)
        t.Start()
        try:
            for i in elements:
                par = Element.LookupParameter(i, parameter_name)
                i.ReferenceLevel = level
                par.Set(BOC)
            # Commit the transaction
            t.Commit()

            t.Commit()

        except Exception as e:
            t.RollBack()
            tb_str = traceback.format_exc()
            print("IronPython Traceback:")
            print(tb_str)
    except:
        pass
