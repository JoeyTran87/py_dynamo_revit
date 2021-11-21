# Load the Python Standard and DesignScript Libraries
import os, sys, json,clr, tempfile,shutil
from shutil import copyfile
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *
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
time_start = time.strftime("%y%m%d %H:%M:%S",time.localtime(time.time()))
debugger = []

#----------------------------------------------------------------#
#----------------------------------------------------------------#
#----------------------------------------------------------------#
#----------------------------------------------------------------#
#----------------------------------------------------------------#
#----------------------------------------------------------------#
def setupUnit(doc):	
	try:
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
		#doc.GetUnits().SetFormatOptions(UnitType.UT_Area,fmOp)
	except Exception as ex:
		pass

#----------------------------------------------------------------#
#----------------------------------------------------------------#

def set_dic(selection):
	elem_dic = {}
	for e in selection:
		try:
			elem_dic[str(e.Id)] = []
			elem_dic[str(e.Id)].append(e)
		except:
			pass
	return elem_dic

#----------------------------------------------------------------#
#----------------------------------------------------------------#
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
#----------------------------------------------------------------#
#----------------------------------------------------------------#
def getAllElementsOfCategories(doc,cates):
	global debugger,categories,category_names
	elements = []
	for cat in cates:
		try:
			if cat in category_names:
				c = categories[int(category_names.index(cat))]				
				elements.extend( [e for e in FilteredElementCollector(doc).OfCategoryId(c.Id).WhereElementIsNotElementType().ToElements()])
		except Exception as ex:
			debugger.append(ex)
			pass
	return elements

def getAllElementsOfCategory(doc,cat):
	global debugger,categories,category_names
	elements = []
	if cat in category_names:
		c = categories[int(category_names.index(cat))]				
		elements.extend( [e for e in FilteredElementCollector(doc).OfCategoryId(c.Id).WhereElementIsNotElementType().ToElements()])
	return elements
#----------------------------------------------------------------#
#----------------------------------------------------------------#
def get_rebar(e):
	# ALL REBAR IN MODEL
	# CHECK IF HOST REBAR
	elem_host_rebar = []
	try:
		rbhd = RebarHostData.GetRebarHostData(e)
		rebars = list(rbhd.GetRebarsInHost())
		if rebars:
			elem_host_rebar.extend(rebars)
	except Exception as ex:
		# elem_host_rebar.append(ex)
		pass
	return elem_host_rebar

def get_rebar_and_host(e):
	# ALL REBAR IN MODEL
	# CHECK IF HOST REBAR
	global doc
	elem_host_rebar = []
	try:
		rbhd = RebarHostData.GetRebarHostData(e)
		rebars = list(rbhd.GetRebarsInHost())
		if rebars:
			elem_host_rebar.extend(rebars)
	except Exception as ex:
		elem_host_rebar.append(ex)
		pass
	return e, elem_host_rebar

def rebar_in_system(floor):
	global doc,debugger
	rebars = []
	floor_id = floor.Id
	rebar_collector = []
	rebar_collector.extend(list(FilteredElementCollector(doc).OfClass(RebarInSystem).ToElements()))
	# rebar_collector.extend(list(FilteredElementCollector(doc).OfClass(Rebar).ToElements()))
	for r in rebar_collector:
		try:
			if r.GetHostId() == floor_id:
				rebars.append(r)
		except:
			pass		
	return rebars


