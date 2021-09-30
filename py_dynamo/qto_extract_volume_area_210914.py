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

def flatten(t):
    return [item for sublist in t for item in sublist]	

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
	geoE1 = e.get_Geometry(opt)
	geoE2 = []
	try:
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

def getRawVolume(solids):
	vol = 0
	try:
		for s in solids:
			vol += s.Volume*0.0283168
	except:	
		pass
	return vol

def get_volume_area(doc,elems,param_volume = None, write_param = False,param_area = None,param_area_sep = None):
    pairs=[]
    exceptions = []
    face_list = []
    face_normal_list = []
    for e in elems: 
        try:
            volume = None
            merged_solid = None
            faces = None
            pair = []
            # if e.__class__.__name__ == 'Stairs':            
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
                    volume = e.LookupParameter('Volume').AsDouble()
                    merged_solid = UnionSolid(getSolids(e))
                else:
                    solids = getSolids(e)
                    merged_solid = UnionSolid(solids)
            
            volume = round(merged_solid.Volume*0.0283168,3)
            
            faces = merged_solid.Faces
            face_area_string = '{0};{1};{2};{3};{4};{5}'
            face_hor_up_area = 0
            face_hor_down_area = 0
            face_ver_area = 0
            face_slant_up_area = 0
            face_slant_down_area = 0
            face_non_flat = 0
            for f in faces:
                if f.__class__.__name__ == 'PlanarFace':
                    if f.FaceNormal.X == f.FaceNormal.Y == 0:
                        if f.FaceNormal.Z > 0: # Face mặt trên
                            face_hor_up_area += round(f.Area*0.092903,3)
                        elif f.FaceNormal.Z < 0: # Face mặt dưới
                            face_hor_down_area += round(f.Area*0.092903,3)
                    elif f.FaceNormal.Z == 0: # Face thẳng đứng
                        face_ver_area += round(f.Area*0.092903,3)
                    elif f.FaceNormal.X != f.FaceNormal.Y:
                        if f.FaceNormal.Z > 0: # Face Xiên hướng lên
                            face_slant_up_area += round(f.Area*0.092903,3)
                        elif f.FaceNormal.Z < 0: # Face Xiên hướng xuống
                            face_slant_down_area += round(f.Area*0.092903,3)
                elif f.__class__.__name__ == 'RuledFace':
                    face_non_flat += round(f.Area*0.092903,3)
            face_area_string = face_area_string.format(face_hor_up_area,face_hor_down_area,face_ver_area,face_slant_up_area,face_slant_down_area,face_non_flat)
            
            pair.append(e)
            pair.append(volume)  
            pair.append(face_area_string)
            pair.append(e.__class__.__name__)  
            pairs.append(pair)
            
            face_list.append(faces)
            face_normal_list.append([f.FaceNormal for f in faces])       
        
        except Exception as ex:
            exceptions.append(ex)
            pass
    
    count_success = 0
    if write_param == True:
        TransactionManager.Instance.EnsureInTransaction(doc)
        for p in pairs:
            try: # Ghi Volume
                param = p[0].LookupParameter(param_volume)
                if param.StorageType == StorageType.Double:
                    param.Set(round(p[1]/0.0283168,3))
                elif param.StorageType == StorageType.String:
                    param.Set(str(round(p[1],3)))
            except Exception as ex:
                exceptions.append(ex)
                pass
            try: # ghi Face Area String
                param1 = p[0].LookupParameter(param_area)
                if param1.StorageType == StorageType.String:
                    param1.Set(str(p[2]))
            except Exception as ex:
                exceptions.append(ex)
                pass
            try: # ghi parater Face Area seperated
                for i in range(len(param_area_sep)):
                    try:
                        param2 = p[0].LookupParameter(param_area_sep[i])
                        if param2.StorageType == StorageType.Double:
                            param2.Set(round(float(p[2].split(';')[i])/0.092903,3))
                    except Exception as ex:
                        exceptions.append(ex.args[0])
                        pass
            except:
                pass

            count_success += 1       
        
        TransactionManager.Instance.TransactionTaskDone()  
	return pairs,"Succeeded write parameter {0}/{1} Elements".format(count_success,len(pairs)), exceptions#,, face_list, face_normal_list


def writeParameterValueSingle(e,paramName,value):	
    """writeParameterValueSingle 210915"""
    try:
        param = e.LookupParameter(paramName)
        param.Set(value)
    except:
        pass

def writeParameterValueMulti(elems,paramName,value):
    """writeParameterValueSingle210915"""
    res = []
    TransactionManager.Instance.EnsureInTransaction(doc)
    for e in elems:
        try:
            param = e.LookupParameter(paramName)
            param.Set(value)
        except:
            pass
        res += 1
	TransactionManager.Instance.TransactionTaskDone()
	return res
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
elems = UnwrapElement(IN[0])
ask_select = IN[1]
categories = IN[2].splitlines()
p_vol = IN[3]
ask_write_param = IN[4]
p_area = IN[5]
p_area_seperated = IN[6].splitlines()

if ask_select == True:
    OUT = get_volume_area(doc,elems,param_volume = p_vol, write_param = ask_write_param,param_area = p_area, param_area_sep = p_area_seperated) 
else:
    elems = []
    for cat in categories:
        try:
            elems.extend(getAllElementsOfCategory(doc,cat))
        except:
            pass
    OUT = get_volume_area(doc,elems,param_volume = p_vol, write_param = ask_write_param,param_area = p_area, param_area_sep = p_area_seperated) 
#elems, categories