
__title__ = "WP by Face"
__author__ = "Andrey.B"
__doc__ = """
SAMPLE TEXT
"""

# from my_lib.import_all import *


import os, clr
from Autodesk.Revit.DB import Transaction

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)
from RevitPluginLib import CustomFunctions, LicenseChecker




uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

check = LicenseChecker.CheckLicenseGranted(app)
if check:

    t = Transaction(doc, __title__)
    t.Start()
    try:

        # view = doc.ActiveView
        #
        # def WorkPlaneByScreent(view):
        #     if str(view.ViewType) == "ThreeD":
        #         orient = view.GetOrientation()
        #         point = orient.ForwardDirection
        #
        #
        #         set_point = XYZ(0, 0, 1)
        #         base_plane = DB.Plane.CreateByNormalAndOrigin(point, point)
        #         sp = DB.SketchPlane.Create(revit.doc, base_plane)
        #         revit.uidoc.ActiveView.SketchPlane = sp
        #
        # WorkPlaneByScreent(view)
        CustomFunctions.WorkPlaneByScreen(uidoc, app)



        t.Commit()
    except Exception as e:
        # If an exception occurs, roll back the transaction
        t.RollBack()
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ISSUE IN LINE -> {}".format(exc_tb.tb_lineno))
