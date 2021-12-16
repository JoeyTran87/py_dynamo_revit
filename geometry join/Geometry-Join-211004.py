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
def clean_joined_not_intersect(doc,JGU):
	global debugger
	warnings = list(doc.GetWarnings())
	for w in warnings:
		try:
			if w.GetDescriptionText() == "Highlighted elements are joined but do not intersect.":
				id_pairs = []
				id_pairs.append(list(w.GetFailingElements()))		
				[JGU.UnjoinGeometry(doc,doc.GetElement(p[0]),doc.GetElement(p[1])) for p in id_pairs]
		except Exception as ex:
			debugger.append("warnings:{0}".format(ex))
			pass

def autojoin(doc,JGU,element,cates):
	global debugger,count,dic_rule,rule_cates,categories,categories_name,collector
	
	intersect_elements = []
	intersect_elements.extend([e for e in collector.WherePasses(ElementIntersectsElementFilter(element)) if e.Category.Name in cates])
	
	joined_elements = []
	joined_elements = [doc.GetElement(i) for i in JGU.GetJoinedElements(doc,element) if doc.GetElement(i).Category.Name in cates]
			
	flag_result = [False]
	for ie in intersect_elements:
		try:
			if ie.Category.Name in dic_rule[element.Category.Name]:
				JGU.JoinGeometry(doc,element,ie)
			elif ie.Category.Name in cates:
				JGU.JoinGeometry(doc,ie,element)
			else:
				pass
		except Exception as ex:
			debugger.append("intersect_elements:{0}".format(ex))
			pass
	
	for je in joined_elements:
		try:
			if je.Category.Name in dic_rule[element.Category.Name]:
				flag_result.append (True)
				# function Check whether A w B Join follow Rule
				is_correct_rule = JGU.IsCuttingElementInJoin(doc,element,je)
				if is_correct_rule == "True":
					pass
				else:
					JGU.SwitchJoinOrder(doc,element,je)
			else:
				flag_result.append (False)
				# function Check whether A w B Join follow Rule --> Switch Joint ????????
		except Exception as ex:
			debugger.append("joined_elements:{0}".format(ex))
			pass
			
	count += 1	
	

time_start = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))
debugger = []

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
elements = UnwrapElement(IN[0])
cates = IN[1].splitlines()

cate_name_copy = cates[:]
dic_rule = {}
while True:    
    dic_rule[cate_name_copy[0]] = cate_name_copy[1:]
    cate_name_copy.remove(cate_name_copy[0])
    if len(cate_name_copy) == 1:
        break
count = 0
#start
TransactionManager.Instance.EnsureInTransaction(doc)

collector = FilteredElementCollector(doc)	
categories = list(doc.Settings.Categories)
categories_name = [cat.Name for cat in categories]
rule_cates = [categories[categories_name.index(c)] for c in cates if c in categories_name]
# clean
clean_joined_not_intersect(doc,JGU)
#process
for element in elements:
	try:
		if element.Category.Name != cates[-1]:
			autojoin(doc,JGU,element,cates)		
	except Exception as ex:
		debugger.append("clean_joined_not_intersect:{0}".format(ex))
		pass
TransactionManager.Instance.TransactionTaskDone()
#end
time_end = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))

OUT = dic_rule,"{0}/{1} Succeeded".format(count,len(elements)),time_start, time_end, debugger