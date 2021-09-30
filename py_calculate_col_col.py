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
#----------------------------------------------------------------#

debugger = []

def calculate_col_vol(column):	
	global debugger
	param_write = column.LookupParameter(param_write_name)	
	if param_write.StorageType == StorageType.String:		
		volume = round(column.LookupParameter("Volume").AsDouble()*0.0283168,3)	
		
		try:	
			intersect_elements = []	
			for cat in cats_2:
				intersect_elements.extend(collector.OfCategoryId(cat.Id).WherePasses(ElementIntersectsElementFilter(column)))
			joined_elements = [doc.GetElement(i) for i in JGU.GetJoinedElements(doc,column) if doc.GetElement(i).Category.Name in cats]
			intersect_elements.extend(joined_elements)			
			elevations = [] # Bottom faces elevation			
			for e in intersect_elements:
				try:
					if e.Category.Name == "Structural Framing":
						elevations.append(round(e.LookupParameter("Elevation at Bottom").AsDouble()*304.8))
				except Exception as ex:
					debugger.append(ex)
					pass
			min_elevation = min(elevations)
			
			
			b_box = column.get_BoundingBox(doc.ActiveView)
			e_max = round(b_box.Max.Z * 304.8)
			e_min = round(b_box.Min.Z * 304.8)		
			above_volume = round(((e_max - min_elevation)/((e_max - min_elevation)+(min_elevation - e_min))) * volume,3)
			under_volume = volume - above_volume		
			param_write.Set("{0};{1}".format(above_volume,under_volume))#f"{above_volume};{under_volume}"))	
			return 1
		except Exception as ex:
			debugger.append(ex)
			param_write.Set(str(volume))
			return 0
	else:
		return 0
#----------------------------------------------------------------#


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

columns = UnwrapElement(IN[0])
cats = IN[1].splitlines()
param_write_name = IN[2]

categories = doc.Settings.Categories
cats_2 = []
for cat in categories:
	if cat.Name in cats:
		cats_2.append(cat)
	else:
		pass
collector = FilteredElementCollector(doc)

count = 0
TransactionManager.Instance.EnsureInTransaction(doc)

for column in columns:
	 count += calculate_col_vol(column)

TransactionManager.Instance.TransactionTaskDone()


# OfCategoryId(cat.Id).
# Assign your output to the OUT variable.
OUT = debugger#"{0} / {1} Succeeded Calculated and write to their parameter".format(count,len(columns))