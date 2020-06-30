from docx import Document, table
import os
from win32com import client


# def doc2pdf(doc_name, pdf_name):
#     """
#     :word文件转pdf
#     :param doc_name word文件名称
#     :param pdf_name 转换后pdf文件名称
#     """
#     try:
#         word = client.DispatchEx("Word.Application")
#         if os.path.exists(pdf_name):
#             os.remove(pdf_name)
#         worddoc = word.Documents.Open(doc_name, ReadOnly=1)
#         worddoc.SaveAs(pdf_name, FileFormat=17)
#         worddoc.Close()
#         return pdf_name
#     except:
#         return 1
#
#
# docx = Document("E:\\CodePrograme\\Python\\EMACS\source\\template\\leica.docx")
# tables = docx.tables
# rows = tables[0].rows
# cols = rows[4].cells
# cell = cols[1]
# cols[9].text = "写进去测试测试"
# text = cell.text
#
# print("go")
# print("测试-", text)
# for tabl in tables[:]:
#     for i, row in enumerate(tabl.rows[:]):  # 读每行
#         row_content = []
#         for cell in row.cells[:]:  # 读一行中的所有单元格
#             c = cell.text
#             row_content.append(c)
#         print(row_content)  # 以列表形式导出每一行数据
#
# docx.save("E:\\CodePrograme\\Python\\EMACS\source\\template\\tet.docx")
from database.database import Database
a = Database()
a.loadConfigJson()
b = Database()
print(b.elliDict,b.workspace,Database.elliDict,Database.workspace)