def get_rebar_dic(e):
	"""
	[0] e : Đối tượng chứa Rebar
	[1] rebar_list :  Danh sách Rebar
	[2] rb_dic_volume : Dictionary Rebar: Volume
	[3] rb_dic_weight : Dictionary Rebar: Weight
	[4] rb_dic_length : Dictionary Rebar: Length"""
	# ALL REBAR IN MODEL
	# CHECK IF HOST REBAR
	global doc,debugger
	rebar_list = []
	try:
		rbhd = RebarHostData.GetRebarHostData(e)
		rebars = list(rbhd.GetRebarsInHost())
		debugger.append(rebars)
		if len(rebars)>0:
			rebar_list.extend(rebars)
		# RebarInSystem
		rebar_list.extend(rebar_in_system(e))
	except Exception as ex:
		debugger.append(ex)
		pass	
	rb_dic_volume = {}
	rb_dic_weight = {}
	rb_dic_length = {}

	for r in rebar_list:
		try:
			key = "D{:0.0f}".format(round(doc.GetElement(r.GetTypeId()).BarDiameter*304.8))
			# VOLUME
			if not key in rb_dic_volume.Keys:
				rb_dic_volume[key] = r.Volume*28316.8 # cubic feet to cubic centimet
			else:
				rb_dic_volume[key] += r.Volume*28316.8
			# WEIGHT
			if not key in rb_dic_weight:
				rb_dic_weight[key] = rebar_weight(r,rb_type = key)
			else:
				rb_dic_weight[key] += rebar_weight(r,rb_type = key)	
			# LENGTH
			if not key in rb_dic_length:
				rb_dic_length[key] = r.LookupParameter("Total Bar Length").AsDouble()*0.3048 # unit Meter
			else:
				rb_dic_length[key] += r.LookupParameter("Total Bar Length").AsDouble()*0.3048				
		except Exception as ex:
			debugger.append(ex)
			pass
	
	return e, rebar_list,rb_dic_volume,rb_dic_weight,rb_dic_length

def rebar_retriver(cates,rounding = 6):	
	"""cat_dic_rebar_ratio : Hàm lượng thép KG / M3 / Category
	cat_dic_rebar_type_ratio : Hàm lượng thép KG / M3 / Category / Rebar Type
	cat_dic_rebar_volume : Khối tích thép M3 / Category
	cat_dic_rebar_weight : Trọng lượng thép KG / Category/ Rebar Type"""
	global doc,debugger
	cat_dic_rebar_ratio = {} #dictionary rebar ratio{"Category": 10.02} kg/m3
	cat_dic_rebar_type_ratio = {} #dictionary rebar type ratio {"Category": {"D10":12,"D16":15}} kg/m3
	cat_dic_rebar_volume = {} # dictionnay rebar volume ex: {"Category": {"D 16": 1.2,"D 20": 2.3}} m3
	cat_dic_rebar_type_weight = {} # dictionnay rebar weight ex: {"Category": {"D 16": 25,"D 20": 30}} kg
	
	for cate in cates:
		cat_dic_rebar_ratio [cate] = 0
		cat_dic_rebar_volume[cate] = {} # ini dictionary of Category ex: {"Category":{}}
		cat_dic_rebar_type_weight[cate] = {}
		try:
			elements = getAllElementsOfCategory(doc,cate)
			volume_concrete_sum = 0
			rebars = [] # List of rebars
			rebars_volume_dics = [] # List of Dictionary for Rebar  volume
			rebars_weight_dics = [] # List of Dictionary for Rebar  Weight			
			for e in elements:
				try:
					rebar_host = get_rebar_dic(e)
					if len(rebar_host[1]) > 0:
						# rebars.extend(rebar_host[1])
						rebars_volume_dics.append(rebar_host[2])
						rebars_weight_dics.append(rebar_host[3])
						debugger.append("here")
						try:
							volume_concrete_sum += rebar_host[0].LookupParameter("Volume").AsDouble()
						except:
							pass
				except Exception as ex:
					pass
			debugger.append("here")
			# tính hàm lượng thép KG / M3 / Category
			# volume_rebar_sum = sum([r.Volume for r in rebars])
			weight_rebar_sum = sum([rebars_weight_dics[d] for d in rebars_weight_dics])
			cat_dic_rebar_ratio [cate] = round(weight_rebar_sum/volume_concrete_sum,rounding)
											
			
			for dic in rebars_volume_dics:				
				for d in dic:
					if not d in cat_dic_rebar_volume[cate].Keys:
						cat_dic_rebar_volume[cate][d] = dic[d]
					else:
						cat_dic_rebar_volume[cate][d] += dic[d]
			
			for dic in rebars_weight_dics:				
				for d in dic:
					if not d in cat_dic_rebar_type_weight[cate].Keys:
						cat_dic_rebar_type_weight[cate][d] = dic[d]
					else:
						cat_dic_rebar_type_weight[cate][d] += dic[d]
		

			for cate in cat_dic_rebar_type_weight:
				if not cate in cat_dic_rebar_type_weight.Keys:
					cat_dic_rebar_type_weight[cate] = {}
				for d in cat_dic_rebar_type_weight[cate]:
					try:
						if not d in cat_dic_rebar_type_weight[cate].Keys:
							cat_dic_rebar_type_weight[cate][d] = 0
						cat_dic_rebar_type_weight[cate][d] = cat_dic_rebar_type_weight[cate][d]/volume_concrete_sum
					except:
						pass

		
		except Exception as ex:
			# debugger.append(ex)
			pass
	return cat_dic_rebar_ratio,cat_dic_rebar_type_weight,cat_dic_rebar_volume,cat_dic_rebar_type_weight

