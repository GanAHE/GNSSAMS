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
from scipy import integrate
from numpy import sin, cos, pi

from database.database import Database
from geodeticSurvey import gravityFieldModel
from geodeticSurvey.legendre import Legendre


class ActionInversionGravityField(QThread):
    infoEmit = pyqtSignal(str, str)
    overEmit = pyqtSignal()
    processEmit = pyqtSignal(int, int)
    ellpsoid = None

    def __init__(self):
        super(ActionInversionGravityField, self).__init__()

    def setPara(self, dictPara):
        self.code = dictPara["code"]
        self.filePath = dictPara["filePath"]
        self.save = dictPara["autoSave"]
        self.N = dictPara["N"]
        self.ellpsoid = Database.ellipsoid.WGS84
        self.legendre = Legendre()

    def run(self) -> None:
        if self.code == 101:
            self.sendInfo("I", "开始重力场反演....")
            self.inversionModel()
            self.sendInfo("T", "重力场反演完成")
        else:
            self.sendInfo("T", "当前功能暂未开发")

        self.sendInfo("over", "")

    def inversionModel(self):
        # 实例化一个重力场对象
        gravity = gravityFieldModel.GravityField()
        Data = [89.75000, 113.50000, 8.78948]
        # 模拟数据读取并实时反演
        path = self.filePath
        savePath = os.path.abspath(Database.workspace + "/WHU-GM")
        with open(savePath, "a+") as F:
            # 先清空
            F.truncate(0)
            for i in range(2, self.N + 1):
                r = gravity.get_r(Data[1], Data[0])
                i_nRe = self.get_detCnmSnm(r, Data[1], Data[0], Data[2], i)
                for g in range(len(i_nRe)):
                    LineStr = ""
                    for k in range(len(i_nRe[0])):
                        if k < 2:
                            LineStr += " " + '{0:{1}<3}\t'.format(i_nRe[g][k], " ")
                        else:  # 长数据间隔写入
                            LineStr += "  " + '{0:{1}<22}\t'.format(i_nRe[g][k], " ")
                    self.sendInfo("G", LineStr)
                    if self.save:
                        LineStr += "\n"
                        F.flush()  # 缓冲区
                        F.writelines(LineStr)
                        os.fsync(F)

        if self.save:
            self.sendInfo("I", "模型已自动保存到工作空间，路径：{}".format(savePath))

    def get_detCnmSnm(self, r, lon, lat, det_g, n):
        """
        解算阶次n,m 球谐系数Cnm,Snm
        :param det_g: 重力异常值
        :param n: 解算阶
        :return: None
        """
        GM = 3.986004415E+14
        result = []
        # 定义积分式
        funC = lambda theta, lada: ((r * r) * (r / self.ellpsoid.a) ** n) * det_g * cos(
            m * lada) * self.legendre.normalizationLegendre_II(n, m, cos(theta)) * sin(theta) / (
                                           GM * (n - 1))
        funS = lambda theta, lada: ((r * r) * (r / self.ellpsoid.a) ** n) * det_g * sin(
            m * lada) * self.legendre.normalizationLegendre_II(n, m, cos(theta)) * sin(theta) / (
                                           GM * (n - 1))
        for m in range(n + 1):
            # 积分并代入数据,由于积分后仍为乘积式，故将积分下限定为0即可
            det_Cnm, errC = integrate.dblquad(funC, 0, (90 - lat) * pi / 180, lambda g: 0, lambda h: lon * pi / 180)
            det_Snm, errS = integrate.dblquad(funS, 0, (90 - lat) * pi / 180, lambda g: 0, lambda h: lon * pi / 180)

            listDa = [n, m, det_Cnm, det_Snm, errC, errS]
            self.setProcess(n, m)
            LineStr = ""
            for k in range(len(listDa)):
                if k < 2:
                    LineStr += " " + '{0:{1}<3}\t'.format(listDa[k], " ")
                else:  # 长数据间隔写入
                    LineStr += "  " + '{0:{1}<22}\t'.format(listDa[k], " ")
            self.sendInfo("G", LineStr)
            # print("阶次：", n, m, det_Cnm, det_Snm, errC, errS)
            result.append([n, m, det_Cnm, det_Snm, errC, errS])
        return result

    def sendInfo(self, type, strInfo):
        if type == "over":
            self.overEmit.emit()
        else:
            self.infoEmit.emit(type, strInfo)

    def setProcess(self, m, n):
        self.processEmit.emit(m, n)

    def killThread(self):
        self.terminate()
