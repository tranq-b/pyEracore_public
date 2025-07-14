__title__ = "SetArea"
__author__ = "pyEracore"
__doc__ = """
1. Description:
This script copies a parameter value from selected scope boxes or floors to all elements inside or intersecting them, by matching a "get" parameter from the box/floor to a "set" parameter on other elements.

2. Steps to use:

    - Run the script.
    
    - Select the category to use as bounding elements (Scope Boxes or Floors).
    
    - Pick one or multiple scope boxes (or all floors in view).
    
    - Choose the parameter to read from the selected boxes/floors.
    
    - Choose the parameter to write this value to on the elements in the view.
    
    - The script will assign the value to elements that are either inside the bounding box (for scope boxes) or intersect with floors.

3. Result:
All elements within the selected scope boxes or intersecting the selected floors will have their specified parameter updated with the value from the chosen parameter of the box or floor.
"""
import os, clr, traceback, sys
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, Element
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

    # SB = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_VolumeOfInterest).ToElements()
    SB = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_VolumeOfInterest).ToElements()
    FLOOR = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_Floors).ToElements()

    all_elements = FilteredElementCollector(doc, doc.ActiveView.Id).WhereElementIsNotElementType().ToElements()
    elements = all_elements

    BOX_CATEGORY = ["ScopeBox", "Floor"]
    selected_category = forms.SelectFromList.show(BOX_CATEGORY, button_name='Select Category')
    if selected_category == "ScopeBox":
        boxes_elements = []
        SB_name_list = {}
        for element in SB:
            SB_name_list.setdefault(element.Name, element)
        scopes = list(SB_name_list.keys())
        scopes = sorted(scopes)
        SB_list_selected = forms.SelectFromList.show(scopes, button_name='Select Scope Boxes',
                                                     multiselect=True)
        for box in SB_list_selected:
            boxes_elements.append(SB_name_list[box])
    elif selected_category == "Floor":
        boxes_elements = FLOOR

    parameters_list = {}
    for parameter in boxes_elements[0].Parameters:
        parameters_list.setdefault(parameter.Definition.Name, parameter)
    set_parameters_list = {}
    for e in elements:
        for parameter in e.Parameters:
            set_parameters_list.setdefault(parameter.Definition.Name, parameter)


    items = list(parameters_list.keys())
    items = sorted(items)

    set_items = list(set_parameters_list.keys())
    set_items = sorted(set_items)

    get_parameter = forms.SelectFromList.show(items, button_name='Get Parameter')
    set_parameter = forms.SelectFromList.show(set_items, button_name='Set Parameter')

    # Start a transaction
    t = Transaction(doc, __title__)
    t.Start()
    try:
        if selected_category == "ScopeBox":
            for box in boxes_elements:
                BB = box.get_BoundingBox(doc.ActiveView)
                set_value = Element.LookupParameter(box, get_parameter).AsString()
                for element in elements:
                    try:
                        # if BoundingBoxContainsElement(BB, element):
                        if CustomFunctions.BoundingBoxContainsElement(doc, app, BB, element):
                            Element.LookupParameter(element, set_parameter).Set(set_value)
                    except:
                        pass
        else:
            for box in boxes_elements:
                set_value = Element.LookupParameter(box, get_parameter).AsString()
                for element in elements:
                    # if IsIntersectElements(box, element):
                    if CustomFunctions.IsIntersectElements(doc, box, element, app):
                        try:
                            Element.LookupParameter(element, set_parameter).Set(set_value)
                        except:
                            pass

        # Commit the transaction
        t.Commit()

    except Exception as e:
        # If an exception occurs, roll back the transaction
        t.RollBack()
        print(e)
