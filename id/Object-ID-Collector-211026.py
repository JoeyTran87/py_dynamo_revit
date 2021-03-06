import sys,os,re
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



#functions
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
def revitDir(doc):
	dir = ""
	try:
		p = doc.PathName.split("\\")
		pp = p[0:len(p)-1]
	
		for s in pp:
			dir += s + "\\"
	except:
		pass
	return dir,doc.PathName.split("\\")[-1].split(".rvt")[0]
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

def collector(doc,cates,file_path,file_name):
	elements = getAllElementsOfCategories(doc,cates)
	for e in elements:
		try:
			debugger.append(e.UniqueId)
		except Exception as ex:
			pass
	content = ""
	list_ = []
	try:
		param = elements[0].LookupParameter(param_name)
		if param.StorageType == StorageType.String:
			for elem in elements:
				try:
					par = elem.LookupParameter(param_name)				
					if par.AsString() != None:
						list_.append("{0}\t{1}\t{2}\t{3}".format(elem.UniqueId,par.AsString(),file_name,elem.Id))
				except:
					pass
			content = "\n".join(list_)
	except:
		pass
	with open(file_path,"w") as f:
		f.write(content)
	return elements,list_

#start
time_start = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))
debugger = []
result = []
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

#excecute
cates = IN[0].splitlines()
param_name = IN[1]
ext_dir_files = IN[2]

rvt_dir = revitDir(doc)
file_path = "{0}{1}.rvt".format(rvt_dir[0],rvt_dir[1])
file_name = rvt_dir[1]+".rvt"
revit_id_data_path = "{0}{1}-Revit-Id-Data.txt".format(rvt_dir[0],rvt_dir[1])

elements = None
list_ = None
if ext_dir_files:
	elements = []
	list_  = []
	docs = []
	patt = re.compile(r".\d\d\d\d.")	
	for p in os.listdir(revitDir(doc)[0]):
		if "rvt" in p and len(patt.findall(p)) == 1:	
			full_path = revitDir(doc)[0]+p
			doc_ = app.OpenDocumentFile(full_path)
			docs.append(doc_)
			file_path = doc_.PathName[:-len(doc_.PathName.split(".")[-1])-1]+".txt"
			file_name = doc_.PathName.split("\\")[-1][:-len(doc_.PathName.split("\\")[-1].split(".")[-1])-1]
			elems,l_ = collector(doc_,cates,file_path,file_name)
			elements.extend(elems)
			list_.extend(l_)
else:
	elements,list_ = collector(doc,cates,revit_id_data_path,file_name)
	pass


#end
time_end = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))

OUT = "{0}/{1} Succeeded".format(len(list_),len(elements)),time_start, time_end