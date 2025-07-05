'''
同步周计划的日程安排到飞书日历上
'''

from openpyxlOperateExcel import ExcelOperation

def enterFunc():
    url = r"E:\资料库\2025周计划集合.xlsx"
    excelData = ExcelOperation(path=url)
    excelData.getAllSheets()
    excelData.splitScheduleInfo()

enterFunc()
