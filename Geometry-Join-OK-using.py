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
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('System.Windows.Forms')
import System.Windows.Forms
from System.Windows.Forms import *

import Autodesk.Revit.DB.JoinGeometryUtils as JGU

##
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()
###################
def UnjoinElementAlready(e,doc,cat):
	res = []
	try:
		joinedElems = getJoinElement(e,doc,cat)
		for ee in joinedElems:
			JGU.UnjoinGeometry(doc,e,ee)
			res.append(ee)
	except Exception, ex:
		res.append(ex)
		pass
	return res


def getJoinElement(e,doc,cat):
	res = []
	try:
		joined = JGU.GetJoinedElements(doc,e)
		for j in joined:
			ee = doc.GetElement(j)
			if ee.Category.Name == cat:
				res.append(ee)
	except Exception, ex:
		res.append(ex)
		pass
	return res
def allElemsOfCat (catName,doc):
	res = []
	cat = []
	for e in doc.Settings.Categories:
	#res.append(e.Name)
		if e.Name == catName.ToString():
			cat = e	
	elems = FilteredElementCollector(doc).OfCategoryId(cat.Id).WhereElementIsNotElementType()	
	for e in elems:
		res.append(e)
	return res

def allElemsIntersectedOfCat(ee,catName,doc):
	res = []
	cat = []
	for e in doc.Settings.Categories:
		if e.Name == catName.ToString():
			cat = e	
	try:
		elems = FilteredElementCollector(doc).OfCategoryId(cat.Id).WherePasses(ElementIntersectsElementFilter(ee))#.WhereElementIsNotElementType()
	except Exception, ex:
		res.append(ex)
		pass
	for eee in elems:
		try:
			res.append(eee)
		except Exception, ex:
			res.append(ex)
			pass
	#joined = getJoinElement(ee, doc,catName)
	#res.Add(joined)
	return res 
  

def allElemsNOTIntersectedOfCat(ee,catName,doc):
	res = []
	cat = []
	for e in doc.Settings.Categories:
	#res.append(e.Name)
		if e.Name == catName.ToString():
			cat = e	
	#elems = FilteredElementCollector(doc).OfCategoryId(cat.Id).WherePasses(ElementIntersectsElementFilter(ee),False)#.WhereElementIsNotElementType()
	elems = getJoinElement(ee,doc,catName)
	for eee in elems:
		if not JGU.IsCuttingElementInJoin(doc, ee, eee):
			res.append(eee)
	return res

def joinTwoElement(a,b):
	try: 
		boolCut = JGU.AreElementsJoined(doc,a,b)
		#JGU.UnjoinGeometry(doc,a,b)
		
		if not boolCut:
			JGU.JoinGeometry(doc,a,b)
		if not JGU.IsCuttingElementInJoin(doc,a,b):
			JGU.SwitchJoinOrder(doc,a,b)
	except :
		pass	
def UNjoinTwoElement(a,b):
	JGU.UnjoinGeometry(doc,a,b)

def joinAllEnableJoinedElemsOfCat(e,cat,doc):
	elems = allElemsIntersectedOfCat(e,cat,doc)
	for el in elems:
		try:
			joinTwoElement(e,el)
		except:
			pass
def UNjoinAllNOTJoinedElemsOfCat(e,cat,doc):
	elems = allElemsNOTIntersectedOfCat(e,cat,doc)
	for el in elems:
		UNjoinTwoElement(e,el)
		
##############
# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
catName1 = IN[0]
catName2 = IN[1]
elem1 = allElemsOfCat(catName1,doc)
elem2 = allElemsOfCat(catName2,doc)

exs=[]
res=[]


with Transaction(doc,"Auto Join") as t:
	t.Start()
	for e1 in elem1:
		try:
			#uj = UnjoinElementAlready(e1,doc,catName2)
			joinAllEnableJoinedElemsOfCat(e1,catName2,doc)		
			
			
			joined = getJoinElement(e1,doc,catName2)
			for j in joined:
				joinTwoElement(e1,j)			
			
			UNjoinAllNOTJoinedElemsOfCat(e1,catName2,doc)
			#res = allElemsIntersectedOfCat(e1,catName2,doc)
		except Exception, ex:
			exs.append(ex)
			pass
 	t.Commit()


#MessageBox.Show('Hello')
# Assign your output to the OUT variable.
OUT = 0