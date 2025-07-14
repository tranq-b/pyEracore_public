__title__ = "Override Elements"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script applies graphic overrides in the active view to highlight selected elements with custom colors, transparency, or halftone effects. It can also fade out all other elements to keep the focus on your selection.

2. Steps to use:

    - Select elements in the model that you want to highlight.
    
    - Run the script.
    
    - In the pop-up window, choose a highlight option (Blue, Green, Red, Halftone, Custom Color, or Reset Overrides) and whether to apply halftone or line overrides.
    
    - If you pick "Custom," select any color from the color dialog.

3. Result:
The selected elements will be visually highlighted in the active view based on your chosen color and style. If "Halftone Other" is selected, all non-selected elements will appear faded, making your selection stand out.
"""
from pyrevit import revit, forms
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, OverrideGraphicSettings, Color, Element
import os, clr, traceback
from System.Collections.Generic import List

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)

from RevitPluginLib import CustomFunctions, LicenseChecker

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application


check = LicenseChecker.CheckLicenseGranted(app)
if check:

    gray = Color(50,50,50)
    blue = Color(0, 191, 255)
    green = Color(0, 255, 0)
    red = Color(250, 0, 0)
    elementsInView = FilteredElementCollector(doc, doc.ActiveView.Id).WhereElementIsNotElementType().ToElements()
    elements = revit.get_selection().elements
    elements_id = [i.Id for i in elements]
    elementsInView = [i for i in elementsInView if i.Id not in elements_id]


    overrides = OverrideGraphicSettings()
    overrides.SetSurfaceTransparency(100)
    overrides.SetCutLineColor(gray)

    cfgs = {'Blue': {'background': '0x00bfff'},
            'Green': {'background': '0x00ff00'},
            'Red': {'background': '0xff0000'},
            'Custom': {'background': '0x8000ff'},
            'Halftone': {'background': '0xFF44475A'}}

    selected_option, switches = \
        forms.CommandSwitchWindow.show(
            ['Blue', 'Green', 'Red', 'Halftone', 'Custom', 'ResOverride', 'Cancel'],
            switches=['Halftone Other', 'Override Lines'],
            message='Select Option:',
            config=cfgs,
            recognize_access_key=True
        )


    t = Transaction(doc, __title__)
    t.Start()
    try:


        line = switches['Override Lines']

        elementsInView_cs = List[Element]()
        for el in elementsInView:
            elementsInView_cs.Add(el)

        elements_cs = List[Element]()
        for el in elements:
            elements_cs.Add(el)

        # Start a transaction
        if switches['Halftone Other']:
            colors_cs = List[Color]()
            colors_cs.Add(gray)
            CustomFunctions.OverrideGraphics(doc, doc.ActiveView, elementsInView_cs, colors_cs, app, transparency=90)

        if selected_option == "Blue":

            colors_cs = List[Color]()
            colors_cs.Add(blue)
            CustomFunctions.OverrideGraphics(doc, doc.ActiveView, elements_cs, colors_cs, app, lines=line)

        elif selected_option == "Halftone":
            colors_cs = List[Color]()
            colors_cs.Add(gray)
            CustomFunctions.OverrideGraphics(doc, doc.ActiveView, elements_cs, colors_cs, app, transparency=90, lines=line)

        elif selected_option == "Green":
            colors_cs = List[Color]()
            colors_cs.Add(green)
            CustomFunctions.OverrideGraphics(doc, doc.ActiveView, elements_cs, colors_cs, app, lines=line)

        elif selected_option == "Red":
            colors_cs = List[Color]()
            colors_cs.Add(red)
            CustomFunctions.OverrideGraphics(doc, doc.ActiveView, elements_cs, colors_cs, app, lines=line)

        elif selected_option == "Custom":

            custom = forms.ask_for_color(default=None)
            hex_color = custom.lstrip('#')
            custom = tuple(int(hex_color[i:i + 2], 16) for i in (2, 4, 6))
            colors_cs = List[Color]()
            colors_cs.Add(Color(custom[0], custom[1], custom[2]))
            CustomFunctions.OverrideGraphics(doc, doc.ActiveView, elements_cs, colors_cs, app, lines=line)

        elif selected_option == "ResOverride":
            if elements == []:
                overrides = OverrideGraphicSettings()
                for i in elementsInView:
                    doc.ActiveView.SetElementOverrides(i.Id, overrides)
            else:
                for element in elements:
                    doc.ActiveView.SetElementOverrides(element.Id, overrides)





        t.Commit()
    except Exception as e:
        t.RollBack()
        tb_str = traceback.format_exc()
        print("IronPython Traceback:")
        print(tb_str)


