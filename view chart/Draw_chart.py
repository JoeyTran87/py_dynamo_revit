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
import math
#------------------------------------------------------------------------#
def get_sheet_view_by_search_string(search_string):
	global doc    
	viewCollector = list(FilteredElementCollector(doc).OfClass(ViewSheet))
	try:
		view_  = [v for v in viewCollector if search_string in v.Name][0]
		return view_
	except:
		return

def get_sheet_view_2 (view_name,sheet_number = "000"):
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
				view_sheet.SheetNumber = sheet_number
			except:
				view_sheet.SheetNumber = sheet_number*2
			view_sheet.Name = view_name
			# Delete Title Block
			title_blocks = list(FilteredElementCollector(doc,view_sheet.Id).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().ToElements())
			[doc.Delete(t.Id) for t in title_blocks]
			TransactionManager.Instance.TransactionTaskDone()
		except Exception as ex:
			# debugger.append(ex)
			pass
	return view_sheet
def write_text(viewId,text,position = None,typeId = None,rotate = None,text_option = None):
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
	if rotate:
		pass
	TransactionManager.Instance.TransactionTaskDone()

	return text_note

def draw_line (view,x,y,x1,y1):
	global doc
	TransactionManager.Instance.EnsureInTransaction(doc)
	P1 = XYZ(x/304.8,y/304.8,0)
	P2 = XYZ(x1/304.8,y1/304.8,0)
	L1 = Line.CreateBound(P1,P2)
	dc = doc.Create.NewDetailCurve(view,L1)
	TransactionManager.Instance.TransactionTaskDone()
	return dc

def draw_line_by_angle_length(view,x,y,angle,length):
	global doc
	TransactionManager.Instance.EnsureInTransaction(doc)
	P1 = XYZ(x/304.8,y/304.8,0)

	

	P2 = XYZ(x1/304.8,y1/304.8,0)
	L1 = Line.CreateBound(P1,P2)
	dc = doc.Create.NewDetailCurve(view,L1)
	TransactionManager.Instance.TransactionTaskDone()
	return dc
	pass

def draw_arc_start_end_third(view,x1,y1,x2,y2,x3,y3):
	global doc
	TransactionManager.Instance.EnsureInTransaction(doc)
	p1 = XYZ(x1/304.8,y1/304.8,0)
	p2 = XYZ(x2/304.8,y2/304.8,0)
	p3 = XYZ(x3/304.8,y3/304.8,0)
	arc = Arc.Create(p1,p2,p3)
	dc = doc.Create.NewDetailCurve(view,arc)
	TransactionManager.Instance.TransactionTaskDone()
	return dc
def draw_elipse(view,x,y,x_Radius=10,y_Radius=10,x_Axis=None,y_Axis=None,start_Parameter=0,end_Parameter=7):
	global doc
	TransactionManager.Instance.EnsureInTransaction(doc)
	XYZcenter = XYZ(x/304.8,y/304.8,0)
	if x_Axis==None: x_Axis=XYZ(1/304.8,0,0)
	if y_Axis==None: y_Axis=XYZ(0,1/304.8,0)
	elipse = Ellipse.CreateCurve(XYZcenter/304.8,x_Radius/304.8,y_Radius,x_Axis,y_Axis,start_Parameter,end_Parameter)
	dc = doc.Create.NewDetailCurve(view,elipse)
	TransactionManager.Instance.TransactionTaskDone()
	return dc

def draw_rectange_by_2_corners(view,x1,y1,x2,y2):
	global doc
	TransactionManager.Instance.EnsureInTransaction(doc)
	p1 = XYZ(x1/304.8,y1/304.8,0)
	p2 = XYZ(x2/304.8,y1/304.8,0)
	p3 = XYZ(x2/304.8,y2/304.8,0)
	p4 = XYZ(x1/304.8,y2/304.8,0)
	l1 = Line.CreateBound(p1,p2)
	l2 = Line.CreateBound(p2,p3)
	l3 = Line.CreateBound(p3,p4)
	l4 = Line.CreateBound(p4,p1)
	rec = [doc.Create.NewDetailCurve(view,l) for l in [l1,l2,l3,l4]]
	TransactionManager.Instance.TransactionTaskDone()
	return rec

