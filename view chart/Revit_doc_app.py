import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
opt = Options()
#-------------------------------------------------------#

OUT = doc,uiapp,app,opt