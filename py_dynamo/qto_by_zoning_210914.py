# Load the Python Standard and DesignScript Libraries
import sys,os,time
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
from Autodesk.DesignScript.Geometry import Point as pt
from Autodesk.DesignScript.Geometry import Line as ln
from Autodesk.DesignScript.Geometry import Polygon as pg
from Autodesk.DesignScript.Geometry import Curve as cr
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

clr.AddReference("DSCoreNodes")
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#

def loc_curve(element):
	curve = None
	try:
		if element.Location.__class__ == LocationCurve:
			curve = element.Location.Curve
			return curve
		else:
			raise Exception('Test')
	except Exception as ex:
		return ex
		
def loc_curve_start_end(element):
	"""Trả lại điểm Đấu cuối của Curve (XYZ - Revit)"""
	curve = None
	try:
		if element.Location.__class__ == LocationCurve:
			curve = element.Location.Curve
			return curve.GetEndPoint(0),curve.GetEndPoint(1)
		else:
			raise Exception('Test')
	except Exception as ex:
		return ex
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def loc_curves(elements):
	curves = []
	for element in elements:
		try:
			curves.append(loc_curve(element))
		except Exception as ex:
			pass
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def getLocation(elements):
	curves = []
	points = []
	for element in elements:
		try:
			if element.Location.__class__ == LocationCurve:
				curves.append(element.Location)
			if element.Location.__class__ == LocationPoint:
				points.append(element.Location)
		except Exception as ex:
			pass
	return curves, points
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
def get_area(area):
	"""Vùng Area"""
	sebo = SpatialElementBoundaryOptions()
	try:
		if area.__class__.__name__ == 'Area':
			return area.GetBoundarySegments(sebo)
		else:
			raise Exception('Test')
	except Exception as ex:
		return ex

def flatten(t):
    return [item for sublist in t for item in sublist]		
    
def _mm(a,r = -1):
	return round(a*304.8,r)
	
def length_curve_loop(loop):
	length = 0
	for curve in loop:
		try:
			length += curve.Length
		except:
			pass
	return length	
def get_floor_boundary(doc,floor):
	if floor.__class__.__name__ == 'Floor':
		opt = Options()	
		sketch = doc.GetElement(ElementId(floor.Id.IntegerValue - 1))
		#if sketch.__class__.__name__ == 'Sketch':
		return list(sketch.Profile)
		
def revit_xyz_to_dyn_point(xyz,z_zero = False):
	"""210917"""
	z = xyz.Z
	if z == True:
		z = 0
	if xyz.__class__.__name__ == 'XYZ':
		return pt.ByCoordinates(_mm(xyz.X),_mm(xyz.Y),_mm(z))
	
def revit_line_to_dyn_line(line):
	if line.__class__.__name__ == 'Line' or line.__class__.__name__ == 'Curve' :
		point_0 = revit_xyz_to_dyn_point(line.GetEndPoint(0))
		point_1 = revit_xyz_to_dyn_point(line.GetEndPoint(1))
		line = ln.ByStartPointEndPoint(point_0,point_1)
		return line

def revit_curves_to_dyn_polygon(curves,end = 0):
	points = [revit_xyz_to_dyn_point(c.GetEndPoint(end)) for c in curves]
	return pg.ByPoints(points)
		
def max_curvesloop(curves_loops):	
	if len(curves_loops) == 1:
		return curves_loops[0]
	elif len(curves_loops) > 1:
		max_loop = curves_loops[0]
		for loop in curves_loops:
			if length_curve_loop(loop) > length_curve_loop(max_loop):
				max_loop = loop
		return max_loop		

def filter_keep_lines(curves_loops):
	list_line = []
	for line in max_curvesloop (curves_loops):
		if revit_line_to_dyn_line(line)	!= None:
			list_line.append(line)
	return list_line
def check_point_in_polygon(polygon,point):
	pass
	
def get_bounding_minmax(doc,elem):
	try:
		bbx = elem.get_BoundingBox(doc.ActiveView)
		min = bbx.Min
		max = bbx.Max
		return min,max
	except Exception as ex:
		return ex
