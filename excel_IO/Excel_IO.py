import clr, time
clr.AddReference("Microsoft.Office.Interop.Excel")
# from System.Runtime.InteropServices import Marshal
import Microsoft.Office.Interop.Excel as Excel
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
def write_excel(excel_path,sheet_name,row,column,data):
    global debugger
    excel_app = Excel.ApplicationClass()
    excel_app.Visible = show_excel    
    workbook = excel_app.Workbooks.Open(excel_path)
    worksheets = workbook.Worksheets
    sheet = [worksheets(i+1) for i in range(worksheets.Count) if worksheets(i+1).Name == sheet_name][0]
    
    if data.__class__.__name__ == "str":
        sheet.Cells(row,column).Value = data   
    
    # workbook.Close(True,excel_path)
    excel_app.Save(excel_path)
    
    

excel_path = IN[0]
sheet_name = IN[1]
show_excel = IN[2]

debugger = []


# write excel:
write_excel(excel_path,sheet_name,10,10,"Data")

# dic_data = {}
# for r in range(1,row+1):
#     try:
#         dic_data[str(r)] = [sheet.Cells(r,c).Text for c in range(1,column+1)]
#         # debugger.append(sheet.Cells(r,column).Text)
#     except:
#         pass


# OUT = dic_data


# if not show_excel:
# 	time.sleep(5)
# 	excel_app.Quit()