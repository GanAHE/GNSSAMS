#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 重力场反演线程

@author: GanAH  2020/7/28.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import os

from PyQt5.QtCore import pyqtSignal, QThread

from database.database import Database
from geodeticSurvey import gravityFieldModel


class ActionInversionGravityField(QThread):
    infoEmit = pyqtSignal(str, str)
    overEmit = pyqtSignal()

    def __init__(self):
        super(ActionInversionGravityField, self).__init__()

    def setPara(self, dictPara):
        self.code = dictPara["code"]
        self.filePath = dictPara["filePath"]

    def run(self) -> None:
        if self.code == 101:
            self.inversionModel()
        else:
            self.sendInfo("T", "当前功能暂未开发")

        self.sendInfo("over", "")

    def inversionModel(self):
        # 实例化一个重力场对象
        gravity = gravityFieldModel.GravityField()
        Data = [89.75000, 113.50000, 8.78948]
        # 模拟数据读取并实时反演
        path = self.filePath
        savePath = os.path.abspath(Database.workspace+"/GravityModel")
        for i in range(2, 180):
            r = gravity.get_r(Data[1], Data[0])
            i_nRe = gravity.get_detCnmSnm(r, Data[1], Data[0], Data[2], i)
            for g in range(len(i_nRe)):
                LineStr = ""
                for k in range(len(i_nRe[0])):
                    if k < 2:
                        LineStr += " " + '{0:{1}<3}\t'.format(i_nRe[g][k], " ")
                    else:  # 长数据间隔写入
                        LineStr += "  " + '{0:{1}<22}\t'.format(i_nRe[g][k], " ")
                self.sendInfo("G",LineStr)
            # gravity.writePlus(savePath, i_nRe)
        # # 反演最大阶
        # N_max = 10
        #
        # # 实例化一个重力场对象
        # c = 1
        # controlM = 0
        # fileExit = False
        # with open(path, "r") as f:
        #     for line in f:
        #         lineList = list(map(float, line.split()))
        #         controlM += 1
        #         if lineList[1] != 0:
        #             for i in range(2, N_max):
        #                 c += 1
        #                 r = gravity.get_r(lineList[1], lineList[0])
        #                 i_nRe = gravity.get_detCnmSnm(r, 114, 30, lineList[2], i)
        #
        #                 print("当前阶:---\n", i_nRe)
        #                 if controlM % 2 == 0:
        #                     gravity.writePlus(savePath[1], i_nRe)
        #
        #                 else:
        #                     gravity.writePlus(savePath[0], i_nRe)
        #
        #                 if c > 10:
        #                     break
        # if controlM % 2 == 0:
        #     print("最终文件保存路径为：", savePath[1])
        # else:
        #     print("最终文件保存路径为：", savePath[0])

    def sendInfo(self, type, strInfo):
        if type == "over":
            self.overEmit.emit()
        else:
            self.infoEmit.emit(type, strInfo)

    def killThread(self):
        self.terminate()
