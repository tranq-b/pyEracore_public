__title__ = "Restore Override"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script clears all graphic overrides in the active view for the selected elements. If no elements are selected, it will clear overrides for all elements in the current view.

2. Steps to use:

    - Optionally select elements in the active view.
    
    - Run the script.
    
    - If nothing is selected, the script will target all elements in the view.

3. Result:
All graphic overrides (colors, line styles, transparency, etc.) on the targeted elements will be removed in the active view, restoring them to their default appearance.
"""

from pyrevit import revit
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, OverrideGraphicSettings
import os, clr

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

from RevitPluginLib import CustomFunctions, LicenseChecker

check = LicenseChecker.CheckLicenseGranted(app)
if check:


    elements = revit.get_selection()
    if not elements:
        elements = FilteredElementCollector(doc, doc.ActiveView.Id)

    overrides = OverrideGraphicSettings()

    t = Transaction(doc, __title__)
    t.Start()
    try:



        for i in elements:
            doc.ActiveView.SetElementOverrides(i.Id, overrides)


        # Commit the transaction
        t.Commit()

    except Exception as e:
        # If an exception occurs, roll back the transaction
        t.RollBack()
        print(e)
