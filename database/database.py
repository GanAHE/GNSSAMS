#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 临时中转数据库

@author: GanAH  2020/3/1.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import json
import os
from database import ellipsoid


class Database(object):
    # 基本配置文件信息
    configJsonPath = "./source/para_json/config.json"
    LicensePath = None
    envir = "CPU"
    default_envir = "CPU"
    speaker = 0
    default_speaker = 0
    workspace = None
    default_workspace = "./workspace/"
    # 数据库文件路径
    databaseFilePath = None
    databaseDefaultFilePath = "./source/database/project.db"

    # 椭球参数:a,b,偏心率e,第二偏心率e'
    ellipsoid = None
    userCheckEllipsoid = "WGS84"
    # 地球自转角速度rad/s -RotationalAngularVelocity
    earth_RAV = 7.29211511467e-5
    # 光速 m/s
    light_speed = 299792458

    localHelpDocument = "./source/template/404.html"
    onlineHelpLink = "https://www.ganahe.top/archives/measureSoftwareHelp.html"
    baiduMapLinkPath = "./source/template/baiduMap.html"
    mapJSVarPath = "./source/template/pointsVar.js"

    userBaiduAK = None
    userBaiduNK = None

    oFilePathList = []
    nFilePathList = []
    sppFilePathList = []
    sp3FilePathList = []
    # 解算后单点数据，类型为DataFrame
    stationPositionDataFrame = None

    # 重力场反演必要文件路径
    inversionGroupFilePath = None
    # 重力测量数据解算重力异常
    gravityMeasureFilePath = None
    grivatyModelPath = None
    gravityAnomalyData = None

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
        Database.envir = dict_data["envir"]
        Database.workspace = dict_data["workspace"]
        Database.databaseFilePath = dict_data["databaseFilePath"]
        Database.userCheckEllipsoid = dict_data["userCheckEllipsoid"]
        # 保存椭球参数
        Database.ellipsoid = ellipsoid.Ellipsoid(WGS84=ellipsoid.WGS84(dict_data["elliPara"]["WGS84_Ellipsoid"]),
                                                 CGCS2000=ellipsoid.CGCS2000(
                                                     dict_data["elliPara"]["CGCS2000_Ellipsoid"]),
                                                 krasovskiEllipsoid=ellipsoid.krasovskiEllipsoid(
                                                     dict_data["elliPara"]["krasovskiEllipsoid"]),
                                                 internationalEllipsoid_1975=ellipsoid.internationalEllipsoid_1975(
                                                     dict_data["elliPara"]["internationalEllipsoid_1975"]),
                                                 userPrivateEllipsoid=ellipsoid.userPrivateEllipsoid(
                                                     dict_data["elliPara"]["userPrivateEllipsoid"]), )
        Database.LicensePath = dict_data["License"]

    def writeJsonKeyValue(self, key1, value, key2=None):
        """
        修改键值
        :param key1: 键
        :param value: 值
        :param key2: 内键 主键为model时
        :return:
        """
        try:
            with open(self.configJsonPath, "r") as f:
                jsonData = json.load(f)
            f.close()
            if key1 == "model" and key2 != None:  # json内字典
                jsonData[key1][key2] = value
                with open(self.configJsonPath, "w") as r:
                    json.dump(jsonData, r)
                return True
            elif key1 != "model" and key2 is None:
                jsonData[key1] = value
                with open(self.configJsonPath, "w") as r2:
                    json.dump(jsonData, r2)
                return True
            else:
                return False
        except Exception as e:
            return e.__str__()

    def connectDatabase(self):
        # 创建一个cursor 游标（用于执行SQL语句）
        # cursor = conn.cursor()
        # # 执行SQL语句
        # # 创建user表
        # cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
        # # 向表中插入数据
        # cursor.execute('insert into user (id, name) values (\'1\', \'seven bai\')')
        # # 执行查询语句
        # cursor.execute('select * from user where id=?', ('1',))
        # # rowcount返回影响的行数（可以在执行update，delete，inset后执行查看）
        # cursor.rowcount
        # # 查询结果
        # values = cursor.fetchall()
        # print(values)
        # # 关闭cursor
        # cursor.close()
        # # 提交事务
        # conn.commit()
        # # 关闭数据库连接
        # conn.close()
        pass

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

    # 坐标系统转换原始坐标文件
    coorSystemTranSourcePath = None

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

    def getSppFilePath(self, type=None):
        if type.lower() == "o":
            return self.oFilePathList
        elif type.lower() == "n":
            return self.nFilePathList
        else:
            return self.sppFilePathList

    def setSppFilePath(self, fileList):
        # 清空数据
        Database.oFilePathList = []
        Database.nFilePathList = []
        Database.sppFilePathList = []
        # 从文件列表查找相同名组
        while len(fileList) > 1:
            i = 1
            if len(fileList) > 1:
                dirIndex, fileNameSaveIndex = os.path.split(fileList[0])
                dirSerch, fileNameSaveSerch = os.path.split(fileList[i])
                # 找到同名文件数据组
                if fileNameSaveIndex[:-1] == fileNameSaveSerch[:-1]:
                    if fileNameSaveIndex[-1].lower() == "o" and fileNameSaveSerch[-1].lower() == "n":
                        Database.oFilePathList.append(fileList[0])
                        Database.nFilePathList.append(fileList[i])
                    elif fileNameSaveIndex[-1].lower() == "n" and fileNameSaveSerch[-1].lower() == "o":
                        Database.oFilePathList.append(fileList[i])
                        Database.nFilePathList.append(fileList[0])
                    # 删除该位置数据
                    fileList.pop(i)
                    fileList.pop(0)
                else:
                    fileList.pop(0)
                    i += 1

    def setPppFilePath(self, fileList):
        # 清空数据
        Database.oFilePathList = []
        Database.sp3FilePathList = []
        # 从文件列表查找相同名组
        while len(fileList) > 0:
            dirIndex, fileName = os.path.split(fileList[0])
            if fileName[-1].lower() == "o":
                Database.oFilePathList.append(fileList[0])
            if fileName[-1].lower() == "3":
                Database.sp3FilePathList.append(fileList[0])
            # 删除该位置数据
            fileList.pop(0)
