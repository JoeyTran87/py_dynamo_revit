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
def get_textnote(view_):
	global doc , debugger,text_type
	text_collector = list(FilteredElementCollector(doc,view_.Id).OfClass(TextNote))
	dic_text = {}
	for t in text_collector:
		try:
			# Global Text Type:
			text_type = t.TextNoteType
			dic_text[str(t.Id)] = {}
			# GIÁ TRI TEXTNOTE		
			dic_text[str(t.Id)]["TextNoteValue"] = t.Text.strip()#GetFormattedText().GetPlainText().strip()				
			# GIÁ TRI TEXTNOTE LIST sep TAB
			dic_text[str(t.Id)]["TextNoteValueColumnList"] = []			
			dic_text[str(t.Id)]["TextNoteValueColumnList"].append(t.Text.strip().split("\t"))#GetFormattedText().GetPlainText().strip()	
			# ÐO DAI TEXTNOTE		
			text_type_border = t.TextNoteType.LookupParameter("Leader/Border Offset").AsDouble()*304.8			
			dic_text[str(t.Id)]["TextNoteWidth"] = ("{:0.0f}".format(round(t.Width*304.8 + 2*text_type_border)))			
			# TEXTNOTE TYPE
			dic_text[str(t.Id)]["TextNoteType"] = t.Name#GetFormattedText().GetPlainText().strip()				
			# TAB SIZE
			dic_text[str(t.Id)]["TextNoteTabSize"] = t.TextNoteType.LookupParameter("Tab Size").AsDouble()*304.8
			# TEXT SIZE
			dic_text[str(t.Id)]["TextNoteTextSize"] = t.TextNoteType.LookupParameter("Text Size").AsDouble()*304.8
			# TEXT FONT
			dic_text[str(t.Id)]["TextNoteFont"] = t.TextNoteType.LookupParameter("Text Font").AsString()
			# TEXT BOLD
			dic_text[str(t.Id)]["TextNoteBold"] = t.TextNoteType.LookupParameter("Bold").AsInteger()
			# TEXT ITALIC
			dic_text[str(t.Id)]["TextNoteItalic"] = t.TextNoteType.LookupParameter("Italic").AsInteger()
			# TEXT UNDERLINE
			dic_text[str(t.Id)]["TextNoteUnderline"] = t.TextNoteType.LookupParameter("Underline").AsInteger()
			# TEXT WIDTH FACTOR
			dic_text[str(t.Id)]["TextNoteWidthFactor"] = t.TextNoteType.LookupParameter("Width Factor").AsDouble()
		except Exception as ex:
			debugger.append(ex)
			pass
	return dic_text
#----------------------------------------------------#
#----------------------------------------------------#
#----------------------------------------------------#
debugger = []


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

# TEXTNOTE TYPE
text_type = None


# GET VIEW SHEET
view_  = get_sheet_view_by_search_string(view_name)

# GET TEXTNOTE
dic_text = get_textnote(view_)



OUT = view_,text_type,dic_text