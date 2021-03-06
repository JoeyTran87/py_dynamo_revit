# This Python file uses the following encoding: utf-8
import os, sys, json,clr, tempfile,shutil
from shutil import copyfile

dynPyDir = r"\\hcmcfcfs01\databim$\BimESC\00-BIM STANDARD\PYTHON\pythondynamo"
sys.path.append(dynPyDir)
revitDir = r"C:\Program Files\Autodesk\Revit 2020"
sys.path.append(revitDir)
revitDynamoDir1 = r"C:\Program Files\Autodesk\Revit 2020\AddIns\DynamoForRevit\Revit"
revitDynamoDir2 = r"C:\Program Files\Autodesk\Revit 2020\AddIns\DynamoForRevit"
sys.path.append(revitDynamoDir1)
sys.path.append(revitDynamoDir2)

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
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference('System.Windows.Forms')
import System.Windows.Forms
from System.Windows.Forms import *
import Autodesk.Revit.DB.JoinGeometryUtils as JGU


import pyDyn
from pyDyn import *

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()		

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getTempDir():
	tempDir = tempfile.gettempdir()
	return tempDir
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getTempFilePath(fileName):
	tempDir = tempfile.gettempdir()
	tempFP = tempDir + fileName
	return tempFP
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#

def writeTxtStringToFile(tempFP,path,exDat): #from txt string
	"""WRITE "ONE_LINE" DATA TO TEMP TXT FILE THEN COPY TO TARGET PATH"""
	with open(tempFP,"w") as f:
		f.write(exDat.encode('utf8'))
	copyfile(tempFP, path)	
	return "Succeeded"

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def writeTxtStringToFile2(path,exDat): #from txt string
	with open(path,"w") as ff:
		ff.write(exDat.encode('utf8'))
	return "Succeeded"
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def splitDynString(cates):	
	# newcats = []
	# if cates:
	# 	cateLines = cates.split("\n")
	# 	# if len(cateLines)==2:
	# 	# 	newcats.append(cates[:-2])
	# 	if len(cateLines)>=2:
	# 		for cat in cateLines[:-1]:
	# 			if len(cat[:-1])>0:
	# 				newcats.append(cat[:-1])	
	# 		if len(cateLines[-1])>0:
	# 			newcats.append(cateLines[-1])
	# 	else:
	# 		if len(cates)>0:
	# 			newcats.append(cates)
	return cates.splitlines()
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def splitDynString2(cates,doc):	
	# newcats = []
	categories = doc.Settings.Categories
	categories = [c.Name for c in categories]
	# newcats2 = []
	# if cates:
	# 	cateLines = cates.split("\n")
	# 	# if len(cateLines)==2:
	# 	# 	newcats.append(cates[:-2])
	# 	if len(cateLines)>=2:
	# 		for cat in cateLines[:-1]:
	# 			if len(cat[:-1])>0:
	# 				newcats.append(cat[:-1])	
	# 		if len(cateLines[-1])>0:
	# 			newcats.append(cateLines[-1])
	# 	else:
	# 		if len(cates)>0:
	# 			newcats.append(cates)
	# for nc in cates.splitlines():
	# 	for cat in categories:
	# 		if nc ==  cat.Name:
	# 			newcats2.append(nc)	
	return [cat for cat in cates.splitlines() if cat in categories]

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def orderedCategoryPair(categoryNames):
	pairs = {}
	count = len(categoryNames)
	if count > 2:
		for i in range(count-1):
			category_first = categoryNames[i]
			rest_categoryNames = categoryNames[i+1:] 
			each_cat_pairs = categoryPair(category_first,rest_categoryNames)
			# for p in each_cat_pairs:
			# 	pairs.append(p)
			pairs[category_first] = each_cat_pairs
	if count == 2:
		pairs[categoryNames[0]] = categoryPair(categoryNames[0],categoryNames[1])
		
	return pairs
	
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def categoryPair(cat,listCat):
	pairs = []
	if len(listCat) > 0:
		for c in listCat:
			# pair = []
			# pair.append(cat)
			# pair.append(c)
			# pairs.append(pair)
			pairs.append(c)
	return pairs

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
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

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getAllElementsOfCategories(cates,doc):
	"""L???y t???t c??? c??c ph???n t??? thu???c Danh s??ch category
	### cates (list)
	### doc : Revit Document
	"""
	try:
		categories = doc.Settings.Categories		
		for c in categories:
			try:
				for cat in cates:
					try:
						if cat and c.Name == cat:
							for e in FilteredElementCollector(doc).OfCategoryId(c.Id).WhereElementIsNotElementType().ToElements():
								yield e
					except:
						pass
			except:
				pass
	except:
		pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getCategoryByName(cateName,doc):
	category = []
	try:
		categories = doc.Settings.Categories
		for c in categories:
			try:
				if cateName and c.Name == cateName:
					category = c
			except:
				pass
	except:
		pass
	return category

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getPropertiesDic(e,doc): # dictionary type for write JSON
	dic = {}
	if e:		
		params = e.Parameters			
		dic['UniqueId'] = e.UniqueId
		if doc.GetElement(e.GetTypeId()):
			dic['TypeUniqueId'] = doc.GetElement(e.GetTypeId()).UniqueId
			# dic['TypeProperties'] = getTypePropertiesDic (e,doc)
			tDic = getTypePropertiesDic (e,doc)
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

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getPropertiesDic2(e,doc): # dictionary type for write JSON
	dic = {}
	if e:		
		params = e.Parameters			
		dic['UniqueId'] = e.UniqueId
		dic['LocationType'] = checkLocation(e)
		dic['LocationPoint'] = getLocationPoints2(e)
		if doc.GetElement(e.GetTypeId()):
			dic['TypeUniqueId'] = doc.GetElement(e.GetTypeId()).UniqueId
			# dic['TypeProperties'] = getTypePropertiesDic (e,doc)
			tDic = getTypePropertiesDic (e,doc)
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

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getTypePropertiesDic (e,doc): # dictionary type for write JSON
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

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getAllCategoryElementsInfoDictionary(doc,cates):
	res = []
	elems = getAllElementsOfCategories(splitDynString(cates),doc)
	for e in elems:
		try:
			res.append(getPropertiesDic(e,doc))
		except:
			pass
	return res

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getAllCategoryElementsInfoDictionaryYield(doc,cates):
	elems = getAllElementsOfCategories(splitDynString(cates),doc)
	for e in elems:
		try:
			yield getPropertiesDic(e,doc)
		except:
			pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getAllCategoryElementsInfoDictionary2(doc,cates):
	res = []
	elems = getAllElementsOfCategories(splitDynString(cates),doc)
	for e in elems:
		try:
			res.append(getPropertiesDic2(e,doc))
		except:
			pass
	return res

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def writeParameterValueMulti(elems,paramName,value):
	res = []
	TransactionManager.Instance.EnsureInTransaction(doc)
	for e in elems:
		try:
			param = e.LookupParameter(paramName)
			param.Set(value)
		except:
			pass
		res += 1
	TransactionManager.Instance.TransactionTaskDone()
	return res
