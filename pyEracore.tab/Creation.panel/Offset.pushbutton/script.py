__title__ = "Offset"
__author__ = "MyPy"
__doc__ = """
SAMPLE TEXT
"""

# from my_lib.import_all import *
import clr, os, traceback
from System.Collections.Generic import List
from pyrevit import revit, forms
from Autodesk.Revit.DB import Transaction, Element
from rpw.ui.forms import FlexForm, Label, TextBox, Button, Separator, CheckBox
import time

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application


t = Transaction(doc, __title__)
t.Start()
try:
    time_start = time.time()
    check = LicenseChecker.CheckLicenseGranted(app)
    # check = True
    if check:
        time_end = time.time()
        print("Time: ", time_end - time_start)

        angle = 0
        pin_conduits = revit.get_selection().elements


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
            if len(pin_conduits) == 1:
                second_conduits = revit.pick_element()
            else:
                second_conduits = revit.pick_elements()


            if second_conduits:
                if len(pin_conduits) == 1:
                    CustomFunctions.CreateOffset(pin_conduits[0], second_conduits, angle, doc)
                else:
                    if len(pin_conduits) != len(second_conduits):
                        forms.alert("The quantity of conduits not match")
                    else:
                        pairs = CustomFunctions.PairParallelElements(CollectElements(pin_conduits), CollectElements(second_conduits), app)
                        for pair in pairs:
                            CustomFunctions.CreateOffset(pair[0], pair[1], angle, doc, app)


    t.Commit()
except Exception as e:
    t.RollBack()
    tb_str = traceback.format_exc()
    print("IronPython Traceback:")
    print(tb_str)