import clr
import math
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 

print(dir(__revit__))
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

print(doc.PathName.split("\\")[-1])

collector = FilteredElementCollector (doc)

categories = ["Walls","Doors","Windows","Roofs"]

elements = []

for e in collector.WhereElementIsNotElementType().ToElements():
	try:
		if e.Category.Name in categories:
			elements.append(e)
			print("{0} : {1}".format(e.Category.Name,e.UniqueId)) 
	except:
		pass
t = Transaction(doc, 'Copy') 
t.Start() 
#perform some action here...
#copy element
for e in elements:
	try:
		ElementTransformUtils.CopyElement(doc,e.Id,XYZ(20000/304.8,0,0))
		doc.Delete(e.Id)
	except Exception as ex:
		print (ex)
	
t.Commit()

#close the script window
#__window__.Close()