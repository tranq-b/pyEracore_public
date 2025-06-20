
__title__ = "Sorting in Schedule +"
__author__ = "Andrey.B"
__doc__ = """
SAMPLE TEXT
"""

from my_lib.import_all import *


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
data = read_file(file_name)


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




write_file(file_name, typ + [set_parameter])



objects = []
for i in elements:
    obj = {
        "id": i.Id,
    }
    for p in typ:
        value = Element.LookupParameter(i, p)
        if value:
            type = value.StorageType
            if type == DB.StorageType.String:
                obj[p] = value.AsString()
            if type == DB.StorageType.Integer:
                obj[p] = value.AsInteger()
            if type == DB.StorageType.Double:
                obj[p] = round_to_nearest(value.AsDouble(), nearest=round_dict[selected_values['round_param']])
                # obj[p] = value.AsDouble()
            if type == DB.StorageType.ElementId:
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
