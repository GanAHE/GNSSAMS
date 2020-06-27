#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: GanAH  2019/10/13.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from window.file import operationFile
from dataFilter.DataFilter import DataFilter
from algorithm.orbetEtc.SatelliteOrbetEtc import SatelliteOrbetEtc
from database import database


def actionCalcuSatLocatin(filePath):
    sourcedata = operationFile.OperationFile().readsmallFile(filePath)

    PRN_time, filterData = DataFilter.staLocation(sourcedata)

    result = DataFilter().twoMISstringToFloat(filterData)
    database.Database().sourceData = result
    self.sourceText.append("文件路径:" + filePath + "\n")
    self.sourceText.append("[注:暂定固定绝对路径，后期修改！]\n")
    self.sourceText.append("_----数据提取结果----_")
    for i in range(7):
        self.sourceText.append("---广播轨道" + str(i + 1) + "---\n")
        for j in range(4):
            self.sourceText.append(str(filterData[i][j] + "\n"))

    t = [79439.9315768461, 86279.9237728612, 83099.9292294162]
    # 存储数据
    positionOFSTA = [[0] * 3 for ge in range(3)]
    for i in range(3):
        positionOFSTA[i] = SatelliteOrbetEtc().orbetEtc(t[i], result)

    # 结果界面输出
    self.resultText.append("\t---当前历元计算----")
    for i in range(3):
        self.resultText.append("\n-当前时刻 t = " + str(t[i]) + "s 时,瞬时瞬时地球坐标为：")
        self.resultText.append("X = " + str(positionOFSTA[i][0]))
        self.resultText.append("Y = " + str(positionOFSTA[i][1]))
        self.resultText.append("Z = " + str(positionOFSTA[i][2]))

    self.resultText.append("    =====================")
    self.resultText.append("    《-------王 定 敢--------》")
    self.resultText.append("  未完成：\n"
                           "  1.MVC设计模式构架；\n"
                           "  2.文件选择器；\n"
                           "  3.绘制图像；\n"
                           "  4.卫星钟差的相对论效应改正及输出等等。\n")


"""
# def calculate(self):
#
#     positionOFSTA = [[0] * 3 for ge in range(3)]
#     t = [79439.9315768461, 86279.9237728612, 83099.9292294162]
#     for i in range(3):
#         print(database.database().sourceData)
#         positionOFSTA[i] = satelliteOrbetEtc().orbetEtc(t[i], database.database().sourceData)
#         print("测试"+positionOFSTA[i])
#     # 结果界面输出
#     self.resultText.append("\t---当前历元计算----")
#     for i in range(3):
#         self.resultText.append("当前时刻t=" + str(t[i]) + " s的瞬时瞬时地球坐标为：")
#         self.resultText.append("X = " + str(positionOFSTA[i][0]))
#         self.resultText.append("Y = " + str(positionOFSTA[i][1]))
#         self.resultText.append("Z = " + str(positionOFSTA[i][2]))
"""