def writeParameterValueSingle(e,paramName,value):	
	try:
		param = e.LookupParameter(paramName)
		param.Set(value)
	except:
		pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
# TXT
TAB = "____"
ATTBREAK = " : "
LINEBREAK = "\n"

def getProperties (params,ATTBREAK,TAB): #one line for text writing
	oneline = ""
	for p in params:		
		try:
			cbTxt = "{0}{2}{1}"			
			n = p.Definition.Name
			v= ""
			if p.AsValueString():
				v = p.AsValueString()
			else:
				if p.StorageType == StorageType.String:
					if p.AsString():
						v = p.AsString()		
			oneline += cbTxt.format(n,v,ATTBREAK) + TAB
		except:
			pass
	return oneline


#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def extractInfo (doc,res,TAB,LINEBREAK):
	strDat = ""
	for e in res:
		try:
			# projectInfoDat + BREAK
			#type property
			typ = doc.GetElement(e.GetTypeId())
			try:
				strDat += getProperties(typ.Parameters) + TAB
			except:
				pass
			#instance property
			try:
				strDat +=  getProperties(e.Parameters) + TAB	
				strDat +=  LINEBREAK
			except:
				pass
			elemDat.append(strDat)	
		except:
			pass
	return strDat		

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def writeTxtFromExcelDat(exDat,_TAB,_BREAKLINE): #from excel data list
	"""#WRITE EXCEL DATA LIST TO TEMP TXT FILE THEN COPY TO TARGET PATH"""
	allText=""
	TAB = _TAB
	BREAKLINE = _BREAKLINE	
	for d in exDat:
		str = ""
		strF = "{0}{1}"		
		if d[0] and len(d)>0:		
			for c in d:
				if c:
					str += strF.format(c,TAB)
		if len(str)>0:
			str += BREAKLINE	
		#list1Line.append(str)
		allText += str	
	f = open(path,"w")
	f.write(allText.encode('utf8'))
	f.close
	return allText

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def readJson(path):	
	"""#process JSON	"""
	res = []
	with open(path,"r") as f:
		for j in json.load(f):
			res.append(j)
	return res

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def readJsonYield(path):	
	with open(path,"r") as f:
		for j in json.load(f):
			yield j

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def writeJsonFile(data,doc):
	count = 0
	newData = []
	for d in data:
		try:
			if dumps(d):
				newData.append(d)
				count += 1
		except:
			pass

	with open(revitDir(doc)[0]+revitDir(doc)[1]+'.json','w') as f:		
		#dic = getPropertiesDic(e,doc)					
		json.dumps(newData,f)
	return newData

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def writeJson(path,data):
	with open(path,'w',encoding="mbcs") as f:				
		f.write(json.dumps(data))
	return "Succeeded"

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def jsonString(data): # cho tr?????ng h???p b??? l???i JSON acsii encoder \u1111	
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

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def UnjoinElementAlready(e,doc,cat):
	"""## process JOIN GEOMETRY"""
	res = []
	try:
		joinedElems = getJoinElement(e,doc,cat)
		for ee in joinedElems:
			try:
				JGU.UnjoinGeometry(doc,e,ee)
				res.append(ee)
			except:
				pass
	except:
		pass
	return res
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getJoinElement(e,doc,cat):
	for j in JGU.GetJoinedElements(doc,e):
		try:
			if doc.GetElement(j).Category.Name == cat:
				yield doc.GetElement(j)
		except:
			pass
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def allElemsOfCat (catName,doc):
	res = []
	rvt_Cat = []
	for _Cat in doc.Settings.Categories:
		if _Cat.Name == catName.ToString():
			rvt_Cat = _Cat	
	for e in FilteredElementCollector(doc).OfCategoryId(rvt_Cat.Id).WhereElementIsNotElementType().ToElements():
		try:
			yield e
		except:
			pass
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def allElemsIntersectedOfCat(elem,catName,doc):
	res = []
	rvt_Cat = getCategoryByName(catName,doc)
	for intersect_elem in FilteredElementCollector(doc).OfCategoryId(rvt_Cat.Id).WherePasses(ElementIntersectsElementFilter(elem)):#.ToElements()#.WhereElementIsNotElementType()	
		try:
			yield intersect_elem
		except:
			pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#  
