__title__ = "Check License"
__author__ = "pyEracore"
__doc__ = """
SAMPLE TEXT
"""

import urllib2
import os
import json
import random
import string
import clr
from pyrevit import forms

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import LicenseChecker
app = __revit__.Application


username = app.LoginUserId
check = LicenseChecker.CheckLicenseGranted(app)
if not check:
    print(app.LoginUserId)



    res = forms.alert("Send the your User Id to IT Depratment:\n"
                      "Your UserID: {}".format(app.LoginUserId),
                      ok=True, yes=False, no=False, warn_icon=False)
else:
    res = forms.alert("Access Granted",
                      ok=True, yes=False, no=False, warn_icon=False)

