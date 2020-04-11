#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 控制网

@author: GanAH  2020/4/7.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from PyQt5.QtCore import pyqtSignal, QThread

from algorithm.common.BasicMeasurementAlgorithm import BasicMeasurementAlgorithm
from algorithm.engineerMesure.COSADataFormat import COSADataFormat
from database.database import Database


class ActionTwoDissControlNet(QThread):
    infoEmit = pyqtSignal(str, str)
    setParaEmit = pyqtSignal(int)
    overEmit = pyqtSignal()

    def __init__(self):
        super(ActionTwoDissControlNet, self).__init__()
        self.setParaEmit.connect(self.setPara)

    def setPara(self, intCount):
        self.knownPointCount = intCount

    def run(self) -> None:
        self._controlNetAdjustment()

    def _controlNetAdjustment(self):
        # 从数据库获取数据
        sourceFileData = Database.COSAControlNetMersureData
        # 解析
        kesaDataFormatAnalysis = COSADataFormat(sourceFileData)
        error_knownPoint, stationDict = kesaDataFormatAnalysis.AnalysisKesaFileData(self.knownPointCount)
        print(error_knownPoint)
        knownPointCoor = error_knownPoint[1:]
        print(knownPointCoor)
        stationCount = 0
        for key in stationDict.keys():
            stationCount += 1
            stationList = stationDict[key]
            stationMersureCount = len(stationList)
            for i in range(stationMersureCount):  # 遍历测站观测列表
                pointMersure = []
                control = 0
                for k in range(i + 1, stationMersureCount):  # 以测站观测列表一个目标为基准，查找该目标的其他观测量
                    if stationList[i][0] == stationList[k][0]:
                        if control == 0:  # 第一次，加入目标基础信息+其他观测信息
                            pointMersure += (stationList[i] + stationList[k][1:])
                            control = 1  # 标记，第一次已完成
                        else:  # 非第一次，追加该点其他观测信息
                            pointMersure += stationList[k][1:]

                    # else:
                    #     pointMersure.append([stationList[i] + ["None", "0"]])
                print("测站:" + key, "观测目标-值:", pointMersure)
                if len(pointMersure) == 5:
                    """
                    # 计算近似坐标，算法需要改进到各种情况
                    # 或是对原始文件做出更为严格的限定！
                    """
                    for station in range(len(knownPointCoor)):
                        if knownPointCoor[station][0] == key:
                            print("Jinalile??")
                            basicCalc = BasicMeasurementAlgorithm()
                            angle = float(pointMersure[2]) + 0.000
                            Xo,Yo = basicCalc.coorForwarkCaclulator(angle, float(pointMersure[4]),
                                                                       float(knownPointCoor[station][1]),
                                                                       float(knownPointCoor[station][2]))
                            knownPointCoor.append([pointMersure[0],Xo,Yo])
                            print("近似坐标", Xo,Yo,knownPointCoor)
                            print("-" * 10 + "\n")

    def killThead(self):
        self.terminate()
