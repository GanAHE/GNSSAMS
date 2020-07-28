#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 解算重力异常

@author: GanAH  2020/7/29.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""

from PyQt5.QtCore import QThread, pyqtSignal
from geodeticSurvey import gravitySurvey


class ActionCacuGravityAnomaly(QThread):
    infoEmit = pyqtSignal(str, str)
    overEmit = pyqtSignal()
    def __init__(self):
        super(ActionCacuGravityAnomaly, self).__init__()

    def setPara(self, dictPara):
        self.code = dictPara["code"]
        self.filePath = dictPara["filePath"]

    def run(self) -> None:
        if self.code == 201:
            self.measureDataCacu()
        else:
            self.gravityModelCacu()

        self.sendInfo("over","")

    def measureDataCacu(self):
        self.sendInfo("I","测量数据解算")
        pass

    def gravityModelCacu(self):
        self.sendInfo("I", "模型数据解算")
        pass

    def sendInfo(self, type, strInfo):
        if type == "over":
            self.overEmit.emit()
        else:
            self.infoEmit.emit(type, strInfo)

    def killThread(self):
        self.terminate()
