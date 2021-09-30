import clr, sys, os
# print(help(clr))
dynPyDir = r"C:\Program Files\Autodesk\Revit 2020\AddIns\DynamoForRevit"#"\\hcmcfcfs01\databim$\BimESC\00-BIM STANDARD\PYTHON\dotNet\references"
sys.path.append(dynPyDir)
dynPyDir2 = r"C:\Program Files\Autodesk\Revit 2020\AddIns\DynamoForRevit\Revit"#"\\hcmcfcfs01\databim$\BimESC\00-BIM STANDARD\PYTHON\dotNet\references"
sys.path.append(dynPyDir2)
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('DSCoreNodes')
from DSCore import Math

clr.AddReference('ProtoGeometry')
import Autodesk
import Autodesk.DesignScript
import Autodesk.DesignScript.Geometry
from Autodesk.DesignScript.Geometry import *
path1 = os.path.abspath(Autodesk.DesignScript.__file__)
path2 = os.path.dirname(Autodesk.DesignScript.Geometry.__file__)


# print(dir(Autodesk.DesignScript.Geometry))
"""['Application', 'Arc', 'BoundingBox', 'Circle', 'CoEdge', 'Cone', 'CoordinateSystem', 'Core', 'Cuboid', 'Curve', 'Cylinder', 'DesignScriptEntity', 'Edge', 'Ellipse', 'EllipseArc', 'Face', 'Geometry', 'GeometryExtension', 'Helix', 'HostFactory', 'IProtoGeometryConfiguration', 'IndexGroup', 'Line', 'Loop', 'Mesh', 'NurbsCurve', 'NurbsSurface', 'Plane', 'Point', 'PolyCurve', 'PolySurface', 'Polygon', 'ProtoGeometryConfiguration', 'Rectangle', 'Solid', 'Sphere', 'Surface', 'TSpline', 'Topology', 'UV', 'Vector', 'Vertex']
PS C:\Users\USER\Documents\GitHub\cofico\cofico\FROM BIM MASTER TEMP 210412\Python\pythonDynamo>"""
# print(help(Autodesk.DesignScript.Geometry))
"""Geometry = class namespace#(MemberTracker)
 |  Method resolution order:
 |      namespace#
 |      MemberTracker
 |      object
 |
 |  Methods defined here:
 |
 |  __getitem__(...)
 |      x.__getitem__(y) <==> x[y]
 |
 |  __iter__(...)
 |      __iter__(self: IEnumerable) -> object
 |
 |  __new__(...)
 |      __new__(cls: type, name: str)
 |
 |  __repr__(...)
 |      __repr__(self: namespace#) -> str
 |
 |  __str__(...)
 |      x.__str__() <==> str(x)
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      Get: __dict__(self: namespace#) -> dict
 |
 |  ----------------------------------------------------------------------
 |  Methods inherited from MemberTracker:
 |
 |  BindToInstance(...)
 |      BindToInstance(self: MemberTracker, instance: DynamicMetaObject) -> MemberTracker
 |
 |  FromMemberInfo(...)
 |      FromMemberInfo(member: MemberInfo, extending: Type) -> MemberTracker
 |      FromMemberInfo(member: MemberInfo) -> MemberTracker
 |
 |  GetBoundError(...)
 |      GetBoundError(self: MemberTracker, binder: ActionBinder, instance: DynamicMetaObject, instanceType: Type) -> ErrorInfo
 |
 |  GetBoundValue(...)
 |      GetBoundValue(self: MemberTracker, resolverFactory: OverloadResolverFactory, binder: ActionBinder, instanceType: Type, instance: DynamicMetaObject) -> DynamicMetaObject
 |
 |  GetError(...)
 |      GetError(self: MemberTracker, binder: ActionBinder, instanceType: Type) -> ErrorInfo
 |
 |  GetValue(...)
 |      GetValue(self: MemberTracker, resolverFactory: OverloadResolverFactory, binder: ActionBinder, instanceType: Type) -> DynamicMetaObject
 |
 |  SetBoundValue(...)
 |      SetBoundValue(self: MemberTracker, resolverFactory: OverloadResolverFactory, binder: ActionBinder, instanceType: Type, value: DynamicMetaObject, instance: DynamicMetaObject, errorSuggestion: DynamicMetaObject) -> DynamicMetaObject
 |      SetBoundValue(self: MemberTracker, resolverFactory: OverloadResolverFactory, binder: ActionBinder, instanceType: Type, value: DynamicMetaObject, instance: DynamicMetaObject) -> DynamicMetaObject   
 |
 |  SetValue(...)
 |      SetValue(self: MemberTracker, resolverFactory: OverloadResolverFactory, binder: ActionBinder, instanceType: Type, value: DynamicMetaObject, errorSuggestion: DynamicMetaObject) -> DynamicMetaObject 
 |      SetValue(self: MemberTracker, resolverFactory: OverloadResolverFactory, binder: ActionBinder, instanceType: Type, value: DynamicMetaObject) -> DynamicMetaObject
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from MemberTracker:
 |
 |  DeclaringType
 |      Get: DeclaringType(self: MemberTracker) -> Type
 |
 |  EmptyTrackers
 |
 |  MemberType
 |      Get: MemberType(self: MemberTracker) -> TrackerTypes
 |
 |  Name
 |      Get: Name(self: MemberTracker) -> str
 |
 |  ----------------------------------------------------------------------
 |  Methods inherited from IEnumerable[KeyValuePair[str, object]]:
 |
 |  __contains__(...)
 |      __contains__[KeyValuePair[str, object]](enumerable: IEnumerable[KeyValuePair[str, object]], value: KeyValuePair[str, object]) -> bool

None"""


