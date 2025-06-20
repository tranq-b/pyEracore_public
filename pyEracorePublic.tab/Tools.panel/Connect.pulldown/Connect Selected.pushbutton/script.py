__title__ = "Connect Selected"
__author__ = "Andrey.B"
__doc__ = """
Creates connections exclusively between the currently selected elements.
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


    res = "Connect"

    # Start a transaction
    t = Transaction(doc, __title__)
    t.Start()
    try:

        with forms.ProgressBar(cancellable=True) as pb:
            max_value = len(elements)
            for num, element in enumerate(elements):
                if pb.cancelled:
                    break
                other_elements = CustomFunctions.ElementsNear(doc, element, app, 0.5)
                for other_element in other_elements:
                    if other_element.Id in elements_id:
                        if element.Id == other_element.Id:
                            continue
                        try:
                            if res == "Connect":
                                CustomFunctions.ConnectElements(doc, element, other_element, app, 0.01)
                        except:
                            pass
                    else:
                        pb.update_progress(num, max_value)


        # Commit the transaction
        t.Commit()
    except Exception as e:
        # If an exception occurs, roll back the transaction
        t.RollBack()
        print(e)