def allElemsIntersected(elem,doc):
	for intersect_elem in FilteredElementCollector(doc).WherePasses(ElementIntersectsElementFilter(elem)):#.ToElements()#.WhereElementIsNotElementType()	
		try:
			yield intersect_elem
		except:
			pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def allElemsJoined(elem,doc,JGU):
	for joined_elem in JGU.GetJoinedElements(doc,elem):
		try:
			yield doc.GetElement(joined_elem)
		except:
			pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def allElemsNotIntersectedOfCat(elem,catName,doc):
	rvt_Cat = []
	for _Cat in doc.Settings.Categories:
		if _Cat.Name == catName.ToString():
			rvt_Cat = _Cat	
	joined_elems = getJoinElement(elem,doc,catName)	
	for je in joined_elems:
		if not JGU.IsCuttingElementInJoin(doc, elem, je):
			yield je

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def joinTwoElement(doc,a,b):
	try: 
		boolCut = JGU.AreElementsJoined(doc,a,b)
		#JGU.UnjoinGeometry(doc,a,b)		
		if not boolCut:
			JGU.JoinGeometry(doc,a,b)
		if not JGU.IsCuttingElementInJoin(doc,a,b):
			JGU.SwitchJoinOrder(doc,a,b)
	except :
		pass	

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def UnjoinTwoElement(doc,a,b):
	try:
		JGU.UnjoinGeometry(doc,a,b)
	except:
		pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def joinAllEnableJoinedElemsOfCat(e,cat,doc):
	elems = allElemsIntersectedOfCat(e,cat,doc)
	for el in elems:
		try:
			joinTwoElement(doc,e,el)
		except:
			pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def UnjoinAllNotJoinedElemsOfCat(e,cat,doc):
	elems = allElemsNotIntersectedOfCat(e,cat,doc)
	for el in elems:
		try:
			UNjoinTwoElement(doc,e,el)
		except:
			pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def autoJoin(doc,catsDic):	
	count = 0
	count2 = 0
	prompt = "{0} elements & {1} Joined Element "
	TransactionManager.Instance.EnsureInTransaction(doc)
	for dic in catsDic:
		try:
			catName1 = dic
			elem1 = allElemsOfCat(catName1,doc)
			for cat in catsDic.get(dic):
				try:
					catName2 = cat
					elem2 = allElemsOfCat(catName2,doc)
				except:
					pass
			for e1 in elem1:
				try:
					for catName2 in catsDic.get(dic):
						# elem2 = allElemsOfCat(catName2,doc)
						joinAllEnableJoinedElemsOfCat(e1,catName2,doc)
						joined = getJoinElement(e1,doc,catName2)
						for j in joined:
							try:
								joinTwoElement(doc,e1,j)
							except:
								pass
							count2 += 1
						UnjoinAllNotJoinedElemsOfCat(e1,catName2,doc)					
						count += 1
				except:
					pass
				
		except:
			pass
	TransactionManager.Instance.TransactionTaskDone()
	return prompt.format(count,count2)

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def unjoinAll(doc,catsDic,JGU):
	count = 0
	count2 = 0
	prompt = "{0} elements already processed UNJOIN & {1} Joined Elements Released"
	TransactionManager.Instance.EnsureInTransaction(doc)
	for dic in catsDic:
		try:
			catName1 = dic
			elem1 = allElemsOfCat(catName1,doc)							
			for e1 in elem1:
				try:
					joinedElems = allElemsJoined(e1,doc,JGU)
					for je in joinedElems:
						try:
							UnjoinTwoElement(doc,e1,je)
						except:
							pass
						count2 += 1
					count += 1
				except:
					pass
		except:
			pass
	TransactionManager.Instance.TransactionTaskDone()
	return prompt.format(count,count2)

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#Revit Link
def getLinkDoc(link):
	linkDoc = []
	try:
		linkDoc = link.GetLinkDocument()
	except:
		pass
	return linkDoc

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def partsFromLink(doc,link,linkCateName):
	linkDoc = getLinkDoc(link)
	linkcategory = getCategoryByName(linkCateName,linkDoc)
	linkElements = FilteredElementCollector(linkDoc).OfCategoryId(linkcategory.Id).WhereElementIsNotElementType().ToElements()
	
	eList = []
	for link_elem in linkElements:
		eList.append(LinkElementId(link.Id,link_elem.Id))
	
	createparts=[]
	try:
		TransactionManager.Instance.EnsureInTransaction(doc)
		createparts = PartUtils.CreateParts(doc, eList)
		TransactionManager.Instance.TransactionTaskDone()
	except:
		pass
	return createparts

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#GEOMETRY
def getSolids(e):
	opt = Options()	
	solid = []
	try:
		geoE1 = e.get_Geometry(opt)
		geoE2 = []
		enum = geoE1.GetEnumerator()	
		while enum.MoveNext():
			geoE2 = enum.Current
			if isinstance(geoE2,Solid):
				solid.Add(geoE2)		
			else:
				if isinstance(geoE2,GeometryInstance):
					geoObj = geoE2.GetInstanceGeometry()
					for s in geoObj:
						if isinstance(s,Solid) and s.Volume > 0:
							solid.Add(s)	
	except Exceptyion, ex:
		mergedSolid.append(ex)
		pass	
	return solid

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#	
def getLocationCurve(element):
	curve = []
	if element.Location.__class__ == LocationCurve:
		curve = element.Location
	return curve

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getLocationCurves(elements):
	curves = []
	for element in elements:
		try:
			curves.append(getLocationCurve(element))
		except:
			pass
	return curves

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getLocation(elements):
	curves = []
	points = []
	for element in elements:
		try:
			if element.Location.__class__ == LocationCurve:
				curves.append(element.Location)
			if element.Location.__class__ == LocationPoint:
				points.append(element.Location)
		except:
			pass
	return curves, points

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getLocationPoints(elements):
	curves = []
	points = []
	for element in elements:
		try:
			if element.Location.__class__ == LocationCurve:
				c = element.Location
				p = []
				p.append(c.Curve.GetEndPoint(0))
				p.append(c.Curve.GetEndPoint(1))
				curves.append(p)
			if element.Location.__class__ == LocationPoint:
				points.append(element.Location.Point)
		except:
			pass
	return curves, points

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getLocationPoints1(element):
	res = ""
	try:
		c = element.Location
		if c.__class__ == LocationCurve:
			res += str(c.Curve.GetEndPoint(0).X*304.8) +" "
			res += str(c.Curve.GetEndPoint(0).Y*304.8) +" "
			res += str(c.Curve.GetEndPoint(0).Z*304.8) +" "
			res += str(c.Curve.GetEndPoint(1).X*304.8) +" "
			res += str(c.Curve.GetEndPoint(1).Y*304.8) +" "
			res += str(c.Curve.GetEndPoint(1).Z*304.8)
		if c.__class__ == LocationPoint:
			res += str(c.Point.X*304.8) +" "
			res += str(c.Point.Y*304.8) +" "
			res += str(c.Point.Z*304.8)
	except:
		pass
	return res

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getLocationPoints2(element): # lay Trung Diem - Mid point cua Location Curve
	res = ""
	try:
		c = element.Location
		if c.__class__ == LocationCurve:
			res += str((c.Curve.GetEndPoint(0).X*304.8+c.Curve.GetEndPoint(1).X*304.8)/2) +" "
			res += str((c.Curve.GetEndPoint(0).Y*304.8+c.Curve.GetEndPoint(1).Y*304.8)/2) +" "
			res += str((c.Curve.GetEndPoint(0).Z*304.8+c.Curve.GetEndPoint(1).Z*304.8)/2)
		if c.__class__ == LocationPoint:
			res += str(c.Point.X*304.8) +" "
			res += str(c.Point.Y*304.8) +" "
			res += str(c.Point.Z*304.8)
	except:
		pass
	return res

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def checkLocation(element):
	res = None
	try:
		if element.Location.__class__ == LocationCurve:
			res = "LocationCurve"
		elif element.Location.__class__ == LocationPoint:
			res = "LocationPoint"
		else:
			res = "Undefined"
	except:
		pass
	return res

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
# solid
def UnionSolid (solids):
	mergedSolid = None
	try:
		if len(solids) == 0:
			return null
		if len(solids) == 1:
			return solids[0]
		else:			
			first = solids[0]
			res = solids[1:]
			second = UnionSolid(res)			
			mergedSolid = BooleanOperationsUtils.ExecuteBooleanOperation(first,second,BooleanOperationsType.Union)
	except:
		pass
	return mergedSolid

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#
def getRawVolume(solids):
	vol = 0
	try:
		for s in solids:
			vol += s.Volume*0.0283168
	except:	
		pass
	return vol

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#

