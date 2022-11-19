#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @ Date    : 2022/10/5 13:55
# @ Author  : paperClub
# @ Email   : paperclub@163.com
# @ Site    :


import xlwt

""" 设置xls文字颜色 """

filename = (u'paperclub.xls')
work_book = xlwt.Workbook()
sheet = work_book.add_sheet('sheet1')
style = "font:colour_index blue;"
red_style = xlwt.easyxf(style)

### 数据
data = [
    ["日期", "类目", "访问量"],
    ["2022-8-1", "paperclub", 200],
    ["2022-9-1", "paperclub", 200],
    ["2022-10-1", "paperclub", 200],
    ["2022-11-1", "paperclub", 200],
]

### 保存
row_count = len(data)
for row in range(row_count):
    col_count = len(data[row])
    for col in range(0, col_count):
        # 行颜色设置
        if row == 0:
            sheet.write(row, col, data[row][col], red_style)
        else:         # 表头下面的数据格式
            sheet.write(row, col, data[row][col])


work_book.save(filename)


from xlsxwriter.workbook import Workbook

workbook = Workbook(r'paperclub2.xlsx')
worksheet = workbook.add_worksheet()

style = {'valign': 'vcenter', # 垂直居中
         'text_wrap': False, # 自动换行
         }

red_style = workbook.add_format({'color': 'red'})
blue_style = workbook.add_format({'color': 'blue'})

row = 0
col = 0
for i, (date, item, value) in enumerate(data):
    string1 = item[:i+1]
    string2 = item[i+1: ]

    worksheet.write_string(row, col, date) # 列1
    item_rich_string = [string1, red_style, string2, blue_style] # 格式
    worksheet.write_rich_string(row, col+1, *item_rich_string) #列二

    worksheet.write_string(row, col+2, str(value)) # 列3
    row += 1

worksheet.freeze_panes(1, 0) # 冻结首行

workbook.close() # 记得关闭


