__title__ = "Elbow Up"
__author__ = "MyPy"
__doc__ = """
SAMPLE TEXT
"""

# from my_lib.import_all import *
import clr, os, traceback
from pyrevit import revit
from Autodesk.Revit.DB import Transaction

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application



# def elbow_up(element, point):
#     if element.Category.Name == "Conduits":
#         connectors = list(element.ConnectorManager.Connectors)
#         if connectors[0].Origin.DistanceTo(point) > connectors[1].Origin.DistanceTo(point):
#             true_connector = connectors[1]
#         else:
#             true_connector = connectors[0]
#
#         new_conduit = ElementTransformUtils.CopyElement(doc, element.Id, XYZ(1, 1, 1))
#         new_conduit = doc.GetElement(new_conduit[0])
#         connector_point = true_connector.Origin
#         top_point = connector_point
#         bottom_connector = XYZ(connector_point.X, connector_point.Y, connector_point.Z + 3)
#         new_line = Line.CreateBound(top_point, bottom_connector)
#         new_conduit.Location.Curve = new_line
#
#         new_connectors = list(new_conduit.ConnectorManager.Connectors)
#         if new_connectors[0].Origin.DistanceTo(connector_point) > new_connectors[1].Origin.DistanceTo(connector_point):
#
#             doc.Create.NewElbowFitting(true_connector, new_connectors[1])
#         else:
#             doc.Create.NewElbowFitting(true_connector, new_connectors[0])
#
#         return new_conduit
#     else:
#         return None

t = Transaction(doc, __title__)
t.Start()
try:
    check = LicenseChecker.CheckLicenseGranted(app)
    if check:
        elements = revit.get_selection().elements
        point = revit.pick_elementpoint(world=True)
        for element in elements:
            CustomFunctions.ElbowUp(element, point, doc, app)


    t.Commit()
except Exception as e:
    t.RollBack()
    tb_str = traceback.format_exc()
    print("IronPython Traceback:")
    print(tb_str)