def getSeftVolume(solids): #Intersect SOlids togeget
	mergedSolid = []
	vol = []
	try:
		mergedSolid = UnionSolid(solids)
		vol = mergedSolid.Volume*0.0283168
	except:	
		pass
	return vol

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
# SHARED PARAMETER
shareParamDataBreak = "_" #shareParamDataBreak
extDefs=[]
definition=""
def getParameterDefinitions(doc):
	"""## get share parameter from file"""
	doc = DocumentManager.Instance.CurrentDBDocument
	uiapp = DocumentManager.Instance.CurrentUIApplication
	app = uiapp.Application
	paraDefs = []
	paraDefNames = []
	definition = app.OpenSharedParameterFile()
	#res = definition.Groups.Item["COF"].Name	
	#CASE parameter file has ONLY 1 COF group
	defGSenum = enumerate(definition.Groups.GetEnumerator())
	for defG in defGSenum:
		if defG[1].Name == "COF":
			dg = defG[1]
			des = dg.Definitions
			for de in des:
				#str=de.GUID+spbr+de.Name+spbr+de.ParameterType+spbr+de.ParameterGroups+spbr+de.Visible+spbr+de.Description+spbr+de.UserModifiable+spbr+de.HideWhenNoValue # FAIL ParameterGroups
				paraDefs.append(de)
				paraDefNames.append(de.Name)
	return paraDefs, paraDefNames


