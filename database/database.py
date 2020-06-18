#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 临时中转数据库

@author: GanAH  2020/3/1.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""


class Database():
    # 坐标转换读入的原始数据
    _coorTranSourceData = None
    _coorTranTargetData = None

    @property
    def coorTranSourceData(self):
        return self._coorTranSourceData

    @coorTranSourceData.setter
    def coorTranSourceData(self, fileReadData):
        self._coorTranSourceData = fileReadData

    @property
    def coorTranTargetData(self):
        return self._coorTranTargetData

    @coorTranTargetData.setter
    def coorTranTargetData(self, fileReadData):
        self._coorTranTargetData = fileReadData

    _publicPointNumber = 3

    @property
    def publicPointNumber(self):
        return self._publicPointNumber

    @publicPointNumber.setter
    def publicPointNumber(self, count):
        self._publicPointNumber = count

    # 坐标转换结果
    @property
    def coorTranResultDict(self):
        return self._coorTranResultDict

    @coorTranResultDict.setter
    def coorTranResultDict(self, resultDict):
        self._coorTranResultDict = resultDict

    @property
    def coorTranResultFormatListData(self):
        return self._coorTranResultFormatListData

    @coorTranResultFormatListData.setter
    def coorTranResultFormatListData(self, list):
        self._coorTranResultFormatListData = list

    @property
    def targetPointName(self):
        return self._coorTranResult

    @targetPointName.setter
    def targetPointName(self, resultList):
        self._coorTranResult = resultList

    # 徕卡数据
    @property
    def leicaSourceGsiData(self):
        return self._leicaSourceGsiData

    @leicaSourceGsiData.setter
    def leicaSourceGsiData(self, gsiSourceStr):
        self._leicaSourceGsiData = gsiSourceStr

    @property
    def leicaAnalysisDict(self):
        return self._leicaAnalysisDict

    @leicaAnalysisDict.setter
    def leicaAnalysisDict(self, analysisDict):
        self._leicaAnalysisDict = analysisDict

    @property
    def COSAControlNetMersureData(self):
        return self._COSAControlNetMersureData

    @COSAControlNetMersureData.setter
    def COSAControlNetMersureData(self, kesaSourceData):
        self._COSAControlNetMersureData = kesaSourceData

    @property
    def stableDotGroupMeasure_I(self):
        return self.stableDotGroupMeasure_I

    @stableDotGroupMeasure_I.setter
    def stableDotGroupMeasure_I(self, measure_I):
        self.stableDotGroupMeasure_I = measure_I

    @property
    def stableDotGroupMeasure_II(self):
        return self.stableDotGroupMeasure_II

    @stableDotGroupMeasure_II.setter
    def stableDotGroupMeasure_II(self, measure_II):
        self.stableDotGroupMeasure_II = measure_II

    @property
    def stablePointCoorGroup(self):
        return self.stablePointCoorGroup

    @stablePointCoorGroup.setter
    def stablePointCoorGroup(self, coorGroup):
        self.stablePointCoorGroup = coorGroup

    @property
    def N_file(self):
        return self._N_fileData

    @N_file.setter
    def N_file(self, _N_file):
        self._N_fileData = _N_file


