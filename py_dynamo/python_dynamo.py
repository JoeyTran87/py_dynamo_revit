import clr
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
revitDir = r"C:\Program Files\Autodesk\Revit 2020"
sys.path.append(revitDir)
revitDynamoDir1 = r"C:\Program Files\Autodesk\Revit 2020\AddIns\DynamoForRevit\Revit"
revitDynamoDir2 = r"C:\Program Files\Autodesk\Revit 2020\AddIns\DynamoForRevit"
sys.path.append(revitDynamoDir1)
sys.path.append(revitDynamoDir2)
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB.JoinGeometryUtils as JGU
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#



#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def splitDynString(cates):	
	newcats = []
	if cates:
		cateLines = cates.split("\n")
		# if len(cateLines)==2:
		# 	newcats.append(cates[:-2])
		if len(cateLines)>=2:
			for cat in cateLines[:-1]:
				if len(cat[:-1])>0:
					newcats.append(cat[:-1])	
			if len(cateLines[-1])>0:
				newcats.append(cateLines[-1])
		else:
			if len(cates)>0:
				newcats.append(cates)
	return newcats
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#

def getAllCategoryElementsInfoDictionary(doc,cates):
	res = []
	elems = getAllElementsOfCategories(splitDynString(cates),doc)
	for e in elems:
		try:
			res.append(getPropertiesDic(e,doc))
		except:
			pass
	return res
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#

def getAllElementsOfCategories(cates,doc):
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

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
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