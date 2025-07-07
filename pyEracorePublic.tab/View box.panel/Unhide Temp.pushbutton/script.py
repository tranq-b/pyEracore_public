__title__ = "Unhide Selected"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script resets the temporary hide/isolate mode in the active view and then temporarily isolates the selected elements together with all other currently visible elements. It is useful for quickly refocusing on your selected elements without losing the context of the existing view state.

2. Steps to use:

    - Select elements in the active view that you want to emphasize.
    
    - Run the script.
    
    - The script will first disable any existing temporary hide/isolate mode and then isolate your selection plus all currently visible elements.

3. Result:
The view will switch to a temporary isolate mode showing only your selected elements and everything that was already visible, helping you focus on these elements while hiding others.
"""

from pyrevit import revit
import os, clr
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, ElementId, TemporaryViewMode
from System.Collections.Generic import List

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)
from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

check = LicenseChecker.CheckLicenseGranted(app)
if check:

    active_view = doc.ActiveView
    elements = revit.get_selection()
    elements = [i for i in elements]
    elements_old = FilteredElementCollector(doc, doc.ActiveView.Id).WhereElementIsNotElementType().ToElements()
    elements_old = [i for i in elements_old]
    elements1 = elements + elements_old

    # Start a transaction
    tran = Transaction(doc, 'Unhide Temp')
    tran.Start()
    try:

        active_view.DisableTemporaryViewMode(TemporaryViewMode.TemporaryHideIsolate)
        element_ids = List[ElementId]([i.Id for i in elements1])
        active_view.IsolateElementsTemporary(element_ids)
        # Commit the transaction
        tran.Commit()

    except Exception as e:
        # If an exception occurs, roll back the transaction
        tran.RollBack()
        print(e)





