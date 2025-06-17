__title__ = "Offset"
__author__ = "pyEracore"
__doc__ = """
SAMPLE TEXT
"""

# from my_lib.import_all import *
import clr, os, traceback
from System.Collections.Generic import List
from pyrevit import revit, forms
from Autodesk.Revit.DB import Transaction, Element, Line, ElementTransformUtils
from rpw.ui.forms import FlexForm, Label, TextBox, Button, Separator, CheckBox


dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

def CollectElements(arry):
    elem = List[Element]()
    for i in arry:
        elem.Add(i)
    return elem

t = Transaction(doc, __title__)
t.Start()
try:

    check = LicenseChecker.CheckLicenseGranted(app)
    if check:
        angle = 0
        pin_conduits = revit.get_selection().elements


        def CenterPoint(element):
            box = element.get_BoundingBox(doc.ActiveView)
            center = (box.Max + box.Min) / 2
            return center

        def angle5(sender, e):
            global angle
            angle = 5
            FlexForm.get_values(sender, e)

        def angle10(sender, e):
            global angle
            angle = 10
            FlexForm.get_values(sender, e)

        def angle11(sender, e):
            global angle
            angle = 11.25
            FlexForm.get_values(sender, e)

        def angle15(sender, e):
            global angle
            angle = 15
            FlexForm.get_values(sender, e)

        def angle22(sender, e):
            global angle
            angle = 22.5
            FlexForm.get_values(sender, e)

        def angle30(sender, e):
            global angle
            angle = 30
            FlexForm.get_values(sender, e)

        def angle45(sender, e):
            global angle
            angle = 45
            FlexForm.get_values(sender, e)

        def angle60(sender, e):
            global angle
            angle = 60
            FlexForm.get_values(sender, e)

        def angle90(sender, e):
            global angle
            angle = 90
            FlexForm.get_values(sender, e)

        components = [
            Label("Choose an angle"),
            Button("5", angle5),
            Button("10", angle10),
            Button("11.25", angle11),
            Button("15", angle15),
            Button("22.5", angle22),
            Button("30", angle30),
            Button("45", angle45),
            Button("60", angle60),
            Button("90", angle90)
        ]

        if pin_conduits:
            form = FlexForm(__title__, components)
            form.show()
        else:
            forms.alert("Please select a one conduit", exitscript=True)

        if angle > 0:
            second_conduits = revit.pick_elements()

            if second_conduits:
                if len(pin_conduits) != len(second_conduits):
                    forms.alert("The quantity of conduits not match")
                else:
                    if len(pin_conduits) > 1:
                        pairs = CustomFunctions.PairParallelElements(CollectElements(pin_conduits),
                                                                     CollectElements(second_conduits), app)
                    else:
                        pairs = [[pin_conduits[0], second_conduits[0]]]
                    closest_pair = {}
                    for pair in pairs:
                        element1 = pair[0]
                        element2 = pair[1]
                        connectors1 = list(element1.ConnectorManager.Connectors)
                        connectors2 = list(element2.ConnectorManager.Connectors)

                        closest_connectors = min(
                            ((connector1, connector2, connector1.Origin.DistanceTo(connector2.Origin)) for connector1 in
                             connectors1 for connector2 in connectors2), key=lambda x: x[2])

                        length = closest_connectors[0].Origin.DistanceTo(closest_connectors[1].Origin)
                        closest_pair[length] = [closest_connectors[0], closest_connectors[1]]

                    min_distance = min(closest_pair.keys())
                    min_pair = closest_pair[min_distance]
                    mid_point = (min_pair[0].Origin + min_pair[1].Origin) / 2

                    element1_point = CenterPoint(pairs[0][0])
                    element2_point = CenterPoint(pairs[0][1])

                    element1_direction = pairs[0][0].Location.Curve.Direction

                    temp_line = Line.CreateUnbound(element1_point, element1_direction)
                    temp_point = temp_line.Project(element2_point).XYZPoint

                    perpendicular_vector = Line.CreateBound(temp_point, element2_point).Direction

                    perpendicular_line = Line.CreateUnbound(mid_point, perpendicular_vector)

                    for pair in pairs:
                        new_element = CustomFunctions.CreateOffset(pair[0], pair[1], angle, doc, app)
                        center = CenterPoint(new_element)
                        new_point = perpendicular_line.Project(center).XYZPoint
                        ElementTransformUtils.MoveElement(doc, new_element.Id, new_point - center)


    t.Commit()
except Exception as e:
    t.RollBack()
    tb_str = traceback.format_exc()
    print("IronPython Traceback:")
    print(tb_str)