def rebar_weight(e,rb_type = None):
	"""Trả về Khối lượng (Kg) Thép"""
	global rb_dic_WPL
	if e.__class__.__name__ == "Rebar" or e.__class__.__name__ == "RebarInSystem":
		if rb_type == None:
			rb_type = "D{:0.0f}".format(round(doc.GetElement(e.GetTypeId()).BarDiameter*304.8))
		# rn_quantity = e.Quantity
		# rb_each_bar_length = round(e.LookupParameter("Bar Length").AsDouble()*304.8)
		rb_total_bar_length = round(e.LookupParameter("Total Bar Length").AsDouble()*304.8)
		rb_total_weight = (rb_total_bar_length/1000)*rb_dic_WPL[rb_type]
		# debugger.append("Type: {}".format(rb_type))
		# debugger.append("Quantity: {}".format(rn_quantity))
		# debugger.append("Each Bar Length: {:0.0f} mm".format(rb_each_bar_length))
		# debugger.append("Total Bar Length: {:0.0f} mm".format(rb_total_bar_length))
		# debugger.append("Total Bar Weight: {:0.0f} kg".format(rb_total_weight))
		return rb_total_weight
def rebar_ratio(cates,rounding = 6):
	"""OUTS:
	[0] dic_cate_elements:	Dictionary Category (Body Concrete) Elements
	[1] dic_cate_volume:	Dictionary Category Volume (m3)
	[2] dic_cate_rebars:	Dictionary Category (Rebar)elements
	[3] dic_cate_rebars_volume:	Dictionary Category Rebar Volume (cm3)
	[4] dic_cate_rebars_weight:	Dictionary Category Rebar Weight (Kg)
	[5] dic_cate_rebars_weight_per_type:	Dictionary Category Rebar Weight per Type (Kg)(/Category/Type)
	[6] dic_cate_rebars_weight_ratio:	Dictionary Category Rebar Weight Ratio (kg/m3)(/Category)
	[7] dic_cate_rebars_weight_ratio_per_type:	Dictionary Category Elements (kg/m3)(/Category/Type)
	[8] dic_cate_rebars_length:	Dictionary Category Rebar Length (m)(/Category)
	[9] dic_cate_rebars_length_per_type:	Dictionary Category Rebar Length Per Type (m)(/Category/Type)"""
	global doc,debugger

	# OUT var

	dic_cate_elements = {}
	dic_cate_volume = {}
	dic_cate_rebars = {}
	dic_cate_rebars_volume = {}
	dic_cate_rebars_weight = {}
	dic_cate_rebars_weight_ratio = {}

	dic_cate_rebars_weight_per_type = {}
	dic_cate_rebars_weight_ratio_per_type = {}

	dic_cate_rebars_length = {}
	dic_cate_rebars_length_per_type = {}
	
	dic_cate_rebars_weight_ratio_per_type_combine = {}

	for cate in cates:
		elements = []

		dic_cate_elements[cate] = []
		dic_cate_volume[cate] = 0
		dic_cate_rebars[cate] = []
		dic_cate_rebars_volume[cate] = 0
		dic_cate_rebars_weight[cate] = 0
		dic_cate_rebars_weight_ratio[cate] = 0

		dic_cate_rebars_weight_per_type[cate] = {}
		dic_cate_rebars_weight_ratio_per_type[cate] = {}
		
		dic_cate_rebars_length[cate] = 0
		dic_cate_rebars_length_per_type[cate] = {}

		try:
			elements = getAllElementsOfCategory(doc,cate)			
		except:
			break
		for e in elements:
			try:
				rebars = get_rebar_dic(e)
				if len(rebars[1]) > 0:
					# OUT COLLECTING
					dic_cate_elements[cate].append(e)
					dic_cate_volume[cate] += e.LookupParameter("Volume").AsDouble()*0.0283168
					dic_cate_rebars[cate].extend(rebars[1])
					dic_cate_rebars_volume[cate] += sum([rebars[2][d] for d in rebars[2]])
					dic_cate_rebars_weight[cate] += sum([rebars[3][d] for d in rebars[3]])
					
					dic_cate_rebars_length[cate] += sum([rebars[4][d] for d in rebars[3]])

					for d in rebars[3]:
						if not d in dic_cate_rebars_weight_per_type[cate]:
							dic_cate_rebars_weight_per_type[cate][d] = rebars[3][d]
						else:
							dic_cate_rebars_weight_per_type[cate][d] += rebars[3][d]
							
						if not d in dic_cate_rebars_length_per_type[cate]:
							dic_cate_rebars_length_per_type[cate][d] = rebars[4][d]
						else:
							dic_cate_rebars_length_per_type[cate][d] += rebars[4][d]
						
			except:
				pass
		try:
			dic_cate_rebars_weight_ratio[cate] = dic_cate_rebars_weight[cate] / dic_cate_volume[cate]
		except:
			pass
		for d in dic_cate_rebars_weight_per_type[cate]:
			dic_cate_rebars_weight_ratio_per_type[cate][d] = round(dic_cate_rebars_weight_per_type[cate][d] / dic_cate_volume[cate],3)
		
		
		for cate in dic_cate_rebars_weight_ratio_per_type:		
			dic_cate_rebars_weight_ratio_per_type_combine[cate] = {} # Category
			dic = dic_cate_rebars_weight_ratio_per_type[cate]			
			key_8 = ";".join([str(d) for d in dic])
			value_8 = ";".join([str(dic[d]) for d in dic])				
			dic_cate_rebars_weight_ratio_per_type_combine[cate][key_8] = value_8
	
	return dic_cate_elements,dic_cate_volume, dic_cate_rebars,dic_cate_rebars_volume,dic_cate_rebars_weight,dic_cate_rebars_weight_per_type,dic_cate_rebars_weight_ratio,dic_cate_rebars_weight_ratio_per_type,dic_cate_rebars_length,dic_cate_rebars_length_per_type,dic_cate_rebars_weight_ratio_per_type_combine

#----------------------------------------------------------------#
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()
categories = list(doc.Settings.Categories)
category_names = [c.Name for c in categories]

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
selection = UnwrapElement(IN[0])
cates = IN[1].splitlines()
rb_data = IN[2][1:]

rebar = UnwrapElement(IN[3])

#----------------------------------------------------------------#
if not selection.__class__.__name__ == "List":
	selection = [selection]
# Element Dictionary for quickly access
try:
	elem_dic = set_dic(selection)
except:
	pass
# rebar data dictionary
rb_dic_WPL = {} # Diction Weight per Length
for rd in rb_data:
	rb_dic_WPL["D{:0.0f}".format(rd[0])] = rd[1]
#----------------------------------------------------------------#
TransactionManager.Instance.EnsureInTransaction(doc)
setupUnit(doc)
TransactionManager.Instance.TransactionTaskDone()
#----------------------------------------------------------------#
# Assign your output to the OUT variable.
floor = selection[0]

OUT = rebar_ratio(cates)