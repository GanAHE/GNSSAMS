#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 稳定点组计算

@author: GanAH  2020/5/24.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from PyQt5.QtCore import pyqtSignal, QThread

from controlNetwork.stablePointGroup import StablePointGroup
from database.database import Database


class ActionStablePointGroup(QThread):
    infoEmit = pyqtSignal(str, str)
    paraEmit = pyqtSignal(float, float, float, float)
    overEmit = pyqtSignal()

    def __init__(self):
        super(ActionStablePointGroup, self).__init__()
        self.f = None
        # 比例系数步长
        self.step = None
        # 比例系数自动调整上限
        self.upValue = None
        # 共线判定阈值
        self.inLine = None

    def setPara(self, f, step, upValue, inLine):
        self.f = f
        self.step = step
        # 比例系数自动调整上限
        self.upValue = upValue
        # 共线判定阈值
        self.inLine = inLine

    def run(self) -> None:
        try:
            self._sendInfo("I", "导入数据库数据....")
            measure_I = Database.stableDotGroupMeasure_I
            measure_II = Database.stableDotGroupMeasure_II
            if len(measure_I) != 0:
                self._sendInfo("I", "开始进行稳定点组解算...")
                self._sendInfo("T", "  ========稳定点组解算报告======= \n")
                self._sendInfo("T", "  自适应调整比例系数 f ...... \n")
                self._sendInfo("T", "  遍历所有点值解算....... \n")
                stablePointGroup = StablePointGroup(measure_I, measure_II, self.inLine, self.f, self.step, self.upValue)
                # 分析
                stablePointGroup.dotGroupSearchAnalysis()
                # 获取稳定点组编号
                stablePointGroupNumber = stablePointGroup.getStablePointGroup()
                self._sendInfo("I", "稳定点组解算完成...")
                self._sendInfo("S", "解算结束！")
                self._sendInfo("T", "稳定点组编号:\n  " + str(stablePointGroupNumber))
                # 编号对应的组解析并存入数据库
                self.pointIndexToPointGroup(stablePointGroupNumber, measure_I, measure_II)
                # 结束,发送结束信号
                self._sendInfo("I", "完成稳定点组解算。")
                self._over()
            else:
                self._sendInfo("W", "待解算数据为空！")
                # 发送线程结束信息
                self._over()

        except Exception as e:
            self._sendInfo("E", "异常错误！详细信息：" + e.__str__())

    def _over(self):
        self.overEmit.emit()

    def _sendInfo(self, type, strInfo):
        """
        发送信号
        :param type: I-顶级界面输出信息；T：本层操作信息；E,W,O等为弹窗提示
        :param strInfo: 信息
        :return:
        """
        self.infoEmit.emit(type, strInfo)

    def pointIndexToPointGroup(self, stablePointGroupNumber, measure_I, measure_II):
        """
        按照编号获取对应稳点点组坐标信息
        :param stablePointGroupNumber:  二维Index List
        :return:
        """
        self._sendInfo("T", "\n===========【稳定点组解算】==============\n")
        self._sendInfo("T", " 1.稳定点组的解算受比例系数影响，解算时适当调整以达到最佳需求；\n 2.此区域为保存区，删改内容都将保存到导出的报告中。\n")
        self._sendInfo("T", " I_ID     X     Y    Z  | II_ID    X     Y    Z \n")
        for i in range(len(stablePointGroupNumber)):
            self._sendInfo("T", " - 第 " + str(i+1) + " 组：\n")
            for k in range(3):
                # resultList.append(measure_I[stablePointGroupNumber[i][k]] + measure_II[stablePointGroupNumber[i][k]])
                groupData = self._listPointCoorToStr(measure_I[stablePointGroupNumber[i][k]])
                self._sendInfo("T", groupData)

    def _listPointCoorToStr(self, list1):
        resultStr1 = " "
        for i in range(len(list1)):
            resultStr1 += str(list1[i]).replace("\n","")+" "
        resultStr1 += "\n"

        return resultStr1

    def killThread(self):
        self.terminate()
