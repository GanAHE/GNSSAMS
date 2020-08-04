#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 解算重力异常

@author: GanAH  2020/7/29.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import csv

from PyQt5.QtCore import QThread, pyqtSignal

from database.database import Database
from geodeticSurvey import gravitySurvey
from geodeticSurvey.gravityFieldModel import GravityModel, GravityField
from geodeticSurvey.gravitySurvey import normalGravity
from window.file import operationFile


class ActionCacuGravityAnomaly(QThread):
    infoEmit = pyqtSignal(str, str)
    overEmit = pyqtSignal()

    def __init__(self):
        super(ActionCacuGravityAnomaly, self).__init__()

    def setPara(self, dictPara):
        self.code = dictPara["code"]
        self.filePath = dictPara["filePath"]
        self.fileType = dictPara["fileType"]
        self.modelFilePath = dictPara["modelFilePath"]
        self.normalFilePath = dictPara["fileNormalPath"]

    def run(self) -> None:
        if self.code == 201:
            self.measureDataCacu()
        else:
            self.gravityModelCacu()
        self.sendInfo("over", "")

    def measureDataCacu(self):
        if self.filePath is None:
            self.sendInfo("T", "缺少观测数据文件！")
        else:
            self.sendInfo("I", "测量数据解算中...")
            title = ["ID", "经度/°", "纬度/°", "高程/m", "测量重力值/mGal", "重力异常/mGal", "布格重力异常/mGal"]
            strTitle = ""
            for i in range(len(title)):
                if i == 0 or i == 3:
                    strTitle += " {0:{1}<6}\t".format(title[i], "")
                elif i > 0 and i < 3:
                    strTitle += "{0:{1}<12}\t".format(title[i], "")
                elif i == 4:
                    strTitle += "{0:{1}<16}\t".format(title[i], "")
                else:
                    strTitle += "{0:{1}<18}\t".format(title[i], "")
            self.sendInfo("G", strTitle)
            data = self.readFile(self.filePath)
            if len(data) > 0:
                for i in range(len(data)):
                    lineData = list(map(float, data[i][1:5]))
                    gravityAnomaly = lineData[3] - normalGravity(lineData[1], H=lineData[2])
                    gravityAnomaly_BG = lineData[3] - normalGravity(lineData[1], H=lineData[2] - 0.1116 * lineData[2])
                    data[i].append(gravityAnomaly)
                    data[i].append(gravityAnomaly_BG)
                    lineStr = ""
                    for l in range(len(data[i])):
                        if l == 0 or l == 3:
                            lineStr += " {0:{1}<6}\t".format(data[i][l], "")
                        elif l > 0 and l < 3:
                            lineStr += "{0:{1}<15}\t".format(data[i][l], "")
                        else:
                            lineStr += "{0:{1}<22}\t".format(data[i][l], "")
                    self.sendInfo("G", lineStr)
                # 循环结束，存入数据库
                Database.gravityAnomalyData = data
                # 发送绘图指令
                self.sendInfo("draw", "")

    def gravityModelCacu(self):
        if self.filePath is None:
            self.sendInfo("T", "缺少观测数据文件！")
        elif self.normalFilePath is None:
            self.sendInfo("T", "未导入正常位系数文件！")
        elif self.modelFilePath is None:
            self.sendInfo("T", "未导入模型文件！")
        else:
            self.sendInfo("I", "重力场模型解算中...")
            model = GravityModel(self.modelFilePath)
            N_model = GravityModel(self.normalFilePath)
            gravity = GravityField()
            title = ["ID", "经度/°", "纬度/°", "高程/m", "测量重力值/mGal", "重力异常/mGal"]
            strTitle = ""
            for i in range(len(title)):
                if i == 0:
                    strTitle += " {0:{1}<6}\t".format(title[i], "")
                elif i > 0 and i < 4:
                    strTitle += "{0:{1}<12}\t".format(title[i], "")
                elif i == 4:
                    strTitle += "{0:{1}<16}\t".format(title[i], "")
                else:
                    strTitle += "{0:{1}<22}\t".format(title[i], "")
            self.sendInfo("G", strTitle)
            data = self.readFile(self.filePath)
            if len(data) > 0:
                for i in range(len(data)):
                    lineData = list(map(float, data[i][1:5]))
                    r = gravity.get_r(lineData[0], lineData[1])
                    # go = GM / (r * r)
                    # print(gravity.model_N(model, r, lineData[0], lineData[1], go))
                    # print("向径", r, gravity.model_N(model, r, lineData[0], lineData[1], go))
                    teta_g = gravity.get_detg(model, N_model, r, lineData[0], lineData[1], 10)
                    data[i].append(teta_g * 100 * 10000)
                    lineStr = ""
                    for l in range(len(data[i])):
                        if l == 0:
                            lineStr += " {0:{1}<6}\t".format(data[i][l], "")
                        elif l > 0 and l < 4:
                            lineStr += "{0:{1}<15}\t".format(data[i][l], "")
                        else:
                            lineStr += "{0:{1}<22}\t".format(data[i][l], "")
                    self.sendInfo("G", lineStr)
                # 循环结束，存入数据库
                Database.gravityAnomalyData = data
                # 发送绘图指令
                self.sendInfo("draw", "")

    def readFile(self, filePath):
        data = []
        if self.fileType == "csv":
            count = 1
            with open(filePath, "r") as F:
                reader = csv.reader(F)
                for row in reader:
                    if count == 1:  # 列表栏
                        count = 2
                    else:
                        data.append(row)
            return data
        elif self.fileType == "txt":
            data = operationFile.OperationFile().readlargeFile(self.filePath)
            lists = []
            for i in range(1,len(data)):
                lists.append(data[i].split())
            return lists

    def sendInfo(self, type, strInfo):
        if type == "over":
            self.overEmit.emit()
        else:
            self.infoEmit.emit(type, strInfo)

    def killThread(self):
        self.terminate()
