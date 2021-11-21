dic = {	"a":{"d10":10,"d16":16,"d20":20},
		"b":{"d10":11,"d16":17,"d20":21},
		"c":{"d10":12,"d16":18,"d20":22}}

for d in dic:
	print(d)
	# print(dic[d])
	# for dd in dic[d]:
	# 	print (dd,dic[d][dd],sep=" ")
	print(";".join([str(dd) for dd in dic[d]]))
	print(";".join([str(dic[d][dd]) for dd in dic[d]]))