def points_array(start,end,step = 1000,ext = 0):
	"""fixed 210917
	TẠO CHUỖI ĐIỂM DYNAMO
	ĐỒNG CAO ĐỘ 0	
	start,end (XYZ - Revit)
	step,ext,offset (mm)

	return: [Point] (Dynamo)
	"""		
	start = revit_xyz_to_dyn_point(start)
	end = revit_xyz_to_dyn_point(end)

	line = ln.ByStartPointEndPoint(start, end)
	try:
		if line.Length > step:
			count = 2
			try:
				count = int(line.Length / (step + ext))
			except:
				pass		
			point_array = list(cr.PointsAtEqualSegmentLength(line, count))
			if point_array != None:
				return point_array
			else:
				raise Exception('Default Apply')
		else:
			raise Exception('Default Apply')
	except Exception as ex:
		return start,end

def points_web(min,max,curve_loop,step = 1000,ext = 2,offset = 500):
	"""TẠO LƯỚI ĐIỂM DYNAMO
	ĐỒNG CAO ĐỘ 0
	min , max (Revit Bouding Box Min Max)
	curve_loop (Revit)
	step,ext,offset (mm)
	
	return: [Point] (Dynamo)
 	"""
	web = []	
	step = round(step/304.8,3)
	offset = round(offset/304.8,3)
	d_x = abs(max.X-min.X)
	d_y = abs(max.Y-min.Y)
	x = min.X
	y = min.Y
	for i in range(int(round(d_x/step))+ext):
		for j in range(int(round(d_y/step))+ext):
			point = XYZ(x + offset + i*step,y + offset + j*step,0)
			point = revit_xyz_to_dyn_point(point)				
			polygon = revit_curves_to_dyn_polygon(curve_loop,end = 0)
			if pg.ContainmentTest(polygon,point):
				web.append(point)
	return web
	
def _m3(v,r = 3):
	return round(v*0.0283168, r)
	
def distribute_quantity_to_point(elem,pts,param = 'Volume',r = 3):
	quantity = _m3(elem.LookupParameter(param).AsDouble())
	count = len(pts)
	if count == 1:
		return quantity
	elif count >1:
		return round(quantity/count, r)
		
#---------------------------------------------------------------------------------#
def area_sketh_outline(doc,area, SEPopt = None):
	"""LẤY ĐƯỜNG BIÊN NGOÀI CỦA ĐỐI TƯỢNG AREA
		LOẠI BỎ CÁC AREA CÓ PROFILE BÊN TRONG"""
	if area.__class__.__name__ == 'Area':
		if SEPopt == None:
			SEPopt = SpatialElementBoundaryOptions ()
		bound_segs = list(area.GetBoundarySegments(SEPopt))
		if len(bound_segs) == 1:				
			return [seg.GetCurve() for seg in bound_segs[0]]
def area_data(areas):
	# XỬ LÍ AREA
	
	areas = areas
	SEPopt = SpatialElementBoundaryOptions ()
	area_curves = [area_sketh_outline(doc,area,SEPopt) for area in areas if area != None]
	area_polygons = [revit_curves_to_dyn_polygon([line for line in list]) for list in area_curves if list != None ]
	area_names = [area.LookupParameter('Name').AsString() for area in areas if area != None]
	area_levels = [doc.GetElement(area.LookupParameter('Level').AsElementId()).Name for area in areas if area != None]
	return area_polygons,area_names,area_levels

def find_zoned_quantity(area_names,area_polygons,points,pt_quan,area_list):
	global area_list_2,debugger
	quan_str = ""
	dic = {}	
	for n in area_list:
		dic[n] = 0
	for point in points:
		for polygon in area_polygons:
			if pg.ContainmentTest(polygon,point):				
				dic[area_names[area_polygons.index(polygon)]] += 1				
	count_zoned_pt = sum([dic[c] for c in dic])
	dic['ZZ_No_Zone'] = len(points) - count_zoned_pt
	new_keys = sorted(dic.keys())
	for k in new_keys:
		quan_str += "{} ".format(dic[k]*pt_quan)		
	return quan_str
