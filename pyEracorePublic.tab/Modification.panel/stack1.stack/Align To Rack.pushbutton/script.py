__title__ = "Align Conduits"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script aligns multiple selected conduits relative to a reference conduit using standard spacing rules. The reference conduit acts as the starting edge all other conduits will be aligned on one side of it. The reference conduit must be at the edge of the conduit group - it cannot be located somewhere in the middle.

2. Steps to use:

    - Select the conduits you want to align.
    
    - Run the script.
    
    - Pick the edge conduit that will serve as the reference.
    
    - In the pop-up form, choose the spacing mode (Default Space, Between Side, or Between Center) and enter spacing values.
    
    - Confirm to apply alignment.

3. Result:
All selected conduits will be aligned on one side of the reference conduit according to the chosen spacing method and NEC-style spacing tables.
"""

from Autodesk.Revit.DB import Transaction, FilteredElementCollector, BuiltInCategory, XYZ, IntersectionResultArray, Line, Element, ElementTransformUtils
from Autodesk.Revit.DB.Electrical import Conduit
from pyrevit import revit
import clr, sys, os, json
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button, CheckBox)
import traceback
from System.Collections.Generic import List, Dictionary

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)
from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

check = LicenseChecker.CheckLicenseGranted(app)
if check:
    def write_file(file_name, dict_values):

        file_path_folder = os.path.join(os.path.expanduser("~"), ".cache", "RevitPlugin", "MyPy")
        if not os.path.exists(file_path_folder):
            os.makedirs(file_path_folder)

        file_path = os.path.join(file_path_folder, file_name + ".json")
        with open(file_path, 'w') as json_file:
            json.dump(dict_values, json_file)


    def read_file(file_name):

        file_path_folder = os.path.join(os.path.expanduser("~"), ".cache", "RevitPlugin", "MyPy")
        if not os.path.exists(file_path_folder):
            os.makedirs(file_path_folder)

        file_path = os.path.join(file_path_folder, file_name + ".json")

        try:
            with open(file_path, 'r') as json_file:
                dict_param = json.load(json_file)
            return dict_param
        except:
            return None


    def CenterPoint(element):

        box = element.get_BoundingBox(doc.ActiveView)
        center = (box.Max + box.Min) / 2
        return center


    def ftToFloat(string):
        minus = False
        string = string.replace("'", "").replace("\"", "").replace("-", "")
        if string[0] == "-":
            minus = True
            string = string[1:]
        try:
            num, denom = string.split()
            whole_num = 0
            decimal_denom = float(denom.split('/')[0]) / float(denom.split('/')[1])
        except:
            try:
                num = string
                whole_num = 0
                decimal_denom = 0
            except:
                whole_num = 0
                decimal_denom = 0
                num = 0

        result = float(whole_num) + float(num) / 12 + (decimal_denom / 12)
        if minus:
            result = result * -1

        return result


    res = "Default Space"

    def default(sender, e):
        global res
        res = "Default Space"
        FlexForm.get_values(sender, e)

    def side(sender, e):
        global res
        res = "Between Side"
        FlexForm.get_values(sender, e)

    def center(sender, e):
        global res
        res = "Between Center"
        FlexForm.get_values(sender, e)


    saved_values = read_file('values_alignt_to_rack')
    if saved_values:
        def_side = saved_values['space_side']
        def_center = saved_values['space_center']
    else:
        def_side = '1"'
        def_center = '2"'

    elements = revit.get_selection()
    element_pin = revit.pick_element_by_category("Conduits")

    components = [Label('Coordinate System:'),
                  Button('Default Space', default),
                  Separator(),
                  Button('Between Side', side),
                  TextBox('space_side', default=def_side),
                  Separator(),
                  Button('Between Center', center),
                  TextBox('space_center', default=def_center)]

    form = FlexForm(__title__, components)
    form.show()

    values = form.values

    saved_values = {"space_side": values['space_side'], "space_center": values['space_center']}

    write_file('values_alignt_to_rack', saved_values)

    space = 0
    dim_space = 0

    if res == "Between Center":
        space = values['space_center']

        dim_space = ftToFloat(space) * 12

    elif res == "Between Side":
        space = values['space_side']

        dim_space = ftToFloat(space) * 12



    spaces_by_size = {
        "1/2\"": {"1/2\"": 1.375, "3/4\"": 1.5, "1\"": 1.75, "1 1/4\"": 2.0, "1 1/2\"": 2.125, "2\"": 2.375, "2 1/2\"": 2.625, "3\"": 3.0, "3 1/2\"": 3.25, "4\"": 3.5, "4 1/2\"": 3.875, "5\"": 4.125, "6\"": 4.75},
        "3/4\"": {"1/2\"": 1.5, "3/4\"": 1.75, "1\"": 1.875, "1 1/4\"": 2.125, "1 1/2\"": 2.25, "2\"": 2.625, "2 1/2\"": 2.75, "3\"": 3.125, "3 1/2\"": 3.375, "4\"": 3.625, "4 1/2\"": 4.0, "5\"": 4.375, "6\"": 5.0},
        "1\"": {"1/2\"": 1.75, "3/4\"": 1.875, "1\"": 2.125, "1 1/4\"": 2.375, "1 1/2\"": 2.5, "2\"": 2.75, "2 1/2\"": 3.0, "3\"": 3.25, "3 1/2\"": 3.625, "4\"": 3.875, "4 1/2\"": 4.125, "5\"": 4.5, "6\"": 5.125},
        "1 1/4\"": {"1/2\"": 2.0, "3/4\"": 2.125, "1\"": 2.375, "1 1/4\"": 2.625, "1 1/2\"": 2.75, "2\"": 3.0, "2 1/2\"": 3.25, "3\"": 3.5, "3 1/2\"": 3.875, "4\"": 4.125, "4 1/2\"": 4.375, "5\"": 4.75, "6\"": 5.375},
        "1 1/2\"": {"1/2\"": 2.125, "3/4\"": 2.25, "1\"": 2.5, "1 1/4\"": 2.75, "1 1/2\"": 2.875, "2\"": 3.125, "2 1/2\"": 3.375, "3\"": 3.75, "3 1/2\"": 4.0, "4\"": 4.25, "4 1/2\"": 4.625, "5\"": 4.875, "6\"": 5.5},
        "2\"": {"1/2\"": 2.375, "3/4\"": 2.625, "1\"": 2.75, "1 1/4\"": 3.0, "1 1/2\"": 3.125, "2\"": 3.5, "2 1/2\"": 3.625, "3\"": 4.0, "3 1/2\"": 4.25, "4\"": 4.5, "4 1/2\"": 4.875, "5\"": 5.25, "6\"": 5.875},
        "2 1/2\"": {"1/2\"": 2.625, "3/4\"": 2.75, "1\"": 3.0, "1 1/4\"": 3.25, "1 1/2\"": 3.375, "2\"": 3.625, "2 1/2\"": 3.875, "3\"": 4.125, "3 1/2\"": 4.5, "4\"": 4.75, "4 1/2\"": 5.0, "5\"": 5.375, "6\"": 6.0},
        "3\"": {"1/2\"": 3.0, "3/4\"": 3.125, "1\"": 3.25, "1 1/4\"": 3.5, "1 1/2\"": 3.75, "2\"": 4.0, "2 1/2\"": 4.125, "3\"": 4.5, "3 1/2\"": 4.75, "4\"": 5.125, "4 1/2\"": 5.375, "5\"": 5.625, "6\"": 6.375},
        "3 1/2\"": {"1/2\"": 3.25, "3/4\"": 3.375, "1\"": 3.625, "1 1/4\"": 3.875, "1 1/2\"": 4.0, "2\"": 4.25, "2 1/2\"": 4.5, "3\"": 4.75, "3 1/2\"": 5.125, "4\"": 5.375, "4 1/2\"": 5.625, "5\"": 5.875, "6\"": 6.625},
        "4\"": {"1/2\"": 3.5, "3/4\"": 3.625, "1\"": 3.875, "1 1/4\"": 4.125, "1 1/2\"": 4.25, "2\"": 4.5, "2 1/2\"": 4.75, "3\"": 5.125, "3 1/2\"": 5.375, "4\"": 5.625, "4 1/2\"": 6.0, "5\"": 6.25, "6\"": 6.875},
        "4 1/2\"": {"1/2\"": 3.875, "3/4\"": 4.0, "1\"": 4.125, "1 1/4\"": 4.375, "1 1/2\"": 4.625, "2\"": 4.875, "2 1/2\"": 5.0, "3\"": 5.375, "3 1/2\"": 5.625, "4\"": 6.0, "4 1/2\"": 6.25, "5\"": 6.625, "6\"": 7.25},
        "5\"": {"1/2\"": 4.125, "3/4\"": 4.375, "1\"": 4.5, "1 1/4\"": 4.75, "1 1/2\"": 5.0, "2\"": 5.25, "2 1/2\"": 5.375, "3\"": 5.625, "3 1/2\"": 6.25, "4\"": 6.625, "4 1/2\"": 6.875, "5\"": 7.25, "6\"": 7.875},
        "6\"": {"1/2\"": 4.75, "3/4\"": 5.0, "1\"": 5.125, "1 1/4\"": 5.375, "1 1/2\"": 5.5, "2\"": 5.875, "2 1/2\"": 6.0, "3\"": 6.375, "3 1/2\"": 6.625, "4\"": 6.875, "4 1/2\"": 7.25, "5\"": 7.875, "6\"": 8.5}
    }


    # Start a transaction
    t = Transaction(doc, __title__)
    t.Start()
    try:

        elements_cs = List[Conduit]()
        for el in elements:
            elements_cs.Add(el)

        spaces_cs = Dictionary[str, Dictionary[str, float]]()
        for k, v in spaces_by_size.items():
            inner = Dictionary[str, float]()
            for k2, v2 in v.items():
                inner.Add(k2, v2)
            spaces_cs.Add(k, inner)

        CustomFunctions.AlignConduits(doc, elements_cs, element_pin, res, spaces_cs, dim_space, app)


        # Commit the transaction
        t.Commit()
    except Exception as e:
        t.RollBack()
        tb_str = traceback.format_exc()
        print("IronPython Traceback:")
        print(tb_str)



