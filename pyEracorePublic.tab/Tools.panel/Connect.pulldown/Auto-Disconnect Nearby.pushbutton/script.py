__title__ = "Auto-Disconnect Nearby"
__author__ = "Andrey.B"
__doc__ = """
Detaches all elements connected to the currently selected elements, leaving only the selected elements connected.
"""



import os, clr, traceback
from Autodesk.Revit.DB import Transaction, Element
from pyrevit import revit, forms
from System.Collections.Generic import List

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)
from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

check = LicenseChecker.CheckLicenseGranted(app)
if check:

    elements = revit.get_selection()
    elements_id = [i.Id for i in elements]


    res = "DisConnect"
    fault = 0.0001

    # Start a transaction
    t = Transaction(doc, __title__)
    t.Start()
    try:
        with forms.ProgressBar(cancellable=True) as pb:
            max_value = len(elements)
            for num, element in enumerate(elements):
                if pb.cancelled:
                    break
                if res == "DisConnect":
                    next_elements = CustomFunctions.NextElementsConnector(element, app)
                    for next in next_elements:
                        CustomFunctions.DisconnectElements(doc, element, next, app, fault)
            else:
                pb.update_progress(num, max_value)


        # Commit the transaction
        t.Commit()
    except Exception as e:
        # If an exception occurs, roll back the transaction
        t.RollBack()
        print(e)