# print (clr.References)
"""
(<mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089>,
<System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089>,
<IronPython.SQLite, Version=2.7.0.40, Culture=neutral, PublicKeyToken=7f709c5b713576e1>,
<IronPython.Wpf, Version=2.7.0.40, Culture=neutral, PublicKeyToken=7f709c5b713576e1>,
<RevitNodes, Version=2.1.0.7733, Culture=neutral, PublicKeyToken=null>,
<ProtoGeometry, Version=2.1.0.23964, Culture=neutral, PublicKeyToken=null>)
"""
# print (dir(clr.References[4].Autodesk.DesignScript.Geometry))
"""
['Application', 'Arc', 'BoundingBox', 'Circle', 'CoEdge', 'Cone', 'CoordinateSystem', 'Core', 'Cuboid', 'Curve', 'Cylinder', 
'DesignScriptEntity', 'Edge', 'Ellipse', 'EllipseArc', 'Face', 'Geometry', 'GeometryExtension', 'Helix', 'HostFactory', 'IProtoGeometryConfiguration', 'IndexGroup', 'Line', 'Loop', 'Mesh', 'NurbsCurve', 'NurbsSurface', 'Plane', 'Point', 'PolyCurve', 
'PolySurface', 'Polygon', 'ProtoGeometryConfiguration', 'Rectangle', 'Solid', 'Sphere', 'Surface', 'TSpline', 'Topology', 'UV', 'Vector', 'Vertex']
"""
# print (dir(clr.References[4].Autodesk.DesignScript.Geometry.Solid))
"""
['Approximate', 'Area', 'BoundingBox', 'ByJoinedSurfaces', 'ByLoft', 'ByRevolve', 'BySweep', 'BySweep2Rails', 'ByUnion', 'Centroid', 'Chamfer', 'CheckArgsForAsmExtents', 'ClosestPointTo', 'ComputeHashCode', 'ContextCoordinateSystem', 'DeserializeFromSAB', 'Difference', 'DifferenceAll', 'Dispose', 'DisposeDisplayable', 'DistanceTo', 'DoesIntersect', 'Edges', 'Equals', 'Explode', 'ExportToSAT', 'Faces', 'Fillet', 'FromNativePointer', 'FromObject', 'FromSolidDef', 'GetHashCode', 'GetType', 'ImportFromSAT', 'Intersect', 'IntersectAll', 'IsAlmostEqualTo', 'MemberwiseClone', 'Mirror', 'ProjectInputOnto', 'ReferenceEquals', 
'Rotate', 'Scale', 'Scale1D', 'Scale2D', 'SerializeAsSAB', 'Split', 'Tags', 'Tessellate', 'ThinShell', 'ToNativePointer', 'ToSolidDef', 'ToString', 'Transform', 'Translate', 'Trim', 'Union', 'UnionAll', 'UpdateDisplay', 'Vertices', 'Volume', '__class__', '__delattr__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__getattribute__', '__hash__', '__init__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'mConstructor', 'scaleFactor']
"""
# print(help(Solid))
