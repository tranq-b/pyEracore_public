__title__ = "Disconnect Selected"
__author__ = "Andrey.B"
__doc__ = """
Disconnects only the currently selected elements from each other without affecting other connections.
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

elements = revit.get_selection()
elements_id = [i.Id for i in elements]

check = LicenseChecker.CheckLicenseGranted(app)
if check:

    res = "DisConnect"
    # Start a transaction
    t = Transaction(doc, __title__)
    t.Start()
    try:
        if res == "Custom Connect":
            fault = float(forms.ask_for_string(
                default='0.0001',
                prompt='Enter fault:',
                title='Fault'
            ))
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
                            CustomFunctions.DisconnectElements(doc, element, other_element, app, 0.0001)

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
