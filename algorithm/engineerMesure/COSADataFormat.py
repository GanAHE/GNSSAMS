#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 科傻文件解析类

@author: GanAH  2020/4/7.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from window.file.operationFile import OperationFile


class COSADataFormat(object):
    def __init__(self, kesaData):
        self.fileData = kesaData

    def AnalysisKesaFileData(self, knownPointCount):
        """
        科傻文件分析
        :param knownPointCount:
        :return: 1.known_Error_point [] :已知固定误差与观测点；
                  2.
        """
        known_Error_point = []
        listTemp = []
        measureDict = {}
        pointIndex = []
        for i in range(len(self.fileData)):
            lineSplitData = ((self.fileData[i]).strip()).split(",")
            if lineSplitData[0]!="":
                listTemp.append(lineSplitData)

            if len(lineSplitData) == 1 and lineSplitData[0] != "":  # 测站号定位标
                pointIndex.append(i)
                measureDict[lineSplitData[0].strip()] = 0

        for i in range(pointIndex[0]):  # 固定误差与已知点数据
            lineSplitData = ((self.fileData[i]).strip()).split(",")
            if len(lineSplitData) > 1:
                known_Error_point.append(lineSplitData)
        count = 0

        # print("listTemp", listTemp)
        for key in measureDict.keys():  # 从获取的站点定位标循环获取站观测数据
            if count != len(pointIndex) - 1:
                measureDict[key] = self.mersureStationAnalysis(listTemp[pointIndex[count] + 1:pointIndex[count + 1]])
            else:
                measureDict[key] = self.mersureStationAnalysis(listTemp[pointIndex[count] + 1:])
            count += 1

        # print("初始",measureDict)
        return known_Error_point, measureDict

    def mersureStationAnalysis(self, listLineData):
        # print("laie",listLineData)
        for i in range(len(listLineData)):
            if (listLineData[i][1]).upper() == "L" or "A":  # 观测类型为方向观测值/坐标方位角
                angle_s = ((listLineData[i][2]).strip()).split(".")
                # print("sfg", angle_s)
                degree = (float(angle_s[0]) + float((angle_s[1])[:2]) / 60 +
                          float((angle_s[1])[3:5] + "." + (angle_s[1])[5:]) / 3600
                          )
                listLineData[i][2] = str(degree)
                # 转换单位并更新
        return listLineData
