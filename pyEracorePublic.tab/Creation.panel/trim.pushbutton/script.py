__title__ = "Multi-Trim"
__author__ = "pyEracore"
__doc__ = """
SAMPLE TEXT
"""

from Autodesk.Revit.DB import Transaction
from pyrevit import revit
import traceback
import clr, os


dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application


# def TrimConduits(elements):
#     groups = {}
#     for element in elements:
#         direction = element.Location.Curve.Direction
#         direction = str(XYZ(abs(direction.X), abs(direction.Y), abs(direction.Z)))
#         groups.setdefault(direction, []).append(element)
#
#     if len(groups) == 2:
#
#         group_keys = groups.keys()
#         first_group, second_group = groups[group_keys[0]], groups[group_keys[1]]
#
#         box = first_group[0].get_BoundingBox(doc.ActiveView)
#         reference_point_1 = (box.Max + box.Min) / 2
#
#         box = second_group[0].get_BoundingBox(doc.ActiveView)
#         reference_point_2 = (box.Max + box.Min) / 2
#
#         first_group_data = {}
#         for element in first_group:
#             line = Line.CreateUnbound(
#                 element.Location.Curve.GetEndPoint(0),
#                 element.Location.Curve.Direction
#             )
#             projected_point = line.Project(reference_point_1).XYZPoint
#             first_group_data[str(element.Id)] = {
#                 "point": projected_point,
#                 "element": element
#             }
#
#         second_group_data = {}
#         for element in second_group:
#             line = Line.CreateUnbound(
#                 element.Location.Curve.GetEndPoint(0),
#                 element.Location.Curve.Direction
#             )
#             projected_point = line.Project(reference_point_2).XYZPoint
#             second_group_data[str(element.Id)] = {
#                 "point": projected_point,
#                 "element": element
#             }
#
#         # Pair elements and connect
#         pairs = []
#         while first_group_data and second_group_data:
#             closest_pair = min(
#                 ((id1, id2, (data1["point"] - data2["point"]).GetLength())
#                  for id1, data1 in first_group_data.iteritems()
#                  for id2, data2 in second_group_data.iteritems()),
#                 key=lambda x: x[2]
#             )
#             if closest_pair:
#                 id1, id2, _ = closest_pair
#                 pairs.append([first_group_data.pop(id1)["element"], second_group_data.pop(id2)["element"]])
#
#         for first_element, second_element in pairs:
#             connectors1 = first_element.ConnectorManager.Connectors
#             connectors2 = second_element.ConnectorManager.Connectors
#
#             closest_connectors = min(
#                 ((connector1, connector2, connector1.Origin.DistanceTo(connector2.Origin))
#                  for connector1 in connectors1
#                  for connector2 in connectors2),
#                 key=lambda x: x[2]
#             )
#
#             if closest_connectors:
#                 connector1, connector2, _ = closest_connectors
#                 doc.Create.NewElbowFitting(connector1, connector2)

t = Transaction(doc, __title__)
t.Start()
try:

    check = LicenseChecker.CheckLicenseGranted(app)
    if check:
        elements = revit.get_selection().elements

        if len(elements) >= 2:
            CustomFunctions.TrimConduits(doc, elements, app)




    t.Commit()
except Exception as e:
    t.RollBack()
    tb_str = traceback.format_exc()
    print("IronPython Traceback:")
    print(tb_str)

