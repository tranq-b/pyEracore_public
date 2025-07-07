
__title__ = "WP by Face"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script creates or sets a work plane in Revit based on the current view orientation and screen position, helping to quickly align the work plane to what you see.

2. Steps to use:

    - Open a 3D or plan view where you want to set the work plane.
    
    - Run the script.
    
    - The script will automatically create or adjust the work plane to match the current screen view.

3. Result:
The active work plane will be aligned to your current view, making it easier to start modeling or placing elements directly on that plane.
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

        CustomFunctions.WorkPlaneByScreen(uidoc, app)



        t.Commit()
    except Exception as e:
        # If an exception occurs, roll back the transaction
        t.RollBack()
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ISSUE IN LINE -> {}".format(exc_tb.tb_lineno))
