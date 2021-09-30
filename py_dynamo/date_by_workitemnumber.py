# Load the Python Standard and DesignScript Libraries
import sys,os,time,tempfile,shutil
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
from Autodesk.DesignScript.Geometry import Point as pt
from Autodesk.DesignScript.Geometry import Line as ln
from Autodesk.DesignScript.Geometry import Polygon as pg
from Autodesk.DesignScript.Geometry import Curve as cr
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
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference("DSCoreNodes")
clr.AddReference('DynamoServices')
from Dynamo.Events import *
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#

def flatten(t):
    return [item for sublist in t for item in sublist]	

def getAllElementsOfCategory(doc,cat):
	"""Lấy tất cả các phần tử thuộc Category
	cates (list)
	oc : Revit Document	"""	
	categories = doc.Settings.Categories		
	for c in categories:
		if c.Name == cat:					
			return list(FilteredElementCollector(doc).OfCategoryId(c.Id).WhereElementIsNotElementType().ToElements())


def browse_element(doc,cat,param = None):
	"""	"""	
	debugger = []
	exceptions = []
	categories = doc.Settings.Categories		
	for c in categories:
		try:
			if c.Name == cat:					
				elements = list(FilteredElementCollector(doc).OfCategoryId(c.Id).WhereElementIsNotElementType().ToElements())
				for e in elements:
					try:
						param_winumber = e.LookupParameter(param)
						wi_number = param_winumber.AsString()
						if wi_number.strip() != "":
							debugger.append(wi_number)

					except Exception as ex:
						exceptions.append(ex)
						pass
		except Exception as ex:
			exceptions.append(ex)
			pass
	return debugger#, exceptions

def get_dyn_path():
	return ExecutionEvents.ActiveSession.CurrentWorkspacePath
def get_revit_dir():
	return os.getcwd()

def get_temp_dir():
	tempDir = tempfile.gettempdir()
	return tempDir

def get_temp_file_path(fileName):
	tempDir = tempfile.gettempdir()
	tempFP = tempDir + fileName
	return tempFP
# def run_cmd(cmd_command):
#     """example: py C:\\Users\\tvpduy\\py_logistic\\monitor_master.py"""
#     cmd_call = f"start /B start cmd.exe @cmd /k {cmd_command}..."
#     os.system(cmd_call)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

cates = IN[0].splitlines()
param_work_item_number = IN[1]
schedule_txt_path = IN[2]


# elements = flatten([getAllElementsOfCategory(doc,cat) for cat in cates])

with open(schedule_txt_path,'r')  as f:
	OUT = f.readlines()
# OUT = get_revit_dir(), get_dyn_path() # flatten([browse_element(doc,cat,param_work_item_number) for cat in cates])
