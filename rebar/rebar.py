# Load the Python Standard and DesignScript Libraries
import os, sys, json,clr, tempfile,shutil
from shutil import copyfile
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *
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
time_start = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))
debugger = []

#----------------------------------------------------------------#
#----------------------------------------------------------------#
#----------------------------------------------------------------#
#----------------------------------------------------------------#
#----------------------------------------------------------------#
#----------------------------------------------------------------#
def setupUnit(doc):	
	try:
		#Area
		unit = Units(UnitSystem.Metric)		
		fmOp = FormatOptions(DisplayUnitType.DUT_SQUARE_METERS,UnitSymbolType.UST_NONE,0.001)		
		unit.SetFormatOptions(UnitType.UT_Area,fmOp)		
		doc.SetUnits(unit)
		#Volume
		unit1 = Units(UnitSystem.Metric)	
		fmOp1 = FormatOptions(DisplayUnitType.DUT_CUBIC_METERS,UnitSymbolType.UST_NONE,0.001)		
		unit.SetFormatOptions(UnitType.UT_Volume,fmOp1)		
		doc.SetUnits(unit)
		#doc.GetUnits().SetFormatOptions(UnitType.UT_Area,fmOp)
	except Exception as ex:
		pass
def set_dic(selection):
    elem_dic = {}
    for e in selection:
        elem_dic[str(e.Id)] = []
        elem_dic[str(e.Id)].append(e)
    return elem_dic
#----------------------------------------------------------------#
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()
#----------------------------------------------------------------#
TransactionManager.Instance.EnsureInTransaction(doc)
setupUnit(doc)
TransactionManager.Instance.TransactionTaskDone()
#----------------------------------------------------------------#

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
selection = UnwrapElement(IN[0])
if not selection.__class__.__name__ == "List":
	selection = [selection]

# Element Dictionary for quickly access
elem_dic = set_dic(selection)

# ALL REBAR IN MODEL
# CHECK IF HOST REBAR
elem_host_rebar = []
for e in selection:
    try:
        rbhd = RebarHostData.GetRebarHostData(e)
        rebars = list(rbhd.GetRebarsInHost())
        if rebars:
            elem_host_rebar.append(e)
    except Exception as ex:
    	elem_host_rebar.append(ex)
        pass




# Assign your output to the OUT variable.
OUT = elem_host_rebar