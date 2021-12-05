import time

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
	text = ""
	list_ = ["{0}\t{1}".format(d,dic[d]) for d in dic]
	list_.insert(0,time_start)
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
	try:
		list_ = []
		list_.append(data_name)
		list_.append(time_start)
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
		content.append(time_start)
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
	try:
		list_ = []
		list_.append(data_name)
		list_.append(time_start)
		for d in dic:
			item_str = ""
			for c in dic[d]:			
				item_str = "{0}\t{1}".format(c,dic[d][c])
			join_str = "{0}\t{1}".format(d,item_str)			
			list_.append(join_str)			
		return "\n".join(list_)
	except Exception as ex:
		return dic_to_text(dic)


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
#-----------------------------------------------------------------------------------------------#
time_start = time.localtime(time.time())
data_name = ""

d1 = {"a":{"D10":10,"D16":16,"D20":20},
	"b":{"D10":11,"D16":17,"D20":21},
	"c":{"D10":12,"D16":18,"D20":22}}
ct = ["D10","D12","D14","D16","D18"]

d2 = {"D10":10,"D16":16,"D20":20}

d3 = {"a":{"D10":10,"D16":16,"D20":20},
		"b":{"D10":11,"D16":17,"D20":21},
		"c":{"D10":12,"D16":18,"D20":22},
		"d":[1,2,3,4]}
d4 = {"a":{"D10":10,"D16":16,"D20":20},
		"b":{"D10":11,"D16":17,"D20":21},
		"c":{"D10":12,"D16":18,"D20":22}}

d5 = {"a":{"D10":10,"D16":16,"D20":20},
	"b":{"D10":11,"D16":17,"D20":21},
	"c":{"D10":12,"D16":18,"D20":22}}
column_types = ["D10","D12","D14","D16","D18","D20"]

# [print(i) for i in dic_to_list_2(d3)]

[print(i) for i in dic_to_list_4(d1)]