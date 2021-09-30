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
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#

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
	
def _m3(v,r = 3):
	return round(v*0.0283168, r)

def getAllElementsOfCategory(doc,cat):
	"""Lấy tất cả các phần tử thuộc Category
	cates (list)
	oc : Revit Document	"""	
	categories = doc.Settings.Categories		
	for c in categories:
		if c.Name == cat:					
			return list(FilteredElementCollector(doc).OfCategoryId(c.Id).WhereElementIsNotElementType().ToElements())

def getSolids(e,opt = None):
	if opt == None:
		opt = Options()	
	solid = []
	try:
		geoE1 = e.get_Geometry(opt)
		geoE2 = []
		enum = geoE1.GetEnumerator()	
		while enum.MoveNext():
			geoE2 = enum.Current
			if isinstance(geoE2,Solid):
				solid.Add(geoE2)		
			else:
				if isinstance(geoE2,GeometryInstance):
					geoObj = geoE2.GetInstanceGeometry()
					for s in geoObj:
						if isinstance(s,Solid) and s.Volume > 0:
							solid.Add(s)	
	except Exception as ex:
		pass	
	return solid
def UnionSolid (solids):
	mergedSolid = None
	try:
		if len(solids) == 0:
			return None
		if len(solids) == 1:
			return solids[0]
		else:			
			first = solids[0]
			res = solids[1:]
			second = UnionSolid(res)			
			mergedSolid = BooleanOperationsUtils.ExecuteBooleanOperation(first,second,BooleanOperationsType.Union)
	except:
		pass
	return mergedSolid

def get_merged_solid(e):
	merged_solid = None
	if e.Category.Name == 'Stairs':
		subs = []
		try:
			runs = [doc.GetElement(eid) for eid in e.GetStairsRuns()]
			landings = [doc.GetElement(eid) for eid in e.GetStairsLandings()]                    
			subs.extend(runs)
			subs.extend(landings)    
			merged_solid = UnionSolid([UnionSolid(getSolids(s)) for s in subs])                
		except: # nếu không có Runs và Landings (trường hợp Model In Place)
			merged_solid = UnionSolid(getSolids(e))
	else:
		if e.LookupParameter('Volume') != None:
			merged_solid = UnionSolid(getSolids(e))
		else:
			solids = getSolids(e)
			merged_solid = UnionSolid(solids)	
	return merged_solid

def get_edges(e,opt = None):
	if opt == None:
		opt = Options()
	merged_solid = get_merged_solid(e)
	edge_array = merged_solid.Edges
	return edge_array
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
elevation = IN[1]
param_write = IN[2]
param_read = IN[3]
step_ = IN[4]
ask_write_parameter = IN[5]
ask_show_points = IN[6]
ask_vertical = IN[7]

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#	
web_points = []
distribution = []

exceptions = []
time_report = []
time_report.append(time.strftime("%d-%m-%y %H:%M:%S"))
debugger = []
debugger.append([])
debugger.append([])
TransactionManager.Instance.EnsureInTransaction(doc)
for e in elems:
	try:
		edges = get_edges(e)
		distribute_points = []
		for ed in edges:			
			try:
				curve = ed.AsCurve()
				transform = curve.ComputeDerivatives(0.5,False)
				points = None
				if ask_vertical == True:
					if curve.Direction.Normalize().Z != 0 :#transform.BasisX.Z != 0:
						points = points_array(curve.GetEndPoint(0),curve.GetEndPoint(1),step = step_,ext = 0)
				else:
					points = points_array(curve.GetEndPoint(0),curve.GetEndPoint(1),step = step_,ext = 0)
				distribute_points.extend(points)

			except Exception as ex:
				exceptions.append(ex)
				pass
		param = e.LookupParameter(param_read)
		distribute_value = 0
		if param.StorageType == StorageType.Double:
			distribute_value = round((param.AsDouble()*0.0283168) / len(distribute_points),3)
		if distribute_value != 0:
			quantity_string = "[Below_{0} ; Above_{0}] , [{1} ; {2}]"
			quantity_below = 0
			quantity_above = 0
			for p in distribute_points:
				if p.Z <= elevation:
					quantity_below += distribute_value
				else:
					quantity_above += distribute_value
					pass
			quantity_string = quantity_string.format(elevation,quantity_below,quantity_above)
			debugger[0].append(quantity_string)
			try:
				param_w = e.LookupParameter(param_write)
				if param_w.StorageType == StorageType.String:
					param_w.Set(quantity_string)
			except Exception as ex:
				exceptions.append(ex)
				pass
		if ask_show_points == True:
			debugger[1].append(distribute_points)
	except Exception as ex:
		exceptions.append(ex)
		pass
TransactionManager.Instance.TransactionTaskDone()
time_report.append(time.strftime("%d-%m-%y %H:%M:%S"))
OUT = time_report, debugger,exceptions