def draw_arrowhead_axis(view,p,angle,length = 5,rotate = 0):
	"""view: 2D VIEW
	angle: degree
	length: mm
	rotate: degree"""
	global doc
	TransactionManager.Instance.EnsureInTransaction(doc)
	angle = math.radians(angle)
	rotate = math.radians(rotate)
	length = length / 304.8

	p1 = Transform.CreateRotationAtPoint(XYZ(0,0,1), - angle+rotate,p).OfPoint(Transform.CreateTranslation(XYZ(length,0,0)).OfPoint(p))
	p2 = Transform.CreateRotationAtPoint(XYZ(0,0,1), angle + math.pi+rotate,p).OfPoint(Transform.CreateTranslation(XYZ(length,0,0)).OfPoint(p))

	p = XYZ(p.X,p.Y,0)
	p1 = XYZ(p1.X,p1.Y,0)
	p2 = XYZ(p2.X,p2.Y,0)

	A_L1 = Line.CreateBound(p,p1)
	A_L2 = Line.CreateBound(p,p2)

	arrow = [doc.Create.NewDetailCurve(view,l) for l in [A_L1,A_L2]]
	TransactionManager.Instance.TransactionTaskDone()
	return arrow
 

def draw_axis_xy(view,origin = None,x_length = 10,y_length = 10,angle = 45, arrow_length = 3):
	global doc
	x_length = x_length/304.8
	y_length = y_length/304.8
	TransactionManager.Instance.EnsureInTransaction(doc)
	P0 = XYZ(0,0,0)
	Px = XYZ(x_length,0,0)
	Py = XYZ(0,y_length,0)

	# Translate
	if not origin == None and origin.__class__.__name__ == "XYZ":
		P0 = translate_point(P0,origin)
		Px = translate_point(Px,origin)
		Py = translate_point(Py,origin)		
	
	L1 = Line.CreateBound(P0,Px)
	L2 = Line.CreateBound(P0,Py)
	c_ = []
	c_.append(L1)
	c_.append(L2)
	
	axis = [doc.Create.NewDetailCurve(view,l) for l in c_]

	axis.extend(draw_arrowhead_axis(view,Px,angle,length = arrow_length,rotate = -90))
	axis.extend(draw_arrowhead_axis(view,Py,angle,length = arrow_length,rotate = 0))
	
	TransactionManager.Instance.TransactionTaskDone()
	return axis

def draw_chart_column(view,origin = None,col_width = 5,col_height = [50,100,150],distance = 30,start_space = 10,col_head = ['Column1','Column2','Column3']):
	for h in col_height:
		head = col_head[col_height.index(h)]
		x1 = start_space + (distance + col_width)*col_height.index(h)
		y1 = 0
		x2 = start_space + col_width + (distance + col_width)*col_height.index(h) 
		y2 = h
		draw_rectange_by_2_corners(view,x1,y1,x2,y2)
		write_text(view.Id, str(head) ,position = XYZ(x1/304.8 , 0,0))
		write_text(view.Id, str(h) ,position = XYZ(0, y2/304.8,0))

	draw_axis_xy(	view,origin = origin,
					x_length = (start_space + col_width + distance) * len(col_height),
					y_length =  max(col_height) + start_space,
					angle = 45, 
					arrow_length = 3)




def draw_chart_pie():
	pass

def translate_point(p,vector):
	if p.__class__.__name__ == "XYZ" and vector.__class__.__name__ == "XYZ":
		translation = Transform.CreateTranslation(vector)
		p2 = translation.OfPoint(p)
		return p2
def translate_curve(c,vector):
	pass
def rotate_point(p,angle = None,origin = None):
	"""angle: degree"""
	if origin == None:
		origin = XYZ()
	if angle == None:
		angle = 0		
	else:
		angle = math.radians(angle)
	if p.__class__.__name__ == "XYZ" and origin.__class__.__name__ == "XYZ":
		translation = Transform.CreateRotationAtPoint(XYZ(0,0,1), angle,origin)
		p2 = translation.OfPoint(p)
		return p2
#-------------------------------------------------------#
dataEnteringNode = IN
debugger = []

doc,uiapp,app = IN[0]
opt = Options()
view_name = IN[1]

view = get_sheet_view_2 (view_name)

OUT = draw_chart_column(view,origin = None,col_width = 5,col_height = [50,100,150],distance = 30,start_space = 10,col_head = ['Column1','Column2','Column3'])
#draw_axis_xy(view,origin = XYZ(10/304.8,10/304.8,0),x_length = 10,y_length = 10,angle = 45, arrow_length = 3)