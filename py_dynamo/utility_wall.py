

# Load the Python Standard and DesignScript Libraries
import os, sys, json,clr, tempfile,shutil

dynPyDir = r"\\hcmcfcfs01\databim$\BimESC\00-BIM STANDARD\PYTHON\pythondynamo"
sys.path.append(dynPyDir)
revitDir = r"C:\Program Files\Autodesk\Revit 2020"
sys.path.append(revitDir)
revitDynamoDir1 = r"C:\Program Files\Autodesk\Revit 2020\AddIns\DynamoForRevit\Revit"
revitDynamoDir2 = r"C:\Program Files\Autodesk\Revit 2020\AddIns\DynamoForRevit"
sys.path.append(revitDynamoDir1)
sys.path.append(revitDynamoDir2)

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
clr.ImportExtensions(Revit.GeometryConversion)

import Autodesk.Revit.DB.JoinGeometryUtils as JGU

import utility_common
from utility_common import *