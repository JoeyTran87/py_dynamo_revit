import os
import subprocess

revit_path = r"C:\Program Files\Autodesk\Revit 2020\Revit.exe"

ask = input("Bạn muốn mở Revit (y/n): ")
if ask.lower() == "y":
    subprocess.call([revit_path])
    # subprocess.Popen([revit_path])