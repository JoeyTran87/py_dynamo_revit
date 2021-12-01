dic = {"a":{"D10":10,"D16":16,"D20":20},
		"b":{"D10":11,"D16":17,"D20":21},
		"c":{"D10":12,"D16":18,"D20":22}}


d1 = {"D10":10,"D16":16,"D20":20}
d2 = {"D10":0,"D11":0,"D12":0,"D13":0,"D14":0,"D15":0,"D16":0,"D17":0,"D18":0,"D19":0,"D20":0}
d2.update(d1)
# print (d2)


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
	text = ""
	text = "\n".join(["{0}\t{1}".format(d,dic[d]) for d in dic])
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
	flag = [dic[d].__class__.__name__ for d in dic].count("dict") == len(dic)
	if not flag:
		return dic_to_text(dic)
	list_ = []
	for d in dic:
		l_ = []
		l_.append(str(d))
		l_.extend([str(dic[d][c]) for c in dic[d]])
		list_.append("\t".join(l_))
	return "\n".join(list_)

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
	flag = [dic[d].__class__.__name__ for d in dic].count("dict") == len(dic)
	if not flag:
		return dic_to_text(dic)

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
	content.append(headers)
	
	for d in new_dic:
		content.append("{}\t{}".format(d,"\t".join([str(new_dic[d][dd]) for dd in new_dic[d]])))
	text = "\n".join(content)
	return text

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
	try:
		list_ = []
		for d in dic:
			item_str = ""			
			for c in dic[d]:			
				item_str = "{0}\t{1}".format(str(c),str(dic[d][c]))			
			join_str = "{0}\t{1}".format(str(d),item_str)			
			list_.append(join_str)
			
		return "\n".join(list_)
	except Exception as ex:
		return dic_to_text(dic)


# column_types = ["D10","D12","D14","D16","D18"]
# print (dic_to_text_3(dic,column_types))


d4 = 	{"a":{"D10;D11":"10;12"},
		"b":{"D10;D11":"11;12"},
		"c":{}}
# print(dic_to_text_4(d4))

d5 = {"Walls"	:{},
"Structural Framing"	:{'D8;D10;D12;D16;D25;D28' : '7.8;26.033;139.579;14.662;226.598;187.309'},
"Parts"	:{'':''},
"Floors"	:{'D10' : '109.119'},
"Structural Foundations"	:{'D10;D12;D8' : '2.169;5.279;0.438'},
"Structural Columns"	:{'D16;D8' : '100.331;34.05'}}
# print(dic_to_text_4(d5))
print(d4.__class__.__name__)
