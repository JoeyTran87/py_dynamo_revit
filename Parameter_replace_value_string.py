# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import TaskDialog
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *
import Autodesk.Revit.DB.JoinGeometryUtils as JGU
import time
#----------------------------------------------------------------#
def getAllElementsOfCategories(doc,cates):
	global debugger
	categories = list(doc.Settings.Categories)
	category_names = [c.Name for c in categories]
	elements = []
	for cat in cates:
		try:
			if cat in category_names:
				c = categories[int(category_names.index(cat))]				
				elements.extend( [e for e in FilteredElementCollector(doc).OfCategoryId(c.Id).WhereElementIsNotElementType().ToElements()])
		except Exception as ex:
			debugger.append(ex)
			pass
	return elements


#----------------------------------------------------------------#
time_start = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))
debugger = []

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()

cates = IN[0].splitlines()
param_name = IN[1]
value_search = IN[2]
value_replace = IN[3]

TransactionManager.Instance.EnsureInTransaction(doc)
elements = getAllElementsOfCategories(doc,cates)
for e in elements:
    try:
        param = e.LookupParameter(param_name)
        if param.StorageType == StorageType.String:
            value_string = param.AsString()
            value_string = value_string.replace(value_search,value_replace)
            param.Set(value_string)
    except Exception as ex:
        debugger.append("Exception in iterating elements : {}".format(ex))


TransactionManager.Instance.TransactionTaskDone()
time_end = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))

OUT = "{0}/{1} Succeeded".format(0,len(elements)),time_start, time_end, debugger