#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def createMultiParameter(doc,paraDefs,cates, paramGroup,prefix):
	res = []
	count = 0
	pg = BuiltInParameterGroup.PG_CONSTRUCTION
	if paramGroup == "Structural":
		pg = BuiltInParameterGroup.PG_STRUCTURAL
	
	catsenum = enumerate(doc.Settings.Categories.GetEnumerator())
	catset = CategorySet()	
	for cat in catsenum:	
		try:
			for cate in cates:
				try:
					if cat[1].Name == cate:
						catset.Insert(cat[1])
				except Exception, ex:
					res.append(ex)
					pass
		except Exception, ex:
			res.append(ex)
			pass
	TransactionManager.Instance.EnsureInTransaction(doc)
	for de in paraDefs:# Case ALL			
		try:
			if de.Name.split(shareParamDataBreak)[0] == prefix:
				newIB = InstanceBinding(catset)
				doc.ParameterBindings.Insert(de,newIB,pg)
				#update by ReInsert
				doc.ParameterBindings.ReInsert(de,newIB,pg)
				count += 1
		except Exception, ex:
			res.append(ex)
			pass
	TransactionManager.Instance.TransactionTaskDone()
	res.append(count)
	return catset

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#

""" BuiltInParameterGroup
PG_ROUTE_ANALYSIS	
PG_GEO_LOCATION	
PG_STRUCTURAL_SECTION_GEOMETRY	
PG_ENERGY_ANALYSIS_BLDG_CONS_MTL_THERMAL_PROPS	
PG_ENERGY_ANALYSIS_ROOM_SPACE_DATA	
PG_ENERGY_ANALYSIS_BUILDING_DATA	
PG_COUPLER_ARRAY	
PG_ENERGY_ANALYSIS_ADVANCED	
PG_RELEASES_MEMBER_FORCES	
PG_SECONDARY_END	
PG_PRIMARY_END	
PG_MOMENTS	
PG_FORCES	
PG_FABRICATION_PRODUCT_DATA	
PG_REFERENCE	
PG_GEOMETRY_POSITIONING	
PG_DIVISION_GEOMETRY	
PG_SEGMENTS_FITTINGS	
PG_CONTINUOUSRAIL_END_TOP_EXTENSION	
PG_CONTINUOUSRAIL_BEGIN_BOTTOM_EXTENSION	
PG_STAIRS_WINDERS	
PG_STAIRS_SUPPORTS	
PG_STAIRS_OPEN_END_CONNECTION	
PG_RAILING_SYSTEM_SECONDARY_FAMILY_HANDRAILS	
PG_TERMINTATION	
PG_STAIRS_TREADS_RISERS	
PG_STAIRS_CALCULATOR_RULES	
PG_SPLIT_PROFILE_DIMENSIONS	
PG_LENGTH	
PG_NODES	
PG_ANALYTICAL_PROPERTIES	
PG_ANALYTICAL_ALIGNMENT	
PG_SYSTEMTYPE_RISEDROP	
PG_LINING	
PG_INSULATION	
PG_OVERALL_LEGEND	
PG_VISIBILITY	
PG_SUPPORT	
PG_RAILING_SYSTEM_SEGMENT_V_GRID	
PG_RAILING_SYSTEM_SEGMENT_U_GRID	
PG_RAILING_SYSTEM_SEGMENT_POSTS	
PG_RAILING_SYSTEM_SEGMENT_PATTERN_REMAINDER	
PG_RAILING_SYSTEM_SEGMENT_PATTERN_REPEAT	
PG_RAILING_SYSTEM_FAMILY_SEGMENT_PATTERN	
PG_RAILING_SYSTEM_FAMILY_HANDRAILS	
PG_RAILING_SYSTEM_FAMILY_TOP_RAIL	
PG_CONCEPTUAL_ENERGY_DATA_BUILDING_SERVICES	
PG_DATA	
PG_ELECTRICAL_CIRCUITING	
PG_GENERAL	
PG_FLEXIBLE	
PG_ENERGY_ANALYSIS_CONCEPTUAL_MODEL	
PG_ENERGY_ANALYSIS_DETAILED_MODEL	
PG_ENERGY_ANALYSIS_DETAILED_AND_CONCEPTUAL_MODELS	
PG_FITTING	
PG_CONCEPTUAL_ENERGY_DATA	
PG_AREA	
PG_ADSK_MODEL_PROPERTIES	
PG_CURTAIN_GRID_V	
PG_CURTAIN_GRID_U	
PG_DISPLAY	
PG_ANALYSIS_RESULTS	
PG_SLAB_SHAPE_EDIT	
PG_LIGHT_PHOTOMETRICS	
PG_PATTERN_APPLICATION	
PG_GREEN_BUILDING	
PG_PROFILE_2	
PG_PROFILE_1	
PG_PROFILE	
PG_TRUSS_FAMILY_BOTTOM_CHORD	
PG_TRUSS_FAMILY_TOP_CHORD	
PG_TRUSS_FAMILY_DIAG_WEB	
PG_TRUSS_FAMILY_VERT_WEB	
PG_TITLE	
PG_FIRE_PROTECTION	
PG_ROTATION_ABOUT	
PG_TRANSLATION_IN	
PG_ANALYTICAL_MODEL	
PG_REBAR_ARRAY	
PG_REBAR_SYSTEM_LAYERS	
PG_CURTAIN_GRID	
PG_CURTAIN_MULLION_2	
PG_CURTAIN_MULLION_HORIZ	
PG_CURTAIN_MULLION_1	
PG_CURTAIN_MULLION_VERT	
PG_CURTAIN_GRID_2	
PG_CURTAIN_GRID_HORIZ	
PG_CURTAIN_GRID_1	
PG_CURTAIN_GRID_VERT	
PG_IFC	
PG_AELECTRICAL	
PG_ENERGY_ANALYSIS	
PG_STRUCTURAL_ANALYSIS	
PG_MECHANICAL_AIRFLOW	
PG_MECHANICAL_LOADS	
PG_ELECTRICAL_LOADS	
PG_ELECTRICAL_LIGHTING	
PG_TEXT	
PG_VIEW_CAMERA	
PG_VIEW_EXTENTS	
PG_PATTERN	
PG_CONSTRAINTS	
PG_PHASING	
PG_MECHANICAL	
PG_STRUCTURAL	
PG_PLUMBING	
PG_ELECTRICAL	
PG_STAIR_STRINGERS	
PG_STAIR_RISERS	
PG_STAIR_TREADS	
PG_UNDERLAY	
PG_MATERIALS	
PG_GRAPHICS	
PG_CONSTRUCTION	
PG_GEOMETRY	
PG_IDENTITY_DATA	
INVALID
"""
"""
# ch??? testing 

def getParameterDefinitions(doc):
	doc = DocumentManager.Instance.CurrentDBDocument
	uiapp = DocumentManager.Instance.CurrentUIApplication
	app = uiapp.Application
	paraDefs = []
	paraDefNames = []
	definition = app.OpenSharedParameterFile()
	#res = definition.Groups.Item["COF"].Name	
	#CASE parameter file has ONLY 1 COF group
	defGSenum = enumerate(definition.Groups.GetEnumerator())
	for defG in defGSenum:
		if defG[1].Name == "COF":
			dg = defG[1]
			des = dg.Definitions
			for de in des:
				#str=de.GUID+spbr+de.Name+spbr+de.ParameterType+spbr+de.ParameterGroups+spbr+de.Visible+spbr+de.Description+spbr+de.UserModifiable+spbr+de.HideWhenNoValue # FAIL ParameterGroups
				paraDefs.append(de)
				paraDefNames.append(de.Name)
	return paraDefs, paraDefNames
def createMultiParameter(doc,paraDefs,cates):
	t = Transaction(doc)
	t.Start("Add Parameter")
	catsenum = enumerate(doc.Settings.Categories.GetEnumerator())
	catset = CategorySet()	
	for cat in catsenum:	
		for cate in cates:
			if cat[1].Name == cate:
				catset.Insert(cat[1])
	for de in paraDefs:
		# Case ALL
		if de.Name.split(spbr)[1] == "GEN" or de.Name.split(spbr)[1] == "CON":
			newIB = InstanceBinding(catset)
			doc.ParameterBindings.Insert(de,newIB,BuiltInParameterGroup.PG_CONSTRUCTION)
			#update by ReInsert
			doc.ParameterBindings.ReInsert(de,newIB,BuiltInParameterGroup.PG_CONSTRUCTION)
	t.Commit()

"""

