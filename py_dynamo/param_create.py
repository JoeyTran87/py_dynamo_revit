# Load the Python Standard and DesignScript Libraries
import sys,os
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.ExternalFileUtils import *
from Autodesk.Revit.Creation import *
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
## add module director
#ip = "172.16.2.29"
#domain = "hcmcfcfs01"
#dynPyDir = ""
#dynPyDir_ip = "\\\\{0}\\databim$\\BimESC\\00-BIM STANDARD\\PYTHON\\pythondynamo".format(ip)
#dynPyDir_domain = "\\\\{0}\\databim$\\BimESC\\00-BIM STANDARD\\PYTHON\\pythondynamo".format(domain)
#if os.path.exists(dynPyDir_domain):
#	dynPyDir = dynPyDir_domain	
#if os.path.exists(dynPyDir_ip):
#	dynPyDir = dynPyDir_ip	
# dynPyDir = IN[5]
# sys.path.append(dynPyDir)
# import pyDyn
# from pyDyn import *

def getParameterDefinitions(app = None,group = None):
    """## get share parameter from file
    updated 210916"""
    paraDefs = []
    paraDefNames = []
    para_dic = {}

    if app == None:   
        app = DocumentManager.Instance.CurrentUIApplication.Application
    if group == None:
        group = 'COF'    
	# definition = app.OpenSharedParameterFile()
	# defGSenum = definition.Groups.GetEnumerator()
    for _,def_group in enumerate(app.OpenSharedParameterFile().Groups.GetEnumerator()):
        if def_group.Name == group: # index 0 : số 0 , index 1 là Definition Group
            definitions = def_group.Definitions
            for de in definitions:
                #str=de.GUID+spbr+de.Name+spbr+de.ParameterType+spbr+de.ParameterGroups+spbr+de.Visible+spbr+de.Description+spbr+de.UserModifiable+spbr+de.HideWhenNoValue # FAIL ParameterGroups
                paraDefs.append(de)
                paraDefNames.append(de.Name)
                para_dic[de.Name] = de
    para_dic_items = sorted(para_dic.items())
    return para_dic_items #[defG for defG in enumerate(app.OpenSharedParameterFile().Groups.GetEnumerator())],paraDefs, paraDefNames,para_dic,

def createMultiParameter(doc,para_dic_items,cates, param_group = None,startwith = None,reset = False):
    exceptions = []
    if startwith == None:
        startwith = 'COF'
    if param_group == None or param_group == 'Construction':
        param_group = BuiltInParameterGroup.PG_CONSTRUCTION
    elif param_group == 'Structural':
        param_group = BuiltInParameterGroup.PG_STRUCTURAL
    else:
        param_group = BuiltInParameterGroup.PG_CONSTRUCTION
    
    cats = doc.Settings.Categories
    catset = CategorySet()
    
    for cate in cates:
        try:
            for cat in cats:
                if cat.Name == cate:
                    catset.Insert(cat)
        except Exception as ex:
            pass
    newIB = InstanceBinding(catset)
    

    TransactionManager.Instance.EnsureInTransaction(doc)
	

    if reset == True:
        binding_map =  doc.ParameterBindings
        for dic in para_dic_items:# Case ALL	
            try:
                if dic[0][:len(startwith)] == startwith:
                    if binding_map.Contains(dic[1]) == True:
                        binding_map.Remove(dic[1])
            except Exception as ex:
            	exceptions.append(ex)
                pass
    if reset == False:
        binding_map =  doc.ParameterBindings
        for dic in para_dic_items:
            try:
                if dic[0][:len(startwith)] == startwith:
                    if binding_map.Contains(dic[1]) == False:
                        binding_map.Insert(dic[1],newIB,param_group)
                    # else:#update by ReInsert
	                #     binding_map.ReInsert(dic[1],newIB,param_group)
            except Exception as ex:
                exceptions.append(ex)
                pass
        
	TransactionManager.Instance.TransactionTaskDone()
    return exceptions,para_dic_items,catset#[binding_map.Contains(dic[1]) for dic in para_dic_items]#

#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()	
# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
cates = IN[0].splitlines()
param_group = IN[1]
start_with = IN[2]
ask_reset = IN[3]

try:
	OUT = createMultiParameter(doc,getParameterDefinitions(app,group = 'COF'),cates,param_group=param_group,startwith=start_with,reset=ask_reset)
except Exception as ex:
	OUT = ex