__title__ = "Unhide Selected"
__author__ = "Andrey.B"
__doc__ = """
SAMPLE TEXT
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





