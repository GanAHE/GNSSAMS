#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 临时中转数据库

@author: GanAH  2020/3/1.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import json


class Database(object):
    # 基本配置文件信息
    configJsonPath = "./source/para_json/config.json"
    LicensePath = None
    workspace = None
    default_workspace = "./workspace/"
    elliDict = None
    # 地球自转角速度rad/s -RotationalAngularVelocity
    earth_RAV = 7.29211511467e-5
    # 光速 m/s
    light_speed = 299792458

    localHelpDocument = "./source/document/test.html"
    onlineHelpLink = "https://www.ganahe.top/"

    oFilePath = None
    nFilePath = None
    oFilePathList = []
    nFilePathList = []

    def loadConfigJson(self):
        """
        加载Json配置文件
        :return: None
        """
        # 读取json文件内容,返回字典格式
        with open(self.configJsonPath, 'r', encoding='utf8')as fp:
            # with open('../source/para_json/config.json', 'r', encoding='utf8')as fp:
            dict_data = json.load(fp)
        fp.close()
        Database.workspace = dict_data["workspace"]
        Database.elliDict = dict_data["elliPara"]
        Database.LicensePath = dict_data["License"]

    # 坐标转换读入的原始数据
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
    def filePath(self):
        """
        #获取文件路径
        #解释器，设定与获取类的静态属性，MVC模式
        #
        #注意这下杠杠！
        #.....我服了，不然会调用错误，Java，c就没有你这么傲娇的语言
                                                         ------10-15
        垃圾明明是你变量名和函数名一致了！ -----2019-12-29
        :return:_filePath
        """
        return self.path

    @filePath.setter
    def filePath(self, path):
        """
        设定打开的文件路径
        :param path:
        :return:
        """
        self.path = path

    @property
    def collect_vetc_time(self):
        return self._collect_vetc_time

    @collect_vetc_time.setter
    def collect_vetc_time(self, etc_time):
        self._collect_vetc_time = etc_time

    @property
    def lat_lon(self):
        return self._lat_lon

    @lat_lon.setter
    def lat_lon(self, lat_lon):
        self._lat_lon = lat_lon

    @property
    def earth_vetc(self):
        return self._earth_vetc

    @earth_vetc.setter
    def earth_vetc(self, earthETC):
        self._earth_vetc = earthETC

    """
    # SPP导航电文及观测文件
    """
    _navigationMessage = None
    _satelliteObservations = None

    @property
    def navigationMess(self):
        return self._navigationMessage

    @navigationMess.setter
    def navigationMess(self, navigationMssData):
        self._navigationMessage = navigationMssData

    @property
    def satelliteObs(self):
        return self._satelliteObservations

    @satelliteObs.setter
    def satelliteObs(self, setelliteObsver):
        self._satelliteObservations = setelliteObsver

    # 异常消息处理
    _warnExceptionText = None

    @property
    def warnExceptionText(self):
        return self._warnExceptionText

    @warnExceptionText.setter
    def warnExceptionText(self, exceptionText):
        self._warnExceptionText = exceptionText

    # 标准气象元素
    _To = 20  # 摄氏度
    _Po = 1013.25  # mbar
    _RHo = 0.5

    @property
    def standardMeteorologicalElement(self):
        """
        获取内部存储的标准气象元素
        :return: list [To,Po,RHo]
        """
        return [self._To, self._Po, self._RHo]

    @standardMeteorologicalElement.setter
    def standardMeteorologicalElement(self, listElement):
        """
        设定标准气象元素
        :param listElement: len = 3,[To,Po,RHo]
        """
        self._To = listElement[0]
        self._Po = listElement[1]
        self._RHo = listElement[2]

    """
    # 地球磁北极坐标,单位：度 在初始化时进行检查更新！
    """
    _fia_earth = 79.93
    _lambda_earth = 288.04

    @property
    def earth_N_pole_coor(self):
        return self._fia_earth, self._lambda_earth

    @earth_N_pole_coor.setter
    def earth_N_pole_coor(self, fia_earth_N_pole, lamda_earth_N_pole):
        self._fia_earth = fia_earth_N_pole
        self._lambda_earth = lamda_earth_N_pole

    """
    # RINEX 文件状态
    # 存在： 1 /否： 0
    # 文件状态 - 正常： 1 /否： 0
    """
    Nfile_exist = 0
    Nfile_status = 1
    Ofile_exist = 0
    Ofile_status = 1

    @property
    def RINEX_status(self, file_type):
        """
        获取卫星文件状态信息
        :param file_type: O-obverseFile ; N-navagate;
        :return:exist_code:0;1
        """
        if file_type == "N":
            return self.Nfile_exist, self.Nfile_status
        elif file_type == "O":
            return self.Ofile_exist, self.Ofile_status
        else:
            return -1

    @RINEX_status.setter
    def RINEX_status(self, file_type, exist_code, status_code):
        """
        设定文件状态信息
        :param file_type: O-obverseFile ; N-navagate;
        :param exist_code: 1-exist;0-not exist
        :param status_code:1-ok;0-false
        :return: boolean
        """
        # print("执行了？")
        if file_type == "N":
            print("测试数据库", exist_code, status_code)
            self.Nfile_exist = exist_code

            self.Nfile_status = status_code
            print("测试数据库", self.Nfile_exist, self.Nfile_status)
            return True
        elif file_type == "O":
            self.Ofile_exist = exist_code
            self.Ofile_status = status_code
            return True
        else:
            return False
