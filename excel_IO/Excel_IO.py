import clr, time
clr.AddReference("Microsoft.Office.Interop.Excel")
# from System.Runtime.InteropServices import Marshal
import Microsoft.Office.Interop.Excel as Excel

excel_path = IN[0]
sheet_name = IN[1]

debugger = []

# Excel app đã khởi tạo + chạy ngầm
excel_app = Excel.ApplicationClass()
# Hiện Excel
excel_app.Visible = False

# Duyệt workbooks
workbook = excel_app.Workbooks
# Mở 1 file excel cụ thể
workbook = workbook.Open(excel_path)
worksheets = workbook.Worksheets
sheet = [worksheets(i+1) for i in range(worksheets.Count) if worksheets(i+1).Name == sheet_name][0]

row = 7
column = 2
dic_data = {}
for r in range(1,row+1):
    try:
        dic_data[str(r)] = [sheet.Cells(r,c).Text for c in range(1,column+1)]
        # debugger.append(sheet.Cells(r,column).Text)
    except:
        pass



OUT = dic_data

time.sleep(5)
excel_app.Quit()