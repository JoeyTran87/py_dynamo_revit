# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
# clr.AddReference('RevitAPI')
# from Autodesk.Revit.DB import *
# clr.AddReference('RevitAPIUI')
# from Autodesk.Revit.UI import TaskDialog
clr.AddReference("RevitNodes")
import Revit
# clr.ImportExtensions(Revit.Elements)
# clr.AddReference("RevitServices")
# import RevitServices
# from RevitServices.Persistence import DocumentManager
# from RevitServices.Transactions import TransactionManager
# from System.Collections.Generic import *

# import Autodesk.Revit.DB.JoinGeometryUtils as JGU

import time



def flat_curves(curves_main,seg_count,at_start):
	curves_flat = []
	raw_points = []
	points_flat = []
	detail_curves = []
	detail_points = []
	L_sum = 0 # độ dài cộng dồn

	for c in curves_main:
		try:
			# at start
			at_start_p = Curve.PointAtParameter(at_start,0.5)

			L = c.Length
			c_start = c.StartPoint
			c_end = c.EndPoint
			
			# chia doan
			points = []
			
			seg = L / int(seg_count)			
			points.append(c_start)
			div_p = Curve.PointsAtChordLengthFromPoint(c,c.StartPoint,seg)
			points.extend(div_p)
			points.append(c_end)
			debugger = [Curve.ParameterAtPoint(c,p) for p in points]

			if round(Curve.ParameterAtPoint(c,points[-2]),2) == 1: #tiny_line.Length < 10:
				points = points[:-1]
			# Kiem tra hướng
			if Line.ByStartPointEndPoint(points[0],at_start_p).Length > Line.ByStartPointEndPoint(points[-1],at_start_p).Length: # check huong
				points.reverse() # dao nguoc danh sach			
			
			raw_points.append(points)			
			# flatten points		
			for p in points:
				points_flat.append(Point.ByCoordinates(p.X,p.Z,0))

			# try:		
			# 	c_flat = PolyCurve.ByPoints(points_flat)
			# except:
			# 	c_flat = Line.ByStartPointEndPoint(points_flat[0],points_flat[-1])
			c_flat = PolyCurve.ByPoints(points_flat)
			# L_flat = c_flat.Length
			
			d_points = []
			for i in range(len(points_flat)):
				try:
					p = points[i]
					pf = points_flat[i]
					d_points.append(Point.ByCoordinates(Curve.ParameterAtPoint(c_flat,pf)*c_flat.Length,p.Z))	
				except:
					pass				
			
			detail_points.append(d_points)
			
			# cộng dồn độ dài		
			L_sum += L_flat
			L_flat = 0
		except Exception as ex:
			detail_points.append(ex)
			pass
	return debugger,at_start_p,raw_points,detail_points
def flat_curve(c,seg_count):
	global raw_points,detail_points,at_start_p,L_sum,params
	try:		
		L = c.Length
		c_start = c.StartPoint
		c_end = c.EndPoint		
		# chia doan
		points = []		
		seg = L / int(seg_count)			
		points.append(c_start)
		div_p = Curve.PointsAtChordLengthFromPoint(c,c.StartPoint,seg)
		points.extend(div_p)
		points.append(c_end)		

		if round(Curve.ParameterAtPoint(c,points[-2]),2) == 1: #tiny_line.Length < 10:
			points = points[:-1]
		# Kiem tra hướng
		if Line.ByStartPointEndPoint(points[0],at_start_p).Length > Line.ByStartPointEndPoint(points[-1],at_start_p).Length: # check huong
			points.reverse() # dao nguoc danh sach			
		
		raw_points.append(points)			
		# flatten points		
		points_flat = []
		for p in points:
			points_flat.append(Point.ByCoordinates(p.X,p.Z,0))
		# try:		
		# 	c_flat = PolyCurve.ByPoints(points_flat)
		# except:
		# 	c_flat = Line.ByStartPointEndPoint(points_flat[0],points_flat[-1])
		c_flat = PolyCurve.ByPoints(points_flat)
		L_flat = c_flat.Length
		
		d_points = []
		param_at_curve = []
		for i in range(len(points_flat)):
			try:
				p = points[i]
				pf = points_flat[i]
				d_points.append(Point.ByCoordinates(L_sum + Curve.ParameterAtPoint(c_flat,pf)*L_flat, p.Z))	
				param_at_curve.append(Curve.ParameterAtPoint(c_flat,pf))
			except:
				pass				
		params.append(param_at_curve)
		detail_points.append(d_points)
		
		# cộng dồn độ dài		
		L_sum += L_flat
		L_flat = 0
	except Exception as ex:
		detail_points.append(ex)
		pass
	return d_points

