# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import time
# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
controller = IN[0]
# Place your code below this line

while True:
    time.sleep(3)
    if not controller.lower() == "q":
        log = "Looping at {}".format(time.strptime("%d/%m%y %H:%M:%S",time.localtime(time.time())))
    else:        
        break
OUT = "End Loop"