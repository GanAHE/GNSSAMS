#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:文件处理类

@author: GanAH  2019/9/24.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import os
import csv

class OperationFile():

    def __init__(self):
        pass

    def readsmallFile(self, filePath):
        """
        打开小文件（快速）
        :param filePath: 文件路径
        :return: data--list
        """
        with open(filePath, 'r') as f:
            for line in f:
                # 不适合操作大型文件
                data = f.readlines()
        f.close()
        return data

    def readlargeFile(self, filePath):
        """
        大文件读取
        :param filePath:filePath
        :return: data--list
        """
        with open(filePath, 'r') as f:
            data = []
            for line in f:
                data.append(line)
        f.close()
        return data

    def writeTXTFile(self, strData, filePath):
        """
        写入文本数据
        :param filePath:文件路径及文件名
        :return:None
        """
        with open(filePath,'w') as txtFile:
            txtFile.flush() # 缓冲区
            for line in strData:
                txtFile.write(line)
            os.fsync(txtFile)
            txtFile.close()

    def writeCSVFile(self,listData,filePath,headList = None):
        """
        写入CSV数据
        :param listData: list文件
        :param filePath: 文件路径及文件名
        :param headList: csv的标题，作为可选参数
        :return: None
        """
        with open(filePath,'w',newline="") as csvFile:
            csvFile.flush()
            csvWriter = csv.writer(csvFile)
            if headList is not None:
                csvWriter.writerow(headList)
            try: # 无奈之举，只有一行list该怎么判断？即内部不嵌套
                for i in range(len(listData)):
                    csvWriter.writerow(listData[i])
            except:
                csvWriter.writerow(listData)

            os.fsync(csvFile)
            csvFile.close()