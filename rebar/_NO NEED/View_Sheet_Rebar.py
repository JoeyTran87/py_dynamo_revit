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

#----------------------------------------------------#
def get_sheet_view_by_search_string(search_string):
    global doc    
    viewCollector = list(FilteredElementCollector(doc).OfClass(ViewSheet))
    try:
	    view_  = [v for v in viewCollector if search_string in v.Name][0]
	    return view_
    except:
    	return

def get_sheet_view (view_name):
	""""""
	global doc#, debugger
	view_sheet = get_sheet_view_by_search_string(view_name)
	if view_sheet == None:
		try:
			# Get an available title block from document
			collector = list(FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_TitleBlocks))
			fs = collector[0]#.FirstElement()		
			TransactionManager.Instance.EnsureInTransaction(doc)	
			view_sheet = ViewSheet.Create(doc,fs.Id)
			try:
				view_sheet.SheetNumber = "000"
			except:
				view_sheet.SheetNumber = "000000000000"
			view_sheet.Name = view_name
			# Delete Title Block
			title_blocks = list(FilteredElementCollector(doc,view_sheet.Id).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().ToElements())
			[doc.Delete(t.Id) for t in title_blocks]
			TransactionManager.Instance.TransactionTaskDone()
		except Exception as ex:
			# debugger.append(ex)
			pass
	return view_sheet
#----------------------------------------------------#
#----------------------------------------------------#
# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
view_name = IN[0]

debugger = []

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()



OUT =  debugger,get_sheet_view (view_name)