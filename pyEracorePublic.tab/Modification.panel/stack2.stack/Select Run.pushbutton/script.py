__title__ = "Select Run"
__author__ = "MyPy"
__doc__ = """
SAMPLE TEXT
"""

from Autodesk.Revit.DB import ElementId, Transaction, Element
from System.Collections.Generic import List
from pyrevit import revit
from collections import deque
import traceback, os, clr

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "bin", "RevitPluginLib.dll"))
clr.AddReference(dll_path)
from RevitPluginLib import CustomFunctions, LicenseChecker

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

# def NextElementsConnector(element):
#     conns = element.MEPModel.ConnectorManager.Connectors if hasattr(element, "MEPModel") and element.MEPModel else element.ConnectorManager.Connectors
#     result = []
#     for c in conns:
#         for ref in c.AllRefs:
#             owner = ref.Owner
#             if owner.Id != element.Id:
#                 result.append(owner)
#     return result
#
#
# def SelectInRevit(nested):
#     all_elems = []
#     for lst in nested:
#         all_elems.extend(lst)
#     elementIds = List[ElementId]()
#     selList = []
#     for elem in all_elems:
#         if hasattr(elem, "Id"):
#             eid = elem.Id
#             selList.append(elem)
#         else:
#             eid = ElementId(int(elem))
#             selList.append(doc.GetElement(eid))
#         elementIds.Add(eid)
#     uidoc.Selection.SetElementIds(elementIds)
#     return selList
#
#
# def sort_to_runs(elements):
#     used = set()
#     runs = []
#     for el in elements:
#         eid = el.Id
#         if eid in used:
#             continue
#         run = [el]
#         used.add(eid)
#         queue = deque(NextElementsConnector(el))
#         while queue:
#             e = queue.popleft()
#             eid2 = e.Id
#             if eid2 in used:
#                 continue
#             run.append(e)
#             used.add(eid2)
#             if "Conduit" in e.Category.Name:
#                 queue.extend(NextElementsConnector(e))
#         runs.append(run)
#     return runs


# def SelectRun(Elements):
#
#     def NextElementsConnector(element):
#         conns = element.MEPModel.ConnectorManager.Connectors if hasattr(element,
#                                                                         "MEPModel") and element.MEPModel else element.ConnectorManager.Connectors
#         result = []
#         for c in conns:
#             for ref in c.AllRefs:
#                 owner = ref.Owner
#                 if owner.Id != element.Id:
#                     result.append(owner)
#         return result
#
#     used = set()
#     runs = []
#     for el in elements:
#         eid = el.Id
#         if eid in used:
#             continue
#         run = [el]
#         used.add(eid)
#         queue = deque(NextElementsConnector(el))
#         while queue:
#             e = queue.popleft()
#             eid2 = e.Id
#             if eid2 in used:
#                 continue
#             run.append(e)
#             used.add(eid2)
#             if "Conduit" in e.Category.Name:
#                 queue.extend(NextElementsConnector(e))
#         runs.append(run)
#     all_elems = []
#     for lst in runs:
#         all_elems.extend(lst)
#     elementIds = List[ElementId]()
#     selList = []
#     for elem in all_elems:
#         if hasattr(elem, "Id"):
#             eid = elem.Id
#             selList.append(elem)
#         else:
#             eid = ElementId(int(elem))
#             selList.append(doc.GetElement(eid))
#         elementIds.Add(eid)
#     uidoc.Selection.SetElementIds(elementIds)

check = LicenseChecker.CheckLicenseGranted(app)
if check:
    t = Transaction(doc, __title__)
    t.Start()
    try:
        elements = revit.get_selection().elements
        # SelectRun(elements)

        elements_cs = List[Element]()
        for el in elements:
            elements_cs.Add(el)

        CustomFunctions.SelectRun(uidoc, doc, elements_cs, app)

        t.Commit()
    except Exception:
        t.RollBack()
        print("IronPython Traceback:")
        print(traceback.format_exc())
