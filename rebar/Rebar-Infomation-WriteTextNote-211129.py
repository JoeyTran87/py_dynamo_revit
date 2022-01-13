# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
import Autodesk.DesignScript.Geometry.Point as pt
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import TaskDialog
clr.AddReference("RevitNodes")
import Revit
import Revit.Elements.TextNote as tn
clr.ImportExtensions(Revit.Elements)
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *

import Autodesk.Revit.DB.JoinGeometryUtils as JGU

import time
clr.AddReference("Microsoft.Office.Interop.Excel")
import Microsoft.Office.Interop.Excel as Excel
#-------------------------------------------------------#
def get_sheet_view_by_search_string(search_string):
	global doc    
	viewCollector = list(FilteredElementCollector(doc).OfClass(ViewSheet))
	try:
		view_  = [v for v in viewCollector if search_string in v.Name][0]
		return view_
	except:
		return

def get_sheet_view (view_name):
	""""""
	global doc#, debugger
	view_sheet = get_sheet_view_by_search_string(view_name)
	if view_sheet == None:
		try:
			# Get an available title block from document
			collector = list(FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_TitleBlocks))
			fs = collector[0]#.FirstElement()		
			TransactionManager.Instance.EnsureInTransaction(doc)	
			view_sheet = ViewSheet.Create(doc,fs.Id)
			try:
				view_sheet.SheetNumber = "000"
			except:
				view_sheet.SheetNumber = "000000000000"
			view_sheet.Name = view_name
			# Delete Title Block
			title_blocks = list(FilteredElementCollector(doc,view_sheet.Id).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().ToElements())
			[doc.Delete(t.Id) for t in title_blocks]
			TransactionManager.Instance.TransactionTaskDone()
		except Exception as ex:
			# debugger.append(ex)
			pass
	return view_sheet

def write_text_note(viewId,position,text,typeId):
	""""""
	global doc
	if doc.GetElement(viewId) == None:
		viewId = doc.ActiveView.Id
	if position == None:
		position = XYZ()
	if typeId ==  None or doc.GetElement(typeId) == None or not doc.GetElement(typeId).__class__ == TextNoteType:
		typeId = list(FilteredElementCollector(doc).OfClass(TextNoteType).WhereElementIsElementType())[0].Id
	
	TransactionManager.Instance.EnsureInTransaction(doc)

	text_note = TextNote.Create(doc,viewId,position,text,typeId = typeId)

	TransactionManager.Instance.TransactionTaskDone()
	return text_note
	
def dic_to_text(dic):
	"""
	print (dic_to_text({"D10":10,"D16":16,"D20":20}))
	---
	D10     10
	D16     16
	D20     20
	print (dic_to_text({"a":{"D10":10,"D16":16,"D20":20},
		"b":{"D10":11,"D16":17,"D20":21},
		"c":{"D10":12,"D16":18,"D20":22},
		"d":[1,2,3,4]}))
	---
	a       {'D10': 10, 'D16': 16, 'D20': 20}
	b       {'D10': 11, 'D16': 17, 'D20': 21}
	c       {'D10': 12, 'D16': 18, 'D20': 22}
	d       [1, 2, 3, 4]
	"""
	global time_start,data_name
	time_ = time.strftime("%d-%m-%y %H:%M:%S",time_start)
	text = ""
	list_ = ["{0}\t{1}".format(d,dic[d]) for d in dic]
	list_.insert(0,time_)
	list_.insert(0,data_name)
	text = "\n".join(list_)
	return text


def dic_to_text_2(dic):
	"""
	{"a":{"D10":10,"D16":16,"D20":20},
		"b":{"D10":11,"D16":17,"D20":21},
		"c":{"D10":12,"D16":18,"D20":22}}
	---
	a       10      16      20
	b       11      17      21
	c       12      18      22
	"""
	global time_start,data_name
	time_ = time.strftime("%d-%m-%y %H:%M:%S",time_start)
	try:
		list_ = []
		list_.append(data_name)
		list_.append(time_)
		for d in dic:
			l_ = []
			l_.append(str(d))
			l_.extend([str(dic[d][c]) for c in dic[d]])
			list_.append("\t".join(l_))
		return "\n".join(list_)
	except:
		return dic_to_text(dic)



