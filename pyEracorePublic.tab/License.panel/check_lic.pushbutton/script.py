__title__ = "Check License"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script checks if your license is valid. It verifies access rights for the current Revit user by calling the license server.

2. Steps to use:

    - Run the script.
    
    - The script will automatically check your user license.
    
    - If your license is not granted, it will display your Revit User ID so you can send it to the IT department.

3. Result:
If the license is valid, you will see an "Access Granted" message. If not, you will get instructions to send your User ID to IT.
"""

import urllib2
import os
import clr
from pyrevit import forms

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import LicenseChecker
app = __revit__.Application


username = app.LoginUserId
check = LicenseChecker.CheckLicenseGranted(app)
if not check:
    print("Send the your User Id to IT Depratment:\n"
                      "Your UserID: {}".format(app.LoginUserId))

else:
    res = forms.alert("Access Granted",
                      ok=True, yes=False, no=False, warn_icon=False)

