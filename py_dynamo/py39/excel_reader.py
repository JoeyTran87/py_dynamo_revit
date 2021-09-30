import sys,getopt
import pandas as pd


if __name__ == '__main__':
    """"""
    path = None
    sheet_name = None
    try:
        opts,_ = getopt.getopt(sys.argv[1:],'p:n:',['-path','-sheetname'])
        pass
    except:
        sys.exit()
    for opt,arg in opts:
        if opt in ['-p','-path']:
            path = arg#r'K:\_WFH ACREDO\MPP\ACC2101(Accredo_Asia)_LOA_210510.xlsx'
            
        if opt in ['-n','-sheetname']:
            sheet_name = arg#'SCHEDULE_LOA_210510'
    print(f"{path}\n{sheet_name}")
    if path != None and sheet_name != None:
        df = pd.read_excel(path,sheet_name=sheet_name).fillna('_')
        print(df)
    # sys.exit()
print(sys.argv)