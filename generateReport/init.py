'''
    报告生成：从数据源生成报告
'''

import pandas as pd
from fakeData import generate_social_media_data
from dataLoader import DataLoader
from excelReporter import generate_excel_report
from wordReporter import generate_word_report

def enterFunc():
    # 生成与社交媒体相关的虚假数据
    generate_social_media_data()

    # 加载数据
    data = DataLoader.load_csv('social_media.csv')

    # 分组汇总
    # data['Date'] = pd.to_datetime(data['发布时间'])
    # monthly_sales = data.groupby(pd.Grouper(key='Date', freq='ME')).sum()

    # 生成各种格式报告
    generate_excel_report(data, 'monthly_sales_report.xlsx')
    generate_word_report(data, 'monthly_sales_report.docx')

    print("所有报告生成完成！")

enterFunc()