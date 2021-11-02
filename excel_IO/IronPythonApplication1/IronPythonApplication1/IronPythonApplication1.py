import clr

clr.AddReference("Microsoft.Office.Interop.Excel")

from Microsoft.Office.Interop import Excel

xlApp = Excel.ApplicationClass()

xlApp.Visible = True

workbook = xlApp.Workbooks.Add()

worksheet = workbook.Worksheets['Sheet1']

print(workbook.Name)
print(worksheet.Name)