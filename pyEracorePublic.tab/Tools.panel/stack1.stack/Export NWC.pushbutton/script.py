__title__ = "Export NWC"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script exports selected Revit views to Navisworks NWC files. It remembers the last export folder and allows choosing between internal or shared coordinates.

2. Steps to use:

    - Select the views in Revit that you want to export.
    
    - Run the script.
    
    - Choose whether to use the last saved folder or select a new folder for the export.
    
    - Pick if you want to export with internal or shared coordinates.
    
    - The script will process each view and export it as an NWC file.

3. Result:
Each selected view will be exported as a separate NWC file into the chosen folder. If a view has no geometry, it will be skipped, and a message will appear in the console.
"""

import os, clr, traceback, sys
from Autodesk.Revit.DB import FilteredElementCollector, Options, Transform
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

    file_path_folder = os.path.join(os.path.expanduser("~"), ".cache", "RevitPlugin", "MyPy")

    if not os.path.exists(file_path_folder):
        os.makedirs(file_path_folder)

    file_path = os.path.join(os.path.expanduser("~"), ".cache", "RevitPlugin", "MyPy", "Export_NWC_Folder.txt")



    if not os.path.isfile(file_path):
        # file doesn't exist, create it
        file = open(file_path, "w")
        file.write("")
        file.close()
    file = open(file_path, "r")
    list_param = file.read()
    file.close()

    views = list(revit.get_selection())


    if views != []:
        if list_param == "":
            selected_option, switches = \
                forms.CommandSwitchWindow.show(
                    ['Select Folder', 'Cancel'],
                    switches=['Internal Coordinate'],
                    message='Select Option:',
                    recognize_access_key=True
                    )
        else:
            selected_option, switches = \
                forms.CommandSwitchWindow.show(
                    ['Load Path Folder', 'Select Folder', 'Cancel'],
                    switches=['Internal Coordinate'],
                    message='Select Option:',
                    recognize_access_key=True
                    )

        if selected_option == 'Cancel':
            sys.exit()


        if selected_option == 'Select Folder':
            path = forms.pick_folder()
            file = open(file_path, "w")
            file.write(str(path))
            file.close()

        else:
            file = open(file_path, "r")
            path = file.read()
            file.close()


        if switches['Internal Coordinate']:
            coord = "Internal"
        else:
            coord = "Shared"

        error_views = []

        max_value = len(views)
        with forms.ProgressBar(cancellable=True) as pb:
            for num, view in enumerate(views):
                if pb.cancelled:
                    break
                name = view.Name
                elements = FilteredElementCollector(doc, view.Id).WhereElementIsNotElementType().ToElements()
                gem = []
                for i in elements:
                    try:
                        if i.Category.Name != "Cameras":

                            options = Options()
                            options.View = doc.ActiveView
                            geometry = i.get_Geometry(options).GetTransformed(Transform.Identity)
                            gem.append(geometry)
                    except:
                        pass
                if gem:
                    CustomFunctions.ExportToNwc(doc, app, view, path, name, coord)
                else:
                    error_views.append("View: {} doesn't have elements and wasn't exported".format(name))
                pb.update_progress(num, max_value)


        res = forms.alert("Done",
                          ok=False, yes=True, no=False)
        if error_views:
            for e in error_views:
                print(e)
    else:
        res = forms.alert("No Selected Views",
                          ok=False, yes=True, no=False)



