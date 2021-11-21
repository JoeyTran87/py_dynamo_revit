# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
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

import Autodesk.Revit.DB.JoinGeometryUtils as JGU

import time
#----------------------------------------------------#
#----------------------------------------------------#
#----------------------------------------------------#
def get_sheet_view_by_search_string(search_string):
    global doc    
    viewCollector = list(FilteredElementCollector(doc).OfClass(ViewSheet))
    try:
	    view_  = [v for v in viewCollector if search_string in v.Name][0]
	    return view_
    except:
    	return



#----------------------------------------------------#
#----------------------------------------------------#
#----------------------------------------------------#
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()
#----------------------------------------------------#
#----------------------------------------------------#
#----------------------------------------------------#

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
view_name = IN[0]

dic = {	"a":{"d10":10,"d16":16,"d20":20},
		"b":{"d10":11,"d16":17,"d20":21},
		"c":{"d10":12,"d16":18,"d20":22}}


# Place your code below this line
view_  = get_sheet_view_by_search_string(view_name)
text_collector = list(FilteredElementCollector(doc,view_.Id).OfClass(TextNote))
dic_text = {}


text_type = ""


for t in text_collector:
    try:
	    dic_text[str(t.Id)] = []
	    dic_text[str(t.Id)].append(t.Text.strip().split("\t"))#GetFormattedText().GetPlainText().strip()	    
	    text_type_border = t.TextNoteType.LookupParameter("Leader/Border Offset").AsDouble()*304.8
	    dic_text[str(t.Id)].append("{:0.0f}".format(round(t.Width*304.8 + 2*text_type_border)))
    
    except:
    	pass
# Assign your output to the OUT variable.
OUT = dic_text