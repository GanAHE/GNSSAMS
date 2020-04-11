#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: GanAH  2020/3/21.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from PyQt5.QtCore import QThread,pyqtSignal

from algorithm.engineerMesure.leicaGsiFormat import LeicaGSIFormat
from database.database import Database


class ActionLeicaGSIThread(QThread):
    infoEmit = pyqtSignal(str,str)
    endEmit = pyqtSignal()

    def __init__(self):
        super(ActionLeicaGSIThread,self).__init__()

    def run(self) -> None:
        self.leicaAnalysis()


    def leicaAnalysis(self):

        # 从数据库获取数据
        sourceStrData = Database.leicaSourceGsiData
        # 格式解析
        leicaGSIAnalysisDict = LeicaGSIFormat(sourceStrData).getAnalysisDict()
        # 解析结果，存入数据库
        Database.leicaAnalysisDict = leicaGSIAnalysisDict


    def killThread(self):
        self.terminate()