# SET PARAMETER VALUE
def setParameterValue(doc,elements,paramName,paramValue):
	res = []
	count = 0
	TransactionManager.Instance.EnsureInTransaction(doc)
	wpv.Start()
	for elem in elements:
		try:
			param = elem.LookupParameter(paramName)
			param.Set(paramValue)
			count += 1
		except Exception, ex:
			res.append(ex)
			pass
	res.append(count)
	wpv.Commit()
	TransactionManager.Instance.TransactionTaskDone()
	return res

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def setParameterUniqueId(doc,elements,paramName):
	res = []
	count = 0
	TransactionManager.Instance.EnsureInTransaction(doc)
	for e in elements:
		try:			
			param = e.LookupParameter(paramName)
			param.Set(e.UniqueId)
			count += 1			
		except Exception, ex:
			res.append(ex)
			pass
	res.append(count)
	TransactionManager.Instance.TransactionTaskDone()
	return res

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def nearestDataPoint2(point,listPoints
						,regionLabel
						,levelLabel
						,categoryLabel
						,xLabel
						,yLabel
						,region
						,level
						,category
						,translateLabel
						,targetLabel
						,targetFilterStartWith
						,rotationLabel
						,angleRound
					):
	#point is List of X, Y, Z						
	x = point[0]
	y = point[1]
	listDist = []
	newListPoints=[]
	flag1 = flag2 = flag3 = flag4 = False
	count = 0
	startWiths = targetFilterStartWith.split(",")
	
	# eAngle = angleOfLine(point1, point2,angleRound)
	for dp in listPoints:
		try:
			flag1 = region.lower() in dp.get(regionLabel).lower()
			flag2 = level.lower() in dp.get(levelLabel).lower()
			flag3 = category.lower() in dp.get(categoryLabel).lower()
			for stw in startWiths:
				if stw.lower() in dp.get(targetLabel).lower()[:len(stw)+1]:
					flag4 = True
			#flag4 = targetFilterStartWith.lower() in dp.get(targetLabel).lower()[:len(targetFilterStartWith)]
			if flag1 and flag2 and flag3 and flag4:								
				translate = dp.get(translateLabel)[1:-1].split(" ")
				tX = float(translate[0])
				tY = float(translate[1])
				
				dpX = float(dp.get(xLabel)) - tX
				dpY = float(dp.get(yLabel)) - tY
				
				distance2P = distance(x,dpX,y,dpY)
				listDist.append(distance2P)
				newListPoints.append(dp)
				flag1 = flag2 = flag3 = flag4 = False
		except:
			pass	
	indexMin = len(listDist)
	for i in range(len(listDist)):
		if listDist[i] <= min(listDist):
			indexMin = i	
	#indexMin = i for i in range(len(listDist)) if listDist[i] <= min(listDist)
	return newListPoints[indexMin]
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def distance(x1,x2,y1,y2):
	return ((x1-x2)**2+(y1-y2)**2)**0.5
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def angleOfLine(point1, point2,angleRound):
	x1 = point1[0]
	y1 = point1[1]
	x2 = point2[0]
	y2 = point2[1]

	deltaX = abs(x1-x2)
	deltaY = abs(y1-y2)
	distance = distance(x1,x2,y1,y2)

	cos = deltaY/distance #t??nh tan
	degree = round(math.degrees(math.acos(cos)),angleRound)
	return degree


#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def exe_setup_unit(doc):	
	try:
		TransactionManager.Instance.EnsureInTransaction(doc)
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
		TransactionManager.Instance.TransactionTaskDone()
	except Exception, e:
		pass

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#


def get_all_rel_dirs():

	os.path.curdir
	os.getcwd()	
	os.path.abspath
	os.path.dirname
	sys.path