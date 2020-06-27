#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: GanAH  2020/2/27.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from PyQt5 import QtCore
from engineerMesure.coorTran import TwoDissCoorTran
from database.database import Database
from myConfig.logger import Logger
from window.tipDig import ActionWarnException


class ActionCoorTran(QtCore.QThread):
    finishEmit = QtCore.pyqtSignal()
    infoEmit = QtCore.pyqtSignal(str, str)
    thisTypeEmit = QtCore.pyqtSignal(str, int)
    _caculType = "D"

    logger = Logger().get_logger("TWO_COOR_TRAN")
    """
    # infoEmit 信号：E执行弹窗提醒，I表示信息
    """

    def __init__(self):
        super(ActionCoorTran, self).__init__()
        self.thisTypeEmit.connect(self.setCaculType)

    def run(self) -> None:
        self.twoCoorTran()

    def twoCoorTran(self):
        try:
            self._sendInfo("I", "--进入子线程,开始二维坐标转换--")
            # 从数据获取数据
            sourceStrListData = Database.coorTranSourceData
            targetStrListData = Database.coorTranTargetData
            """
            需要解决！！！！！！！！！！！
            """
            if sourceStrListData is None:  # 数据库初始化的值为None
                self._sendInfo("E", "原始坐标文件数据未导入！")
            elif targetStrListData is None:
                self._sendInfo("E", "目标坐标文件数据未导入！")
            else:
                self._sendInfo("I", "基本参数处理完成，开始转换....")
                # 分离数据
                sourcePointName, sourceCoorData = self.separatePointName_position(sourceStrListData)
                targetPointName, targetCoorData = self.separatePointName_position(targetStrListData)

                # 获取参数计算方法并计算
                if self._caculType == "D":
                    # 直接参数法
                    self._sendInfo("I", "直接参数法解算中....")
                    resultDict = TwoDissCoorTran().directParaMethod(sourceCoorData, targetCoorData)

                elif self._caculType == "L":
                    # 最小二乘
                    self._sendInfo("I", "最小二乘法解算中....")
                    resultDict = TwoDissCoorTran().leastSquaresMethod(self._publicCount, sourceCoorData, targetCoorData)
                else:
                    # 正形变换
                    if len(targetCoorData) < 6:
                        self.logger.info("正形变换公共点少于必要个数！")
                        self._sendInfo("E", "公共点少于必要点数-6")
                    else:
                        self._sendInfo("I", "正形变换修正法解算中....")
                        resultDict = TwoDissCoorTran().conformalTransFormationMethod(self._publicCount, sourceCoorData,
                                                                                     targetCoorData)

                # 发送结束信号，存入数据库，由接收信号者获取数据，同时关闭线程（延迟1s）
                self._sendInfo("I", "转换完成，关闭线程....\n")
                Database.coorTranResultDict = resultDict
                self.finishEmit.emit()

        except Exception as e:
            # 异常信息
            self._sendInfo("E", "程序异常：" + e.args.__str__() + "\n,请联系开发者。")

    def separatePointName_position(self, dataList):
        """
        分离点名和坐标数据，并将字符数字化
        :param dataList: 待处理数据
        :return: pointNameList ,
        """
        pointNameList = []
        coorDataList = []
        for i in range(len(dataList)):
            pointNameList.append(dataList[i][0])
            coorDataList.append([float(dataList[i][1]), float(dataList[i][2])])
        return pointNameList, coorDataList

    def setCaculType(self, str, intPublicCount):
        self._caculType = str
        self._publicCount = intPublicCount

    def _sendInfo(self, strType, strInfo):
        self.logger.info(strInfo)
        self.infoEmit.emit(strType, strInfo)

    def _setInfoLog(self, strInfo):
        self.logger.info(strInfo)

    def killThread(self):
        self.terminate()