def getAllElementsOfCategory(doc,cat):
	"""Lấy tất cả các phần tử thuộc Category
	cates (list)
	oc : Revit Document	"""	
	categories = doc.Settings.Categories		
	for c in categories:
		if c.Name == cat:					
			return list(FilteredElementCollector(doc).OfCategoryId(c.Id).WhereElementIsNotElementType().ToElements())
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
elems = IN[0]
elems = UnwrapElement(elems)
try :
	len(elems)
except:
	elems = [elems]
	
areas = IN[1]
areas = [a for a in UnwrapElement(areas) if a.__class__.__name__ == 'Area']
try :
	len(areas)
except:
	areas = [areas]

paramName = IN[2]
param_read = IN[3]
param_zone_names = IN[4]

# LẤY TÊN TOÀN BỘ AREA TRONG MÔ HÌNH
area_list = [a.LookupParameter('Name').AsString() for a in getAllElementsOfCategory(doc,'Areas')]

area_list = [d for d in {a for a in area_list}]
area_list.sort()
area_list.append('ZZ_No_Zone')
step_ = IN[5]
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#	
web_points = []
distribution = []
exceptions = []
area_polygons,area_names,area_levels = area_data(areas)
time_report = []
time_report.append(time.strftime("%d-%m-%y %H:%M:%S"))
debugger = []

trans_name = "Zone Quantity {0}".format(time.strftime("%y%m%d %H%M%S"))

TransactionManager.Instance.EnsureInTransaction(doc)
for elem in elems:
	try:
		points = None
		if elem.__class__.__name__ == 'Floor':
			curves_loops = get_floor_boundary(doc,elem)
			floor_boundary = filter_keep_lines(curves_loops)
			lines = flatten(curves_loops)
			min,max = get_bounding_minmax(doc,elem)
			# TẠO LUOI ĐIỂM ĐỂ PHÂN BỐ
			points = points_web(min,max,floor_boundary,step = step_) # vẫn còn là revit point			
			
		if elem.Location.__class__ is LocationPoint:
			points = revit_xyz_to_dyn_point(elem.Location.Point)
		
		if elem.Location.__class__ is LocationCurve:
			start,end = loc_curve_start_end(elem)
			points = points_array(start,end,step = step_)
			# points = [revit_xyz_to_dyn_point(p) for p in loc_curve_start_end(elem)]
		
		if len(points) == 0:
			min,max = get_bounding_minmax(doc,elem)
			points = revit_xyz_to_dyn_point(XYZ((min.X+max.X)/2,(min.Y + max.Y)/2,0))
		debugger = points
		
		try:
			len(points)
		except:
			points = [points]
		
		web_points.append(points)
		# TÍNH TOÁN LƯỢNG KHỐI LỢNG PHÂN BỔ CHO TỪNG ĐIỂM 
		pt_quan = distribute_quantity_to_point(elem,points, param=param_read)	
		# TÌM ĐIỂM THUỘC AREA
		zoned_quanity = find_zoned_quantity(area_names,area_polygons,points,pt_quan,area_list)
		
		distribution.append(zoned_quanity)
		#GHI GIÁ TRỊ VÀO PARAMETER
		try:
			param = elem.LookupParameter(paramName)
			param.Set(zoned_quanity)
			param2 = elem.LookupParameter(param_zone_names)
			param2.Set(' '.join(area_list))
		except:
			pass
	except Exception as ex:
		exceptions.append(ex)
		pass
TransactionManager.Instance.TransactionTaskDone()
time_report.append(time.strftime("%d-%m-%y %H:%M:%S"))
OUT = debugger,time_report," ".join(area_list), "{0} trên {1} đối tuong xử lí thành công Quantity Zone".format(len(distribution),len(elems))

# FOR DEBUGGING
# ,web_points,exceptions#,distribution,area_polygons,area_names,area_levels,debugger,area_polygons,,exceptions,web_points