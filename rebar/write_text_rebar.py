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
#-----------------------------------------------------------------------#
def get_sheet_view_by_search_string(search_string):
    global doc    
    viewCollector = list(FilteredElementCollector(doc).OfClass(ViewSheet))
    try:
	    view_  = [v for v in viewCollector if search_string in v.Name][0]
	    return view_
    except:
    	return

#-----------------------------------------------------------------------#
debugger = []
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()
#-----------------------------------------------------------------------#
# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
data = IN[0]
dic = {"a":{"D10":10,"D16":16,"D20":20},
		"b":{"D10":11,"D16":17,"D20":21},
		"c":{"D10":12,"D16":18,"D20":22}}#IN[0]

dic1 = {"a":46,
		"b":47,
		"c":48}#IN[0]


#VIEW
view = IN[1]

# DATA REBAR WEIGHT
rb_data = IN[3][1:]
rb_types = ["D{:0.0f}".format(data[0]) for data in rb_data]

# WRITE TEXT
# POINT
point = pt.ByCoordinates(0,0) #START
# TEXT TO WRITE
dic_text={} # primitive
for ttt in rb_types:
    dic_text[ttt] = 0

new_dic = {}
for d in dic:
	new_dic[d] = {}
	new_d = dic_text.copy()
	new_d.update(dic[d])
	new_dic[d] = new_d

headers = "Category\t{}".format("\t".join([tt for tt in rb_types]))

content = []
content.append(headers)
for d in new_dic:
	content.append("{}\t{}".format(d,"\t".join([str(new_dic[d][dd]) for dd in new_dic[d]])))

text = "\n".join(content)
# ALIGN
align = "Left"
# TEXT TYPE

text_type = IN[2]
keep_rot = False
rot = 0
# WRITE
t= tn.ByLocation(view,point,text,align,text_type,keep_rot,rot)

OUT = headers