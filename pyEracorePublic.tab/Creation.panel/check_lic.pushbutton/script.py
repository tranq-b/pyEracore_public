__title__ = "check_lic"
__author__ = "MyPy"
__doc__ = """
SAMPLE TEXT
"""

import urllib2
import os
import json
import random
import string

import clr

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import LicenseChecker

app = __revit__.Application


def create_obfuscated_license_file(granted=True):

    folder = os.path.join(os.getenv("TEMP"))
    if not os.path.exists(folder):
        os.makedirs(folder)

    data = {}
    real_key = "Xy9Zk"
    data[real_key] = "ag" if granted else "ad"

    while len(data) < 100:
        key = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(5)])
        if key not in data:
            data[key] = random.choice(["false", "null", "0", "na", "maybe", "skip", ""])

    path = os.path.join(os.getenv("TEMP"), "gWk9vYzS2fFbepQ1aM8D7CNrjL0xzTqUhyoRMIbHvXJpnsEtgKc3ZfALdduWQGVh5PTlXmOYeaNBczFRKAvqM2Hs7nEJtw" + ".json")
    with open(path, "w") as f:
        json.dump(data, f)

    print("License file created at:", path)
    return real_key

def check_license():
    temp_dir = os.getenv("TEMP")
    filename = "gWk9vYzS2fFbepQ1aM8D7CNrjL0xzTqUhyoRMIbHvXJpnsEtgKc3ZfALdduWQGVh5PTlXmOYeaNBczFRKAvqM2Hs7nEJtw.json"
    path = os.path.join(temp_dir, filename)

    if not os.path.exists(path):
        print("License file not found")
        return False

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print("Failed to read license file:", e)
        return False

    real_key = "Xy9Zk"
    return data.get(real_key) == "ag"

# check = LicenseChecker.CheckAndCreateLicenseFile()

username = app.LoginUserId
check = LicenseChecker.CheckLicenseGranted(app)
if not check:
    print(app.LoginUserId)


# GIST_URL = "https://gist.githubusercontent.com/tranq-b/a3f2a4125cf11ed0f7c82868226f7718/raw/license.txt"
# current_user = "Andrey@test.ccom"
#
# try:
#     data = urllib2.urlopen(GIST_URL).read()
#     authorized_users = [line.strip() for line in data.splitlines()]
#     if current_user in authorized_users:
#         print("Have access")
#         create_obfuscated_license_file(granted=True)
#     else:
#         print("You don't have Access.")
#         create_obfuscated_license_file(granted=False)
# except Exception as e:
#     print("Somthing went wrong:", e)


# GIST_URL = "https://gist.githubusercontent.com/tranq-b/a3f2a4125cf11ed0f7c82868226f7718/raw/license.txt"
# current_user = "Andrey@test.ccom"
# data = urllib2.urlopen(GIST_URL).read()
# print(data)