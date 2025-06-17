
#IMPORT
from Autodesk.Revit.DB import *
import clr

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *

doc = DocumentManager.Instance.CurrentDBDocument

import sys

sys.path.append(r"C:\Program Files (x86)\IronPython 2.7\Lib")

#

def geometry(item):
    options = Options()
    options.DetailLevel.Coarse
    geometry = item.get_Geometry(options)
    return geometry.GetTransformed(Transform.Identity)

def IsIntersect(Solid1, Solid2):
    option = BooleanOperationsType.Intersect
    Solid = BooleanOperationsUtils.ExecuteBooleanOperation(Solid1, Solid2, option)
    if Solid.Volume > 0:
        return True
    else:
        return False

def NextElementsConnector(element):
    arry = []
    if "Conduit" in str(element):
        for connector in list(element.ConnectorManager.Connectors):
            for elements in connector.AllRefs:
                if elements.Owner.Id != element.Id:
                    arry.append(elements.Owner)
        return arry
    else:
        for connector in list(element.MEPModel.ConnectorManager.Connectors):
            for elements in connector.AllRefs:
                if elements.Owner.Id != element.Id:
                    arry.append(elements.Owner)
        return arry

def Network(element):
    network = [element]
    networkId = [element.Id]
    nexelem = element
    second_list = []
    safecount1 = 0
    safecount2 = 0
    while safecount1 < 1000:
        if nexelem == element:
            nexelem = NextElementsConnector(element)
        if len(nexelem) > 2:
            second_list.append(nexelem[-1])
            nexelem.remove(nexelem[-1])
        for elem in nexelem:
            if elem.Id not in networkId:
                networkId.append(elem.Id)
                network.append(elem)
                nexelem = NextElementsConnector(elem)
            else:
                nexelem = False
        if not nexelem:
            break
        safecount1 += 1
        print(safecount1)
    return network

def sortNetwork(network):
    arry = []
    arry1 = []
    for i in network:
        if "Conduit" in i.Category.Name:
            arry.append(i)
        else:
            arry.append(i)
            arry1.append(arry)
            arry = []
            arry.append(i)
    if arry1 == []:
        return [arry]
    else:
        return (arry1)
