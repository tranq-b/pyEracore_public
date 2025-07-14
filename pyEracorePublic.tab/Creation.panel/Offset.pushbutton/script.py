__title__ = "Offset"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script creates offset conduit runs with a specified angle between selected conduits. It pairs and offsets either a single pair of conduits or multiple parallel conduits, aligning them and automatically inserting the kick angle.

2. Steps to use:

    - Select one or multiple conduits in the model.
    
    - Run the script.
    
    - In the pop-up window, choose the desired kick angle (5, 10, 15, etc.).
    
    - Select the second conduit (or conduits) to connect.
    
    - The script will pair conduits by proximity and create offsets.

3. Result:
New conduit segments will be created at the specified angle between the selected conduits. The script ensures that the offset segments are positioned correctly along a calculated perpendicular line for optimal alignment.
"""

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


def CenterPoint(element):
    box = element.get_BoundingBox(doc.ActiveView)
    center = (box.Max + box.Min) / 2
    return center


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


        def make_angle_handler(value):
            def handler(sender, e):
                global angle
                angle = value
                FlexForm.get_values(sender, e)

            return handler


        angles = [5, 10, 11.25, 15, 22.5, 30, 45, 60, 90]

        components = [Label("Choose an angle")]
        components.extend(Button(str(ang), make_angle_handler(ang)) for ang in angles)

        if pin_conduits:
            form = FlexForm(__title__, components)
            form.show()
        else:
            forms.alert("Please select a one conduit", exitscript=True)

        if angle > 0:
            if len(pin_conduits) == 1:
                second_conduits = [revit.pick_element()]
            else:
                second_conduits = revit.pick_elements()

            if second_conduits:
                if len(pin_conduits) != len(second_conduits):
                    forms.alert("The quantity of conduits not match")
                else:
                    if len(pin_conduits) > 1:
                        pairs = CustomFunctions.PairParallelElements(CollectElements(pin_conduits),
                                                                     CollectElements(second_conduits), app)

                        closest_pair = {}

                        temp_element11 = pairs[0][0]
                        temp_element22 = pairs[1][0]

                        temp_line_element11 = temp_element11.Location.Curve

                        temp_line11 = Line.CreateUnbound(temp_line_element11.GetEndPoint(0),
                                                         temp_line_element11.Direction)

                        temp_point_element22 = CenterPoint(temp_element22)
                        temp_point_element11 = temp_line11.Project(temp_point_element22).XYZPoint

                        for pair in pairs:
                            element1 = pair[0]
                            element2 = pair[1]
                            connectors1 = list(element1.ConnectorManager.Connectors)
                            connectors2 = list(element2.ConnectorManager.Connectors)

                            closest_connectors = min(
                                ((connector1, connector2, connector1.Origin.DistanceTo(connector2.Origin)) for
                                 connector1 in connectors1 for connector2 in connectors2), key=lambda x: x[2])

                            length = closest_connectors[0].Origin.DistanceTo(closest_connectors[1].Origin)
                            closest_pair[length] = [closest_connectors[0], closest_connectors[1]]

                        min_distance = min(closest_pair.keys())
                        min_pair = closest_pair[min_distance]
                        mid_point = (min_pair[0].Origin + min_pair[1].Origin) / 2

                        perpendicular_vector = Line.CreateBound(temp_point_element11, temp_point_element22).Direction
                        perpendicular_line = Line.CreateUnbound(mid_point, perpendicular_vector)

                        for pair in pairs:
                            new_element = CustomFunctions.CreateOffset(pair[0], pair[1], angle, doc, app)
                            if not new_element:
                                new_element = CustomFunctions.CreateOffset(pair[1], pair[0], angle, doc, app)
                            doc.Regenerate()
                            center = CenterPoint(new_element)
                            new_point = perpendicular_line.Project(center).XYZPoint
                            ElementTransformUtils.MoveElement(doc, new_element.Id, new_point - center)
                    else:
                        pairs = [[pin_conduits[0], second_conduits[0]]]

                        connectors1 = list(pairs[0][0].ConnectorManager.Connectors)
                        connectors2 = list(pairs[0][1].ConnectorManager.Connectors)

                        closest_connectors = min(
                            ((connector1, connector2, connector1.Origin.DistanceTo(connector2.Origin)) for connector1 in
                             connectors1 for connector2 in connectors2), key=lambda x: x[2])

                        new_point = (closest_connectors[0].Origin + closest_connectors[1].Origin) / 2

                        new_element = CustomFunctions.CreateOffset(pairs[0][0], pairs[0][1], angle, doc, app)
                        if not new_element:
                            new_element = CustomFunctions.CreateOffset(pairs[0][1], pairs[0][0], angle, doc, app)
                        doc.Regenerate()
                        center = CenterPoint(new_element)

                        ElementTransformUtils.MoveElement(doc, new_element.Id, new_point - center)

    t.Commit()
except Exception as e:
    t.RollBack()
    tb_str = traceback.format_exc()
    print("IronPython Traceback:")
    print(tb_str)