def process_curve(c,seg_count):
	global raw_points,at_start_p
	try:		
		L = c.Length
		c_start = c.StartPoint
		c_end = c.EndPoint		
		# chia doan
		points = []		
		seg = L / int(seg_count)			
		points.append(c_start)
		div_p = Curve.PointsAtChordLengthFromPoint(c,c.StartPoint,seg)
		points.extend(div_p)
		points.append(c_end)
		if round(Curve.ParameterAtPoint(c,points[-2]),2) == 1: #tiny_line.Length < 10:
			points = points[:-1]
		# Kiem tra hướng
		if Line.ByStartPointEndPoint(points[0],at_start_p).Length > Line.ByStartPointEndPoint(points[-1],at_start_p).Length: # check huong
			points.reverse() # dao nguoc danh sach		
		return points
	except Exception as ex:
		pass	
def flatten_poly_curve(poly_c,flatten_poly_c,panel_width):
	global line_ele
	FL = flatten_poly_c.Length

	FC_start = flatten_poly_c.StartPoint
	FC_end = flatten_poly_c.EndPoint
	
	# chia doan
	F_points = []		
	panel_width = float(panel_width)
	F_points.append(FC_start)
	div_p = Curve.PointsAtChordLengthFromPoint(flatten_poly_c,FC_start,panel_width)
	F_points.extend(div_p)
	F_points.append(FC_end)

	try:
		if round(Curve.ParameterAtPoint(flatten_poly_c,F_points[-2]),2) == 1: #tiny_line
			F_points = F_points[:-1]
	except:
		pass

	points_on_polycurve = []
	for p in F_points:
		try:
			vec = Vector.ByCoordinates(0,0,1)
			pp = Point.Project(p,poly_c,vec)
			if pp == None:
				vec = Vector.ByCoordinates(0,0,-1)
				pp = Point.Project(p,poly_c,vec)
			points_on_polycurve.append(pp[0])
		except:
			pass
	
	connect_lines = []
	d_points = []
	for i in range(len(F_points)):
		try:
			p = points_on_polycurve[i]
			pf = F_points[i]
			d_points.append(Point.ByCoordinates(i*panel_width,p.Z))				
		except Exception as ex:
			pass	
	flatten_curves = PolyCurve.ByPoints(d_points).Curves()

	line_zero = Line.ByStartPointEndPoint(Point.ByCoordinates(-FL/8,line_ele),Point.ByCoordinates(FL+FL/8,line_ele))
		
	for i in range(len(d_points)):
		try:
			p1 = d_points[i]
			vec = Vector.ByCoordinates(0,-1,0)
			p2 = Point.Project(p1,line_zero,vec)
			if p2 == None:
				vec = Vector.ByCoordinates(0,1,0)
				p2 = Point.Project(p1,line_zero,vec)
			connect_lines.append(Line.ByStartPointEndPoint(p1,p2[0]))
		except Exception as ex:
			connect_lines.append(ex)
			pass	

	return flatten_curves,line_zero,connect_lines,d_points
# Assign your output to the OUT variable.


# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
curves_main = IN[0]
at_start = IN[1] # curve
seg_count = IN[2]
panel_width  = IN[3]
panel_height  = IN[4]
line_ele = float(IN[5])

if not curves_main.__class__.__name__ == "list":
	curves_main = [curves_main]
# at start
at_start_p = Curve.PointAtParameter(at_start,0.5)

curves_flat = []
raw_points = []
detail_curves = []
detail_points = []
L_sum = 0 # độ dài cộng dồn
params = []

for c in curves_main:
	if curves_main.index(c) == len(curves_main)-1:
		raw_points.extend(process_curve(c,seg_count))
	else:
		raw_points.extend(process_curve(c,seg_count)[:-1])

poly_c = PolyCurve.ByPoints(raw_points)
flatten_poly_c = Curve.PullOntoPlane(poly_c,Plane.XY())

flatten_list = flatten_poly_curve(poly_c,flatten_poly_c,panel_width)

detail_curves.extend(flatten_list[0])
detail_curves.append(flatten_list[1])
detail_curves.extend(flatten_list[2])

OUT = detail_curves