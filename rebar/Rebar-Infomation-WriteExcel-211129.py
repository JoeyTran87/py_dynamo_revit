# Load the Python Standard and DesignScript Libraries
import sys,os
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
def dic_to_list_1(dic,data_name = "Data table name",header = ['Category','Rebar Weight Ratio(kg/m3)']):
	"""
	print (dic_to_text({"D10":10,"D16":16,"D20":20}))
	---
	[['D10','10'],
	['D16','16'],
	['D20','20']]
	print (dic_to_text({"a":{"D10":10,"D16":16,"D20":20},
		"b":{"D10":11,"D16":17,"D20":21},
		"c":{"D10":12,"D16":18,"D20":22},
		"d":[1,2,3,4]}))
	---
	[['a','{'D10': 10, 'D16': 16, 'D20': 20}'],
	['b','{'D10': 11, 'D16': 17, 'D20': 21}'],
	[c','{'D10': 12, 'D16': 18, 'D20': 22}'],
	['d','[1, 2, 3, 4]']]
	"""
	global time_start
	time_ = time.strftime("%d-%m-%y %H:%M:%S",time_start)
	list_ = []
	list_.append(data_name)
	list_.append(time_)
	list_.append(header)
	list_.extend([[d,dic[d]] for d in dic])
	return list_

def dic_to_list_2(dic,data_name = "Data table name",header = ['Category','Rebar Weight Ratio(kg/m3)']):
	"""
	{"a":{"D10":10,"D16":16,"D20":20},
		"b":{"D10":11,"D16":17,"D20":21},
		"c":{"D10":12,"D16":18,"D20":22}}
	---
	[['a','10','16','20'],
	['b','11','17','21'],
	['c','12','18','22']]
	"""
	global time_start
	try:
		time_ = time.strftime("%d-%m-%y %H:%M:%S",time_start)
		list_ = []
		list_.append(data_name)
		list_.append(time_)
		list_.append(header)
		for d in dic:
			l_ = []
			l_.append(str(d))
			l_.extend([str(dic[d][c]) for c in dic[d]])
			list_.append(l_)
		return list_
	except:
		return dic_to_list_1(dic,data_name=data_name)

def dic_to_list_3(dic,column_types,data_name = "Rebar Weight Ratio(kg/m3) / Category / Rebar Type",header = ['Category']):
	"""
	dic (dict): Từ điển Dữ liệu Ex: {"a":{"D10":10,"D16":16,"D20":20},
									"b":{"D10":11,"D16":17,"D20":21},
									"c":{"D10":12,"D16":18,"D20":22}}
	column_types (list): Danh sách Tên cột  Ex: ["D10","D12","D14","D16","D18","D20"]
	---
	[['Category', 'D10', 'D12', 'D14', 'D16', 'D18', 'D20'],
	['a', 10, 0, 0, 16, 0, 20],
	['b', 11, 0, 0, 17, 0, 21],
	['c', 12, 0, 0, 18, 0, 22]]
	"""
	global time_start
	try:
		time_ = time.strftime("%d-%m-%y %H:%M:%S",time_start)
		dic_text={} # primitive Column head
		for ttt in column_types:
			dic_text[ttt] = 0
		new_dic = {}

		for d in dic:
			new_dic[d] = {}
			new_d = dic_text.copy()
			new_d.update(dic[d])
			new_dic[d] = new_d
		
		header.extend([tt for tt in column_types])
		content = []

		content.append(data_name)
		content.append(time_)
		content.append(header)

		for d in new_dic:
			line = []
			line.append(d)
			line.extend([new_dic[d][c] for c in column_types])
			content.append(line)
		
		return content
	except:
		return dic_to_list_1(dic,data_name=data_name)
def dic_to_list_4(dic,data_name = "Data table name",header = ['Category','Rebar Weight Ratio(kg/m3)/ Category / Rebar Type']):
	"""
	{"a":{"D10":10,"D16":16,"D20":20},
		"b":{"D10":11,"D16":17,"D20":21},
		"c":{"D10":12,"D16":18,"D20":22}}
	---
	[['a','10','16','20'],
	['b','11','17','21'],
	['c','12','18','22']]
	"""
	global time_start
	try:
		time_ = time.strftime("%d-%m-%y %H:%M:%S",time_start)
		list_ = []
		list_.append(data_name)
		list_.append(time_)
		list_.append(header)
		for d in dic:
			l_ = []
			l_.append(str(d))
			if dic[d].__class__.__name__ == "dict":
				ll_ = []
				for c in dic[d]:
					ll_.append(c)
					ll_.append(dic[d][c])
				l_.extend(ll_)
			else:
				l_.extend([str(dic[d][c]) for c in dic[d]])
			list_.append(l_)
		return list_
	except:
		return dic_to_list_1(dic,data_name=data_name)

