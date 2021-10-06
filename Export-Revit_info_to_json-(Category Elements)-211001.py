# Load the Python Standard and DesignScript Libraries
import os, sys, json,clr, tempfile,shutil
from shutil import copyfile
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
time_start = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))
debugger = []
#----------------------------------------------------------------#
cates = IN[0].splitlines()

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

def getAllCategoryElementsInfoDictionary(doc,cates):
	global debugger
	res = []
	elems = getAllElementsOfCategories(doc,cates)
	for e in elems:
		try:
			res.append(getPropertiesDic(doc,e))
		except:
			pass
	return res

def getPropertiesDic(doc,e): # dictionary type for write JSON
	dic = {}
	if e:		
		params = e.Parameters			
		dic['UniqueId'] = e.UniqueId
		if doc.GetElement(e.GetTypeId()):
			dic['TypeUniqueId'] = doc.GetElement(e.GetTypeId()).UniqueId
			# dic['TypeProperties'] = getTypePropertiesDic (e,doc)
			tDic = getTypePropertiesDic (doc,e)
			for td in tDic:
				dic[td] = tDic.get(td)
		else:
			dic['TypeUniqueId'] = "NoneType"
			dic['TypeProperties'] = "NoneTypeProperties"
		for p in params:	
			try:	
				if p.StorageType == StorageType.String:
					if p.AsString():
						v = p.AsString()
						n = p.Definition.Name
						dic[n] = v
				else:
					if p.StorageType == StorageType.Double:
						if p.AsValueString():					
							if p.DisplayUnitType == DisplayUnitType.DUT_DECIMAL_DEGREES or p.DisplayUnitType == DisplayUnitType.DUT_SLOPE_DEGREES:
								v = float(p.AsDouble())
							else:
								v = float(p.AsValueString())								
							n = p.Definition.Name
							dic[n] = v
					if p.StorageType == StorageType.ElementId:
						if p.AsValueString():
							v = p.AsValueString()								
							n = p.Definition.Name
							dic[n] = v	
					if p.StorageType == StorageType.Integer:
						if p.AsValueString():
							v = p.AsValueString()								
							n = p.Definition.Name
							dic[n] = v
						else:
							v = p.AsInteger()								
							n = p.Definition.Name
							dic[n] = v
			except:
				pass
	return dic

def getTypePropertiesDic (doc,e): # dictionary type for write JSON
	params = doc.GetElement(e.GetTypeId()).Parameters
	dic = {}
	#dic['TypeUniqueId'] = doc.GetElement(e.GetTypeId()).UniqueId
	for p in params:	
		try:	
			if p.StorageType == StorageType.String:
				if p.AsString():
					v = p.AsString()
					n = p.Definition.Name
					dic[n] = v
			else:
				if p.StorageType == StorageType.Double:
					if p.AsValueString():					
						if p.DisplayUnitType == DisplayUnitType.DUT_DECIMAL_DEGREES or p.DisplayUnitType == DisplayUnitType.DUT_SLOPE_DEGREES:
							v = float(p.AsDouble())						
						else:
							v = float(p.AsValueString())								
						n = p.Definition.Name
						dic[n] = v
				if p.StorageType == StorageType.ElementId:
					if p.AsValueString():
						v = p.AsValueString()								
						n = p.Definition.Name
						dic[n] = v	
				if p.StorageType == StorageType.Integer:
					if p.AsValueString():
						v = p.AsValueString()								
						n = p.Definition.Name
						dic[n] = v
					else:
						v = p.AsInteger()								
						n = p.Definition.Name
						dic[n] = v
		except:
			pass
	return dic
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

def jsonString(data): # cho trường hợp bị lỗi JSON acsii encoder \u1111	
	res = ""
	fmr = "{0}{1}{2}"
	res2 = ""
	res3=[]
	try:
		for dat in data:
			try:
				dicStr = ""
				fm = "{0}{1}{2}{3}{4}{5}{6}"	
				#fm.format("{","123","}")	
				for d in dat:
					try:
						#res.append(type(dat.get(d)).__name__)#(dumps(d, indent = 2,sort_keys = True,ensure_ascii = True))
						tn = type(dat.get(d)).__name__
						if tn == "str":
							dicStr += fm.format("\"",d,"\"",":","\"",dat.get(d),"\"")+","
						if tn =="float":
							dicStr += fm.format("\"",d,"\"",":","",dat.get(d),"")+","
					except Exception as ex:
						res3.append(ex)
						pass
				res += fmr.format("{",dicStr[:-1],"}") +","	
			except:
				pass
		res2 = fmr.format("[",res[:-1],"")+"]"
	except:
		pass
	return res2
def getTempFilePath(fileName):
	tempDir = tempfile.gettempdir()
	tempFP = tempDir + fileName
	return tempFP

def writeTxtStringToFile(tempFP,path,exDat): #from txt string
	"""WRITE "ONE_LINE" DATA TO TEMP TXT FILE THEN COPY TO TARGET PATH"""
	with open(tempFP,"w") as f:
		f.write(exDat.encode('utf8'))
	copyfile(tempFP, path)	
	return "Succeeded"

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
try:
	data = getAllCategoryElementsInfoDictionary(doc,cates)
	dataStr = jsonString(data)
	debugger.append("Here")
	path = revitDir(doc)[0]+revitDir(doc)[1]+'.json'
	fileName = revitDir(doc)[1]+'.json'
	tempfilepath = getTempFilePath(fileName)
	filepath = revitDir(doc)[0]+revitDir(doc)[1]+'.json'

	writeTxtStringToFile(tempfilepath,filepath,dataStr)

	time_end= time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))
	OUT = "Succeeded",time_start,time_end ,debugger# cates,getAllElementsOfCategories(cates, doc),debugger,

except Exception as ex:
	debugger.append(ex)
	time_end= time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))
	OUT = "Fail",time_start,time_end, debugger


