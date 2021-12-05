import clr, time,os
clr.AddReference("Microsoft.Office.Interop.Excel")
# from System.Runtime.InteropServices import Marshal
import Microsoft.Office.Interop.Excel as Excel
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
def write_excel(excel_path,sheet_name,row,column,data):
	global debugger      
	excel_app = Excel.ApplicationClass()
	excel_app.Visible = show_excel
	workbook = excel_app.Workbooks.Open(excel_path)
	worksheets = workbook.Worksheets
	sheet = [worksheets(i+1) for i in range(worksheets.Count) if worksheets(i+1).Name == sheet_name][0]    
	if data.__class__.__name__ == "str":
		sheet.Cells(row,column).Value = data       
	try:
		workbook.Close(SaveChanges = True,Filename = excel_path)
	except Exception as ex:
		debugger.append(ex)
		pass

def write_excel_2(file_name,dir_path,sheet_name,row,column,data):
	global debugger
	time_ = time.strftime("%y%m%d %H%M%S",time.localtime(time.time()))
	excel_path = "{0}-{1}{2}".format("\\".join([dir_path,file_name]),time_ ,".xlsx")
	
	excel_app = Excel.ApplicationClass()
	excel_app.Visible = show_excel	
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
	# WRITE DATA
	if data.__class__.__name__ == "str":
		sheet.Cells(row,column).Value = data
	if data.__class__.__name__ == "list":
		for d in data:
			if not d.__class__.__name__ == "list":
				sheet.Cells(row + data.index(d),column).Value = c
			else:
				for c in d:
					sheet.Cells(row + data.index(d),column + d.index(c)).Value = d
	if data.__class__.__name__ == "dict":
		keys = sorted(data) #list
		for k in keys:
			r = keys.index(k)
			c = 1
			sheet.Cells(row + r,column).Value = k			
			if data[k].__class__.__name__ in ["str","float"] :
				sheet.Cells(row + r,column + c).Value = data[k]
			# if data[d].__class__.__name__ == "dict":
			# 	sheet.Cells(row + r,column).Value = data[d]	
	
	# save then close
	active_workbook.SaveAs(Filename = excel_path)
	active_workbook.Close()
	excel_app.Quit()
	return 0

def dic_to_list(dic,column_types,col_head_first = "Category"):
	"""
	dic (dict): Từ điển Dữ liệu Ex: {"a":{"D10":10,"D16":16,"D20":20},
									"b":{"D10":11,"D16":17,"D20":21},
									"c":{"D10":12,"D16":18,"D20":22}}
	column_types (list): Danh sách Tên cột  Ex: ["D10","D12","D14","D16","D18"]
	---
	[['Category', 'D10', 'D12', 'D14', 'D16', 'D18']
	['a', 10, 0, 0, 16, 0, 20]
	['b', 11, 0, 0, 17, 0, 21]
	['c', 12, 0, 0, 18, 0, 22]]
	"""
	global time_start,data_name
	try:
		if not dic.__class__.__name__ == "dict": # verify if dic not dict
			raise Exception("Not dict")
		column_types = sorted([str(i) for i in column_types]) # ensure sorted list of strng
		content = []
		content.append(data_name)
		content.append(time_start)

		headers = []
		headers.append(col_head_first)
		headers.extend(column_types)

		content.append(headers)
		keys = sorted(dic)

		dic_text={} # primitive Column head
		for ttt in column_types:
			dic_text[ttt] = 0
		new_dic = {}

		for d in keys:
			try:
				line = []
				line.append(d) # Category
				
				new_d = dic_text.copy()
				new_d.update(dic[d])
				# new_dic[d] = new_d
				line.extend([new_d[w] for w in sorted(new_d)]) # rebar weight ratio / category / type
				content.append(line)
			except:
				pass		
		return content
	except:
		return sorted(dic)

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

dir_path = IN[0]
sheet_name = IN[1]
show_excel = IN[2]
file_name = IN[3]

debugger = []
excel_path = "\\".join([dir_path,file_name]) + ".xlsx"


data1 = [1,2,3,4]
data2 = IN[4]
d = {"a":{"D10":10,"D16":16,"D20":20},
	"b":{"D10":11,"D16":17,"D20":21},
	"c":{"D10":12,"D16":18,"D20":22}}
ct = ["D10","D12","D14","D16","D18"]

OUT = write_excel_2(file_name,dir_path,sheet_name,1,1,dic_to_list(d,ct)),debugger


# if not show_excel:
# 	time.sleep(5)
# 	excel_app.Quit()