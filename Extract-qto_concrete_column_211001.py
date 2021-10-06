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

time_start = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))

debugger = []

def calculate_col_vol(column,ratio = 0.5,base_point = None):
	global debugger
	global param_write_name, param_write_not_cal,param_write_notice
	translate_ele= 0 
	if base_point != None:
		translate_ele = round(base_point.Z*304.8)
	try:	
		param_write = column.LookupParameter(param_write_name)	
		param_write_NC = column.LookupParameter(param_write_not_cal)
		param_write_note = column.LookupParameter(param_write_notice)
		volume = round(column.LookupParameter("Volume").AsDouble()*0.0283168,3)# column.LookupParameter("Volume").AsDouble()#	
		if param_write.StorageType == StorageType.Double and param_write_NC.StorageType == StorageType.Double and param_write_note.StorageType == StorageType.String:		
			b_box = column.get_BoundingBox(doc.ActiveView)
			e_max = round(b_box.Max.Z * 304.8) - translate_ele # Top elevation of Column
			e_min = round(b_box.Min.Z * 304.8) - translate_ele# Bottom elevation of Column
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
					# debugger.append(ex)
					pass						
			# VERIFY min_elevation
			min_elevation = min(elevations)	
			while True:
				if min_elevation-e_min > (e_max-e_min)*ratio:
					break
				else:
					"""Except"""
					elevations.remove(min_elevation)
					min_elevation = min(elevations)	
			
			min_elevation = min(elevations)		
			
			# debugger.append(min_elevation)
			
			above_volume = round(((e_max - min_elevation)/((e_max - e_min))) * volume,3)
			under_volume = volume - above_volume		
			
			param_write.Set(under_volume)#("{0};{1}".format(above_volume,under_volume))#f"{above_volume};{under_volume}"))	
			param_write_NC.Set(above_volume)	
			note = "Beam H ={0}".format(str(round(e_max-min_elevation)))
			param_write_NC.Set(note)
			debugger.append(note)
			return 1
		else:
			raise Exception ("Parameter Storage Type Wrong !!")
	except Exception as ex:
		debugger.append(ex)
		param_write.Set(volume)
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
ratio = IN[3]
param_write_not_cal = IN[4]
param_write_notice = IN[5]

siteCategoryfilter = ElementCategoryFilter(BuiltInCategory.OST_ProjectBasePoint)
basepoint = FilteredElementCollector(doc).WherePasses(siteCategoryfilter).ToElements()[0].Position


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
	 count += calculate_col_vol(column,ratio=ratio,base_point=basepoint)

TransactionManager.Instance.TransactionTaskDone()

time_end= time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))
# OfCategoryId(cat.Id).
# Assign your output to the OUT variable.
OUT = time_start,time_end,"{0} / {1} Succeeded".format(count,len(columns)),debugger,