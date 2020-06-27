from docx import Document, table
import os
from win32com import client


def doc2pdf(doc_name, pdf_name):
    """
    :word文件转pdf
    :param doc_name word文件名称
    :param pdf_name 转换后pdf文件名称
    """
    try:
        word = client.DispatchEx("Word.Application")
        if os.path.exists(pdf_name):
            os.remove(pdf_name)
        worddoc = word.Documents.Open(doc_name, ReadOnly=1)
        worddoc.SaveAs(pdf_name, FileFormat=17)
        worddoc.Close()
        return pdf_name
    except:
        return 1


docx = Document("E:\\CodePrograme\\Python\\EMACS\source\\template\\leica.docx")
tables = docx.tables
rows = tables[0].rows
cols = rows[4].cells
cell = cols[1]
cols[9].text = "写进去测试测试"
text = cell.text

print("go")
print("测试-", text)
for tabl in tables[:]:
    for i, row in enumerate(tabl.rows[:]):  # 读每行
        row_content = []
        for cell in row.cells[:]:  # 读一行中的所有单元格
            c = cell.text
            row_content.append(c)
        print(row_content)  # 以列表形式导出每一行数据

docx.save("E:\\CodePrograme\\Python\\EMACS\source\\template\\tet.docx")

#
# doc2pdf("E:\\CodePrograme\\Python\\EMACS\source\\template\\leica.docx","E:\\CodePrograme\\Python\\EMACS\source\\template\\leica.pdf")


# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# """
# comment:
#
# @author: GanAH  2020/3/20.
# @version 1.0.
# @contact: dinggan@whu.edu.cn
# """
# from HTMLTable import HTMLTable
#
# # 标题
# table = HTMLTable(caption='果园收成表')
# # 表头行
# table.append_header_rows((
#     ('名称',    '产量 (吨)',    '环比',             ''),
#     ('',        '',             '增长量 (吨)',      '增长率 (%)'),
# ))
# # 合并单元格
# table[0][0].attr.rowspan = 2
# table[0][1].attr.rowspan = 2
# table[0][2].attr.colspan = 2
#
# # 数据行
# table.append_data_rows((
#     ('荔枝', 11, 1, 10),
#     ('芒果', 9, -1, -10),
#     ('香蕉', 6, 1, 20),
# ))
#
# # 标题样式
# table.caption.set_style({
#     'font-size': '15px',
# })
#
# # 表格样式，即<table>标签样式
# table.set_style({
#     'border-collapse': 'collapse',
#     'word-break': 'keep-all',
#     'white-space': 'nowrap',
#     'font-size': '14px',
# })
#
# # 统一设置所有单元格样式，<td>或<th>
# table.set_cell_style({
#     'border-color': '#000',
#     'border-width': '1px',
#     'border-style': 'solid',
#     'padding': '5px',
# })
#
# # 表头样式
# table.set_header_row_style({
#     'color': '#fff',
#     'background-color': '#48a6fb',
#     'font-size': '18px',
# })
#
# # 覆盖表头单元格字体样式
# table.set_header_cell_style({
#     'padding': '15px',
# })
# # 调小次表头字体大小
# table[1].set_cell_style({
#     'padding': '8px',
#     'font-size': '15px',
# })
# # 遍历数据行，如果增长量为负，标红背景颜色
# for row in table.iter_data_rows():
#     if row[2].value < 0:
#         row.set_style({
#             'background-color': '#ffdddd',
#         })
# html = table.to_html()
# print(html)
#
