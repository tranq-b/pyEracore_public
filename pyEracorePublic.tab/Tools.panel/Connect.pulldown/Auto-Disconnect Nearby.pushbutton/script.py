__title__ = "Auto-Disconnect Nearby"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script disconnects all immediate connections from the selected elements. It finds directly connected elements via connectors and breaks those links.

2. Steps to use:

    - Select the elements (such as conduits) you want to disconnect from their connected runs.
    
    - Run the script.
    
    - The script will process each selected element and disconnect it from adjacent connected elements.

3. Result:
The selected elements will no longer be connected to their neighboring elements, effectively isolating them in the model.
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
