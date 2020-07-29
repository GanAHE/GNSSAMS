#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: GanAH  2019/10/13.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import os

from PyQt5 import QtWidgets, QtCore

from database.database import Database
from window.file.operationFile import OperationFile


class FileMsg(QtCore.QObject):
    def __init__(self, parentPanel):
        """
        初始化
        :param parentPanel: centerWight
        """
        # super(FileMsg, parent=None).__init__()
        self.centerPanel = parentPanel

    def openFile(self):
        """
        打开文件对话框
        :return:dataList
        """
        filePath, ok = QtWidgets.QFileDialog.getOpenFileName(self.centerPanel, "打开", Database.workspace,
                                                             "All Files (*);;Text Files (*.txt);;Leica GSI (*.gsi);;Kesa IN2 (*.in2)")

        if filePath != "":
            dataList = OperationFile().readlargeFile(filePath)
            # dirPath = os.path.dirname(os.path.realpath(filePath))  # 除开文件名的路径
            return dataList, filePath
        else:
            return None

    def writeFile(self, type,data):
        """
        保存文件对话框
        :param data:需要写入的数据
        :return:
        """
        if type == "txt":
            fileFilter = "Text Files (*.txt)"
        elif type == "csv":
            fileFilter = "CSV Files (*.csv)"
        elif type == "docx":
            fileFilter = "Docx Files(*.docx)"
        else:
            fileFilter = "All Files (*);;Text Files (*.txt);;Docx Files(*.docx);;CSV Files (*.csv)"

        filePath, ok = QtWidgets.QFileDialog.getSaveFileName(self.centerPanel, "打开", Database.workspace,fileFilter)

        if type == "txt":
            OperationFile().writeTXTFile(data, filePath)
        else:
            pass

    def getWriteFilePath(self, type):
        """
        仅获取路径及文件名，自定义写入方式
        :param type: 指定保存的str文件类型，目前有 txt | docx | csv 其他默认
        :return: filePath
        """
        if type == "txt":
            fileFilter = "Text Files (*.txt)"
        elif type == "csv":
            fileFilter = "CSV Files (*.csv)"
        elif type == "docx":
            fileFilter = "Docx Files(*.docx)"
        else:
            fileFilter = "All Files (*);;Text Files (*.txt);;Docx Files(*.docx);;CSV Files (*.csv)"

        filePath, ok = QtWidgets.QFileDialog.getSaveFileName(self.centerPanel, "保存为 (Save as)", "./source/", fileFilter)

        return filePath
