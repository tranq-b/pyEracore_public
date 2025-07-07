__title__ = "Disconnect Selected"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script disconnects all connections between the selected elements if they are within 0.5 ft of each other, effectively isolating them in the model.

2. Steps to use:

    - Select multiple elements in the model that you want to disconnect from each other.
    
    - Run the script.
    
    - The script will check for close connections among the selected elements and break them.

3. Result:
All selected elements will be disconnected from one another if they were previously joined within a 0.5 ft distance, leaving them individually isolated.
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
