# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
import Autodesk.DesignScript.Geometry.Point as pt
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import TaskDialog
clr.AddReference("RevitNodes")
import Revit
import Revit.Elements.TextNote as tn
clr.ImportExtensions(Revit.Elements)
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *

import Autodesk.Revit.DB.JoinGeometryUtils as JGU

import time

dataEnteringNode = IN

debugger = []

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()


def write_text_note(viewId,position,text,typeId):
    """"""
    global doc
    if doc.GetElement(viewId) == None:
        viewId = doc.ActiveView.Id
    position = XYZ()

    if doc.GetElement(typeId) == None or not doc.GetElement(typeId).__class__ == TextNoteType:
        typeId = list(FilteredElementCollector(doc).OfClass(TextNoteType).WhereElementIsElementType())[0].Id

    TransactionManager.Instance.EnsureInTransaction(doc)
    text_note = TextNote.Create(doc,viewId,position,text,typeId = typeId)
    TransactionManager.Instance.TransactionTaskDone()


OUT = 0