def dic_to_text_3(dic,column_types,col_head_first = "Category"):
	"""
	dic (dict): Từ điển Dữ liệu Ex: {"a":{"D10":10,"D16":16,"D20":20},
									"b":{"D10":11,"D16":17,"D20":21},
									"c":{"D10":12,"D16":18,"D20":22}}
	column_types (list): Danh sách Tên cột  Ex: ["D10","D12","D14","D16","D18"]
	---
	Category        D10     D12     D14     D16     D18
	a       10      0       0       16      0       20
	b       11      0       0       17      0       21
	c       12      0       0       18      0       22
	"""
	global time_start,data_name
	time_ = time.strftime("%d-%m-%y %H:%M:%S",time_start)
	try:
		dic_text={} # primitive Column head
		for ttt in column_types:
			dic_text[ttt] = 0
		new_dic = {}

		for d in dic:
			new_dic[d] = {}
			new_d = dic_text.copy()
			new_d.update(dic[d])
			new_dic[d] = new_d
		headers = "{0}\t{1}".format(col_head_first,"\t".join([tt for tt in column_types]))
		content = []
		content.append(data_name)
		content.append(time_)
		content.append(headers)

		for d in new_dic:
			content.append("{}\t{}".format(d,"\t".join([str(new_dic[d][dd]) for dd in new_dic[d]])))
		text = "\n".join(content)
		return text
	except:
		return dic_to_text(dic)

def dic_to_text_4(dic):
	"""
	{"a":{"D10;D11":"10;12"},
		"b":{"D10;D11":"11;12"},
		"c":{"D10;D11":"12;12"}}
	---
	a       D10;D11      10;12
	b       D10;D11      11;12
	c       D10;D11      12;12
	"""
	global time_start,data_name,debugger
	time_ = time.strftime("%d-%m-%y %H:%M:%S",time_start)
	try:
		list_ = []
		list_.append(data_name)
		list_.append(time_)
		for d in dic:
			item_str = ""
			for c in dic[d]:			
				item_str = "{0}\t{1}".format(c,dic[d][c])
			join_str = "{0}\t{1}".format(d,item_str)			
			list_.append(join_str)			
		return "\n".join(list_)
	except Exception as ex:
		return dic_to_text(dic)

def dictionary_to_dict(dic):
	"""Use for converting Dynamo Dictionary to Python dict
	Apply for {'key':{'key':{}}}
	"""	
	if dic.__class__.__name__ == "Dictionary[object, object]":
		dic = dict(dic)		
	try:
		for d in dic:			
			if dic[d].__class__.__name__ == "Dictionary[object, object]":
				dic[d] = dict(dic[d])
			try:
				for c in dic[d]:
					if dic[d][c].__class__.__name__ == "Dictionary[object, object]":
						dic[d][c] = dict(dic[d][c])
			except:
				pass
	except:
		pass
	return dic

def revitDir(doc):
	"""
	dir : directory
	file_name : Revit file name
	"""
	dir = ""
	try:
		p = doc.PathName.split("\\")
		pp = p[0:len(p)-1]	
		for s in pp:
			dir += s + "\\"
		file_name = doc.PathName.split("\\")[-1].split(".rvt")[0]	
	except:
		pass
	return dir,file_name

#-------------------------------------------------------#
#-------------------------------------------------------#
#-------------------------------------------------------#
dataEnteringNode = IN
debugger = []
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()
#-------------------------------------------------------#
view_name = IN[0]
data = dictionary_to_dict(IN[1])
rb_data = IN[2][1:]
y = float(IN[3])/304.8
data_name = IN[4]
mode = int(IN[5])
#-------------------------------------------------------#
time_start = tuple(IN[6])
time_s = time.strftime("%y%m%d %H%M%S",time_start)
rb_types = ["D{:0.0f}".format(dat[0]) for dat in rb_data]


viewId = get_sheet_view (view_name).Id
if mode == 1:
	text = dic_to_text(data)
if mode == 2:
	text = dic_to_text_2(data)
if mode == 3:
	text = dic_to_text_3(data,rb_types)
if mode == 4:
	text = dic_to_text_4(data)

text_note = write_text_note(viewId,XYZ(0,y,0),text,None)
if text_note:
	OUT = data
else:
	OUT = "FAIL"