def write_excel_2(file_name,dir_path,excel_app,active_workbook,sheet_name,row,column,data,save = False):
	"""data = single list"""

	global debugger
	
	if excel_app == None or active_workbook == None:
		excel_path = "{0}{1}".format("\\".join([dir_path,file_name]),".xlsx")	
		excel_app = Excel.ApplicationClass()
		excel_app.Visible = True	
		active_workbook = excel_app.ActiveWorkbook
		if active_workbook == None:
			excel_app.Workbooks.Add()
			active_workbook = excel_app.ActiveWorkbook
		worksheets = active_workbook.Worksheets
	
	if not sheet_name in [worksheets(i+1).Name for i in range(worksheets.Count)]:
		sheet = worksheets.Add()
		sheet.Name = sheet_name
	else:
		sheet = [worksheets(i+1) for i in range(worksheets.Count) if worksheets(i+1).Name == sheet_name][0]
	
	if data.__class__.__name__ == "list":
		for d in data:
			if d.__class__.__name__ == "list":
				for c in d:
					sheet.Cells(row + data.index(d),column + d.index(c)).Value = c
			else:
				sheet.Cells(row + data.index(d),column).Value = str(d)
	if save:
		active_workbook.SaveAs(Filename = excel_path)
		active_workbook.Close()
		excel_app.Quit()


def write_excel_3(file_name,dir_path,sheet_names,row,column,datas):
	"""datas : list[list]"""
	global debugger
	excel_path = "{0}{1}".format("\\".join([dir_path,file_name]),".xlsx")	
	excel_app = Excel.ApplicationClass()
	excel_app.Visible = True	
	active_workbook = excel_app.ActiveWorkbook
	if active_workbook == None:
		excel_app.Workbooks.Add()
		active_workbook = excel_app.ActiveWorkbook
	worksheets = active_workbook.Worksheets
	# WRITE DATA
	if len(datas) == len(sheet_names):
		for data in datas:
			try:
				sheet_name = sheet_names[datas.index(data)]
				# write_excel_2(file_name,dir_path,excel_app,active_workbook,sheet_name,row,column,data,save = False)
				if not sheet_name in [worksheets(i+1).Name for i in range(worksheets.Count)]:
					sheet = worksheets.Add()
					sheet.Name = sheet_name
				else:
					sheet = [worksheets(i+1) for i in range(worksheets.Count) if worksheets(i+1).Name == sheet_name][0]
				if data.__class__.__name__ == "list":
					for d in data:
						if d.__class__.__name__ == "list":
							for c in d:
								sheet.Cells(row + data.index(d),column + d.index(c)).Value = c
						else:
							sheet.Cells(row + data.index(d),column).Value = str(d)
			except:
				pass
		active_workbook.SaveAs(Filename = excel_path)
		active_workbook.Close()
		excel_app.Quit()
	return 0

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
dataEnteringNode = IN
view_name = IN[0]
data = [dictionary_to_dict(dic) for dic in IN[1]] # data = list[dict]
rb_data = IN[2][1:]
sheet_names = IN[3] # list[str] sheet Name
time_start = tuple(IN[4])#time.strftime("%y%m%d %H%M%S",time.strptime(IN[4],"%d-%m-%y %H:%M:%S"))#time.strftime("%d-%m-%y %H:%M:%S",time.localtime(time.time()))
data_names = IN[5]
#-------------------------------------------------------#
time_s = time.strftime("%y%m%d %H%M%S",time_start)
rb_types = ["D{:0.0f}".format(dat[0]) for dat in rb_data]

rvt_dir, rvt_file = revitDir(doc)
file_name = rvt_file +"-"+view_name+"-"+time_s
dir_path = rvt_dir[:-1]

if len(data) == len(sheet_names) == len(data_names):
	datas = []
	data_name = data_names[0]
	datas.append(dic_to_list_1(data[0],data_name = data_names[0]))
	
	datas.append(dic_to_list_3(data[1],column_types = rb_types,data_name = data_names[1]))
	
	datas.append(dic_to_list_4(data[2],data_name = data_names[2]))

	write_excel_3(file_name,dir_path,sheet_names,1,1,datas)


OUT = file_name,dir_path,sheet_names,datas
