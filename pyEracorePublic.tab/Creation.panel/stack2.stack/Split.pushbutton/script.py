__title__ = "Split Conduits"
__author__ = "MyPy"
__doc__ = """
SAMPLE TEXT
"""


from Autodesk.Revit.DB import Transaction
from pyrevit import revit
import traceback
import clr, os


dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application


t = Transaction(doc, __title__)
t.Start()
try:

    check = LicenseChecker.CheckLicenseGranted(app)
    if check:
        elements = revit.pick_rectangle()
        elements = [i for i in elements if i.Category.Name == "Conduits"]
        box = CustomFunctions.PickSplitBox(uidoc)
        for element in elements:
            CustomFunctions.SplitConduit(doc, element, box, app)

    t.Commit()
except Exception as e:
    t.RollBack()
    tb_str = traceback.format_exc()
    print("IronPython Traceback:")
    print(tb_str)

