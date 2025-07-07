__title__ = "Auto-Connect Nearby"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script automatically connects selected elements (typically conduits) to nearby elements within a 0.5 ft range, creating connections wherever possible.

2. Steps to use:

    - Select the elements in the model that you want to auto-connect.
    
    - Run the script.
    
    - The script will loop through each selected element and attempt to connect it to any nearby elements.

3. Result:
All selected elements will be connected to adjacent elements within a 0.5 ft distance, improving model continuity by automatically creating join connections.
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
                else:
                    pb.update_progress(num, max_value)
                other_elements = CustomFunctions.ElementsNear(doc, element, app, 0.5)
                for other_element in other_elements:
                    if element.Id == other_element.Id:
                        continue
                    try:
                        if res == "Connect":
                            CustomFunctions.ConnectElements(doc, element, other_element, app, 0.01)

                    except:
                        pass



        # Commit the transaction
        t.Commit()
    except Exception as e:
        t.RollBack()
        tb_str = traceback.format_exc()
        print("IronPython Traceback:")
        print(tb_str)