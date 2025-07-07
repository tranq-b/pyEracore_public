
__title__ = "Sorting in Schedule +"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script sorts selected elements based on a sequence of chosen parameters, assigns a unique sequential number to each combination of parameter values, and writes that number into a target parameter. It also supports rounding for numeric (length) parameters. You can run the script by selecting elements directly in the model or by selecting a column in a Revit schedule and launching it from there.

2. Steps to use:

    - Select elements in the model or select a column in a Revit schedule.
    
    - Run the script.
    
    - In the dialog, specify:
    
    - The number of sorting parameters (rows).
    
    - The parameters to sort by (multi-level sorting).
    
    - The rounding precision for length values.
    
    - The target parameter to store the generated numbering.
    
    - Confirm to run.

3. Result:
Each element will receive a unique sequential code in the chosen target parameter, based on its combination of selected parameter values. Identical combinations will share the same number, making it easier to group or filter in schedules.
"""

import os, clr, traceback, sys, json
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, Element, StorageType
from pyrevit import revit, forms
from System.Collections.Generic import List
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button, CheckBox)
dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)
from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

check = LicenseChecker.CheckLicenseGranted(app)
if check:
    def round_to_nearest(value, nearest = 0.0833):
        return round(value / nearest) * nearest

    def find_common_values(lists):
        common_values = set(lists[0]).intersection(*lists[1:])

        # Convert the set back to a list
        result_list = list(common_values)
        return result_list

    def sort_objects(objects, *args):
        return sorted(objects, key=lambda x: [x[arg] for arg in args])


    def add_rows(sender, e):
        global rows, check, check_file
        check_file = False
        form.get_values(sender, e)
        values = form.values
        rows = int(values['Rows'])
        check = True


    round_dict = {
        '1/8 in': 0.0104166,
        '1/4 in': 0.0208333,
        '1/2 in': 0.041666,
        '1 in': 0.08333,
        "1 ft": 1
    }


    file_name = "Sort in Schedule"
    file_path_folder = os.path.join(os.path.expanduser("~"), ".cache", "RevitPlugin", "MyPy")
    if not os.path.exists(file_path_folder):
        os.makedirs(file_path_folder)

    file_path = os.path.join(file_path_folder, file_name + ".json")

    try:
        with open(file_path, 'r') as json_file:
            dict_param = json.load(json_file)
        data = dict_param
    except:
        data = None


    elements = revit.get_selection().elements

    types = {}
    for i in elements:
        type = i.Name
        if type not in types:
            types[type] = i


    parameters = []
    for i in types.values():
        param = i.Parameters
        try:
            param_fam = i.Symbol.Parameters
            param = list(param) + list(param_fam)
        except:
            pass
        parameters.append([p.Definition.Name for p in param])


    parameters = find_common_values(parameters)

    check_file = False

    if data:
        check_file = True
        for d in data:
            if d not in parameters:
                check_file = False
                break



    rows = 6
    if check_file:
        rows = len(data) - 1
    check = True
    while check:

        check = False

        components = [
            TextBox("Rows", str(rows)),
            Button("Set Rows", add_rows),
            Label("Select round for Lengths Parameters"),
            ComboBox("round_param", round_dict.keys(), default="1/8 in"),
            Separator(),
            Label("Select Parameters"),
            ]
        if check_file:
            for i in range(1, rows + 1):
                components.append(ComboBox("parameter" + str(i), parameters, default=data[i - 1]))
        else:
            for i in range(1, rows + 1):
                components.append(ComboBox("parameter" + str(i), parameters))

        components += [
            Separator(),
            Label("Select Fill Parameter")
        ]
        if check_file:
            components += [
            ComboBox("fill_param", parameters, default=data[-1]),
            Button("Run")
        ]
        else:
            components += [
                ComboBox("fill_param", parameters),
                Button("Run")
            ]

        form = FlexForm("Select Parameters", components)
        form.show()

    selected_values = form.values




    set_parameter = selected_values['fill_param']


    typ = []
    for i in range(1, rows + 1):
        search = "parameter" + str(i)
        typ.append(selected_values[search])




    # write_file(file_name, typ + [set_parameter])

    file_path_folder = os.path.join(os.path.expanduser("~"), ".cache", "RevitPlugin", "MyPy")
    if not os.path.exists(file_path_folder):
        os.makedirs(file_path_folder)

    file_path = os.path.join(file_path_folder, file_name + ".json")
    with open(file_path, 'w') as json_file:
        json.dump(typ + [set_parameter], json_file)


    objects = []
    for i in elements:
        obj = {
            "id": i.Id,
        }
        for p in typ:
            value = Element.LookupParameter(i, p)
            if value:
                type = value.StorageType
                if type == StorageType.String:
                    obj[p] = value.AsString()
                if type == StorageType.Integer:
                    obj[p] = value.AsInteger()
                if type == StorageType.Double:
                    obj[p] = round_to_nearest(value.AsDouble(), nearest=round_dict[selected_values['round_param']])
                    # obj[p] = value.AsDouble()
                if type == StorageType.ElementId:
                    obj[p] = value.AsElementId().IntegerValue
        objects.append(obj)


    sorted_objects = sort_objects(objects, *typ)



    unique_combinations = {}
    unique_number = 1

    for obj in sorted_objects:

        id = obj["id"]
        del obj["id"]

        param_values = tuple(obj.values())


        obj["id"] = id

        if param_values not in unique_combinations:

            unique_combinations[param_values] = unique_number
            unique_number += 1

    for obj in sorted_objects:
        id = obj["id"]
        del obj["id"]
        param_values = tuple(obj.values())
        obj["id"] = id
        obj["num"] = unique_combinations[param_values]






    t = Transaction(doc, __title__)
    t.Start()
    try:

        for obj in sorted_objects:
            element = doc.GetElement(obj["id"])
            set_value = obj["num"]
            if set_value < 100 and set_value < 10:
                set_value = "00" + str(obj["num"])
            elif set_value < 100:
                set_value = "0" + str(obj["num"])
            else:
                set_value = str(obj["num"])


            Element.LookupParameter(element, set_parameter).Set(set_value)

        t.Commit()
    except Exception as e:
        # If an exception occurs, roll back the transaction
        t.RollBack()
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ISSUE IN LINE -> {}".format(exc_tb.tb_lineno))
