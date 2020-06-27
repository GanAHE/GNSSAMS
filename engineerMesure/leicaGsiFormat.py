#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 徕卡Gsi数据格式解析

@author: GanAH  2020/3/21.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""


class LeicaGSIFormat():

    def __init__(self, strSourceGSI):
        """
        GSI - 8
        :param strSourceGSI:
        """
        self.GISSourceData = strSourceGSI
        self.mersureModel = None

        self.GSIAnalysis()

    def GSIAnalysis(self):
        self.controlStationPointID_groundHeight = []
        self.intermediateStation = []
        self.stationCaculatorResult = []

        for i in range(len(self.GISSourceData)):
            lineSplitData = (self.GISSourceData[i].strip()).split()
            lineLenght = len(lineSplitData)
            if lineLenght == 1:
                """
                # 测量模式
                # 需要增添不同测量模式的数据读取在此添加
                
                <p> 此方式当前为特殊读取方式，后续可自行完善--> 魔法值变量化即可
                """
                if lineSplitData[0][-1:] == "2":  # BFFB 模式
                    self.mersureModel = "BFFB"

            elif lineLenght == 2:
                # 测段信息数据
                self.controlStationPointID_groundHeight.append([lineSplitData[0][-3:],lineSplitData[1][-4:]])
            else:
                # 进入测段观测数据
                if i == 2 or lineLenght == 5:  # 注意顺序
                    # 测量数据
                    self.intermediateStation.append([
                        lineSplitData[0][-2:],
                        lineSplitData[1][8:13] + "." + lineSplitData[1][-2:], # 单位为 0.01 mm，转为1 mm
                        lineSplitData[2][9:], # + "." + lineSplitData[2][-2:]
                        lineSplitData[3][-4:],
                        lineSplitData[4][-3:-2] + "."+lineSplitData[4][-2:]
                    ])
                elif lineLenght == 6 and i != 2:
                    # 解算数据 : 符号位 + 毫米级别数据值
                    self.stationCaculatorResult.append([
                        lineSplitData[0][-2:],
                        lineSplitData[1][6]+lineSplitData[1][-3:-2]+ "." + lineSplitData[1][-2:],
                        lineSplitData[2][6]+lineSplitData[2][-3:-2]+ "." + lineSplitData[2][-2:],
                        lineSplitData[3][6]+lineSplitData[3][8:13]+ "." + lineSplitData[3][-2:],
                        lineSplitData[4][6]+lineSplitData[4][8:13]+ "." + lineSplitData[4][-2:],
                        lineSplitData[5][6]+lineSplitData[5][8:13]+ "." + lineSplitData[5][-2:],
                    ])

    def getAnalysisDict(self):
        return {"model": self.mersureModel,
                "ID": self.controlStationPointID_groundHeight,
                "data": self.intermediateStation,
                "calculator": self.stationCaculatorResult
                }

