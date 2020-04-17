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
from myConfig.logger import Logger


class ActionTwoDissControlNet(QThread):
    infoEmit = pyqtSignal(str)
    setParaEmit = pyqtSignal(int)
    overEmit = pyqtSignal()
    logger = Logger().get_logger("TWO_DISS_CONTROLNET")

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
        error_knownPoint, stationDict = kesaDataFormatAnalysis.AnalysisKesaFileData()
        self._setText(" 1.固定误差与已知点坐标" + str(error_knownPoint))
        self.knownPointCoor = error_knownPoint[1:]
        # print(knownPointCoor)
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
                print(" 测站: " + key, " 观测目标-值:", pointMersure)
                if len(pointMersure) > 1:
                    self._setText("  测站号" + str(i) + "观测序" + str(k) + " 当前解算测站:" + key + "，观测目标信息:" + str(pointMersure))
                if len(pointMersure) >= 5:
                    """
                    # 计算近似坐标，算法需要改进到各种情况
                    # 或是对原始文件做出更为严格的限定！
                    """
                    for station in range(len(self.knownPointCoor)):
                        if self.knownPointCoor[station][0] == key:
                            basicCalc = BasicMeasurementAlgorithm()
                            """
                            # 这里出了问题！！！！！！！！坐标方位角的计算与传递
                            """
                            angle = float(pointMersure[2]) + 0.000  # 坐标方位角
                            Xo, Yo = basicCalc.coorForwarkCaclulator(angle, float(pointMersure[4]),
                                                                     float(self.knownPointCoor[station][1]),
                                                                     float(self.knownPointCoor[station][2]))
                            self.setKnownPoint([pointMersure[0], Xo, Yo])
                            print("近似坐标", Xo, Yo, self.knownPointCoor)
                            print("-" * 10 + "\n")
                            self._setText(
                                " 当前点近似坐标:" + pointMersure[0] + " (" + str(Xo) + "," + str(
                                    Yo) + ") ")
                            self._setText(" 近似点坐标列表更新：")
                            for lens in range(len(self.knownPointCoor)):
                                self._setText(" " + str(self.knownPointCoor[lens]))
                            self._setText("-" * 10 + "\n")

        # 结束，发送关闭线程指令
        self.logger.info("结束网平差解算，关闭线程")
        self._setText("网平差解算近似坐标完成，关闭线程")
        self.overEmit.emit()

    def setKnownPoint(self, pointList):
        for i in range(len(self.knownPointCoor)):
            print("死循环？", len(self.knownPointCoor), pointList, self.knownPointCoor)
            if pointList[0] == self.knownPointCoor[i][0]:
                self.knownPointCoor[i][1] = str((float(self.knownPointCoor[i][1]) + float(pointList[1])) / 2)
                self.knownPointCoor[i][2] = str((float(self.knownPointCoor[i][2]) + float(pointList[2])) / 2)
                break
            elif i == len(self.knownPointCoor) - 1:
                self.knownPointCoor.append(pointList)
                break

    def _setText(self, text):
        self.infoEmit.emit(text)

    def killThead(self):
        self.terminate()
