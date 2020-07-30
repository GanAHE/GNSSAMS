#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 标准单点定位

@author: GanAH  2020/7/18.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import datetime
import os
import pandas
import numpy as np
from GNSS.file import readFile
from GNSS.orbetEtc import satelliteOrbetEtc
from numpy import sqrt, mat, cos, sin, transpose, linalg, arctan, rad2deg
from GNSS.timeSystem.timeChange import TimeSystemChange
from GNSS.correctionModel import tropCorrection, ionCorrection
from database.database import Database
from measureTool import coordinationTran
from myConfig.logger import Logger
from PyQt5.QtCore import QThread, pyqtSignal
from GNSS.map import baiduMap
import matplotlib.pyplot as plt


class ActionGetStationPositionThread(QThread):
    infoEmit = pyqtSignal(str, str)
    overEmit = pyqtSignal()
    logger = Logger().get_logger("ACTION_GET_STATION_POSITION")
    id = None
    ellipsoid = None
    resDict = {"pointID": [], "X": [], "Y": [], "Z": [], "B": [], "L": [], "H": [], "PDOP": [], "mP": [], "TDOP": [],
               "mT": [], "GDOP": [], "mG": [], "VDOP": [], "mV": [], "HDOP": [], "mH": [], "information": []}

    def __init__(self):
        super(ActionGetStationPositionThread, self).__init__()

    def setPara(self, paraDict):
        self.code = paraDict["code"]
        self.paraDict = paraDict

    def run(self) -> None:
        ellipsoid = self.paraDict["ellipsoid"]
        try:
            if self.code == 201:
                self.actionSPP(ellipsoid)
            elif self.code == 202:
                self.actionPPP(ellipsoid)
            else:
                self.drawSatelliteOrbet()
            self._sendInfo("B", "")
        except Exception as e:
            self._sendInfo("E", e.__str__())

    def killThread(self):
        self.terminate()

    def actionSPP(self, ellipsoid):
        # 传入的椭球参数，设置到类中
        self.ellipsoid = ellipsoid
        # 从数据库获取文件路径
        path_OFile = Database.oFilePathList
        path_NFile = Database.nFilePathList
        # path_OFile = r"E:\CodePrograme\Python\EMACS\workspace\GNSS\D068305A.19O"
        # path_NFile = r"E:\CodePrograme\Python\EMACS\workspace\GNSS\D068305A.19N"
        print(len(path_NFile), type(path_NFile))
        if len(path_OFile) != 0 and len(path_OFile) == len(path_NFile):
            # 清空字典值
            for key in self.resDict.keys():
                self.resDict[key] = []
            index = []
            for i in range(len(path_NFile)):
                # 读取观测文件并提取对应数据
                obsClass = readFile.read_obsFile(path_OFile[i])
                obsEpoch = obsClass.observation.epoch.index.values.tolist()
                # 选定一个观测时间
                obsTime = obsEpoch[0][0]
                # print(obsEpoch,type(obsClass.observation.epoch))
                # sv =obsClass.observation.loc[(obsTime,obsEpoch[0][1])]
                Sat = []
                count_satellite = 6
                for k in range(len(obsEpoch)):
                    if obsTime == obsEpoch[k][0]:
                        if (obsEpoch[k][1])[0] == "G":
                            Sat.append(obsEpoch[k][1])
                        # elif (obsEpoch[k][1])[0] == "R":
                        #     PR
                    # if len(PRN) >= count_satellite:
                    #     break

                # 读取导航电文
                navClass = readFile.read_navFile(path_NFile[i])
                # 设定处理的点序号
                self.id = str(i)
                self.getStationPosition_SPP(obsTime, "C1C", Sat, count_satellite, obsClass, navClass)
                # 存储到数据库
                index.append(obsClass.stationName)
            columns = [str(key) for key in self.resDict.keys()]
            Database.stationPositionDataFrame = pandas.DataFrame(self.resDict, index, columns)

            points = []
            for i in range(len(self.resDict["L"])):
                points.append({'lat': self.resDict["B"][i], 'lng': self.resDict["L"][i],
                               'infomation': self.resDict["information"][i]})
            # 将解算的点写入JS变量
            with open(Database.mapJSVarPath, "w", encoding="utf-8") as f:
                f.write("points = " + str(points))

            self._sendInfo("T", "完成单点定位解算！点击地图显示可以查看该点\n在地图上的位置信息，该步骤加载较慢，如需要请耐心等待片刻...")

        else:
            self._sendInfo("T", "未导入导航电文/观测文件")

    def actionPPP(self, ellipsoid):
        self.ellipsoid = ellipsoid

        oFilePathList = Database.oFilePathList
        sp3FilePathList = Database.sp3FilePathList

        if len(oFilePathList) == 0 and len(sp3FilePathList) == 0:
            self._sendInfo("T", "观测文件或sp3文件未导入！")
        else:
            # 清空字典值
            for key in self.resDict.keys():
                self.resDict[key] = []
            path_sp3FilePast = sp3FilePathList[0]
            path_sp3FileNow = sp3FilePathList[1]
            path_sp3FileFuture = sp3FilePathList[2]

            sp3PastClass = readFile.read_sp3File(path_sp3FilePast)
            sp3NowClass = readFile.read_sp3File(path_sp3FileNow)
            sp3FutureClass = readFile.read_sp3File(path_sp3FileFuture)
            for i in range(len(oFilePathList)):
                # 设定处理的点序号
                self.id = str(i)
                obsClass = readFile.read_obsFile(oFilePathList[0])

                # sp3PastEpoch = sp3PastClass.ephemeris.index.values.tolist()
                # sp3NowEpoch = sp3NowClass.ephemeris.index.values.tolist()
                # sp3FutureEpoch = sp3FutureClass.ephemeris.index.values.tolist()
                obsEpoch = obsClass.observation.index.values.tolist()

                obsTime = obsEpoch[0][0]
                count_satellite = 6

                self.getStationPosition_PPP(sp3PastClass, sp3NowClass, sp3FutureClass, obsClass, obsTime,
                                            count_satellite)

                # 存储到数据库
                index = [str(i) for i in range(len(oFilePathList))]
                columns = [str(key) for key in self.resDict.keys()]
                Database.stationPositionDataFrame = pandas.DataFrame(self.resDict, index, columns)

            points = []
            for i in range(len(self.resDict["L"])):
                points.append({'lat': self.resDict["B"][i], 'lng': self.resDict["L"][i],
                               'infomation': self.resDict["information"][i]})
            # 将解算的点写入JS变量
            with open(Database.mapJSVarPath, "w", encoding="utf-8") as f:
                f.write("points = " + str(points))

            self._sendInfo("T", "完成单点定位解算！点击地图显示可以查看该点\n在地图上的位置信息，该步骤加载较慢，如需要请耐心等待片刻...")

    def drawSatelliteOrbet(self):
        self._sendInfo("T", "卫星轨道解算中，请稍候...")
        self.satelliteOrbits()
        self._sendInfo("T", "完成卫星轨道可视化")

    def getStationPosition_SPP(self, observationEpoch, waveBand, Sat, count_satellite, obsClass, navClass):

        # print("这是椭球参数：",Database.ellipsoid.CGCS2000.a)
        # print(coordinationTran.CoordinationTran(self.ellipsoid).XYZ_to_BLH(
        #     [6378020.461599736, 12739.801484877651, 49091.74122939511]))
        # 卫星数量
        # count_satellite = len(PRN)
        # 光速 m/s
        c = 299792458
        # 地球自转角速度rad/s -RotationalAngularVelocity
        earth_RAV = 7.29211511467e-5
        # 测站近似坐标,一维list
        approxPosition = obsClass.approx_position

        # 判断与观测时间最近的导航电文时间
        delta = []
        navEpoch = navClass.navigation.epoch.index.values.tolist()
        for i in range(len(navEpoch)):
            delta.append((navEpoch[i][0] - observationEpoch).seconds)
        delta = list(map(abs, delta))
        num = 0
        navTime = ""
        for i in range(len(delta)):
            mindelta = min(delta)
            navTime = observationEpoch + datetime.timedelta(seconds=mindelta)
            if navTime.minute != 0 and navTime.second != 0:
                num = delta.index(mindelta)
                Sat.pop(num)
                delta.pop(num)
            else:
                break
        # print(delta.pop(num))
        # print(navTime)

        PRN = []
        for i in range(len(Sat)):
            PRN.append(Sat[i])
            if len(PRN) >= count_satellite:
                break
        # print(PRN)

        # 构建系数矩阵
        B = []
        L = []
        # 设置测站
        self._sendInfo("测站", obsClass.stationName)
        for i in range(len(PRN)):
            satelliteName = PRN[i]
            # 根据行键获取数据，key = ('2019-10-28 10:00:00', 'G10'),使用iloc可以根据行序获取，键值从观测文件找
            # navEpochData = navClass.navigation.loc[(navClass.navigation.index.values[i][0], satelliteName)].tolist()
            navEpochData = navClass.navigation.loc[(navTime, satelliteName)].tolist()
            # 根据接收时间和伪距，计算信号发射时刻
            # time_receiveSignal = "2019-10-28 08:33:15"

            waveDistance = obsClass.observation.loc[(observationEpoch, satelliteName)][waveBand]

            # intTimeFormat 实现如下转换：2019-10-28 08:33:15 --> [2019, 10, 28, 8, 33, 15]
            intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))
            UTCTimeList = intTimeFormat(str(observationEpoch))
            time_rec = TimeSystemChange(UTCTimeList[0], UTCTimeList[1], UTCTimeList[2], UTCTimeList[3], UTCTimeList[4],
                                        UTCTimeList[5])
            week, tow = time_rec.UTC2GPSTime()

            approxDistance = waveDistance
            temp = 0
            Vts = 0
            xyz = []
            while abs(temp - approxDistance) > 1e-6:
                temp = approxDistance
                teta_ts = approxDistance / c
                time_sendSignal = tow + 0.01 - teta_ts
                Vts, xyz = satelliteOrbetEtc.getSatellitePositon_II(time_sendSignal, navEpochData)
                # print(PRN[i]+"卫星位置：", xyz)
                # 对卫星坐标进行地球自转改正
                # xyz = mat([[cos(earth_RAV * teta_ts), sin(earth_RAV * teta_ts), 0],
                #            [-sin(earth_RAV * teta_ts), cos(earth_RAV * teta_ts), 0],
                #            [0, 0, 1]]) * mat(xyz)
                xyz = mat([[0, sin(earth_RAV * teta_ts), 0],
                           [-sin(earth_RAV * teta_ts), 0, 0],
                           [0, 0, 0]]) * mat(xyz) + mat(xyz)
                # xyz = mat(xyz)
                # xyz = xyz.tolist()
                # 计算近似站星距离/伪距
                sum = 0
                for k in range(3):
                    sum += (xyz[k, 0] - approxPosition[k]) * (xyz[k, 0] - approxPosition[k])
                approxDistance = sqrt(sum)
                # print("迭代站星距：{}".format(approxDistance))

            # TODO 查找卫星仰角
            satelliteAngle = self.calSatelliteAngle(approxPosition, xyz[0, 0], xyz[1, 0], xyz[2, 0])

            # 对流层延迟/电离层延迟改正
            if navClass.version[0] == 2:
                Vion = ionCorrection.klobuchar(satelliteAngle, UTCTimeList, approxPosition, xyz, navClass.alphalist,
                                               navClass.betalist, self.ellipsoid)
            else:
                Vion = 0

            Vtrop = tropCorrection.tropospheric_delay(approxPosition, satelliteAngle, UTCTimeList, self.ellipsoid)
            print(Vts, Vion, Vtrop)
            B.append(
                [-(xyz[0, 0] - approxPosition[0]) / approxDistance,
                 -(xyz[1, 0] - approxPosition[1]) / approxDistance,
                 -(xyz[2, 0] - approxPosition[2]) / approxDistance,
                 -1])
            print("==+==", PRN[i], waveDistance - approxDistance, approxDistance)
            L.append([approxDistance + c * Vts + Vion + Vtrop - approxDistance])

        # 循环解算系数等完成
        # 平差求解
        matrix_B = mat(B)
        matrix_L = mat(L)
        self._sendInfo("K", "--matrix_B")
        self.outputFormatList("K", matrix_B.tolist(), 13)
        # self._sendInfo("K", "--matrix_B:{}\n".format(matrix_B.tolist()))
        self._sendInfo("K", "--matrix_L:{}\n".format(matrix_L.tolist()))
        Q = linalg.inv(transpose(matrix_B) * matrix_B)
        matrix_x = Q * (transpose(matrix_B) * matrix_L)
        matrix_v = matrix_B * matrix_x - matrix_L
        self._sendInfo("K", "--matrix_x:{}\n".format(matrix_x.tolist()))
        self._sendInfo("K", "--matrix_v:{}\n".format(matrix_v.tolist()))
        sigma_o = sqrt((transpose(matrix_v) * matrix_v)[0, 0] / (count_satellite - 4))
        self._sendInfo("K", "中误差：{} mm".format(sigma_o * 1000))
        # D = sigma_o * sigma_o * Q
        # 改正
        stationPosition = [approxPosition[0] + matrix_x[0, 0], approxPosition[1] + matrix_x[1, 0],
                           approxPosition[2] + matrix_x[2, 0]]
        self._sendInfo("K", "近似坐标：{} \n最后坐标：{}\n-----------------\n".format(approxPosition, stationPosition))
        self._sendInfo("坐标X/m", str(stationPosition[0]))
        self._sendInfo("坐标Y/m", str(stationPosition[1]))
        self._sendInfo("坐标Z/m", str(stationPosition[2]))
        coor_B, coor_L, coor_H = coordinationTran.CoordinationTran(self.ellipsoid).XYZ_to_BLH(stationPosition)
        self._sendInfo("B/°", str(rad2deg(coor_B)))
        self._sendInfo("L/°", str(rad2deg(coor_L)))
        self._sendInfo("H/m", str(coor_H))
        # 调用百度地图API获取经纬度对应的地理位置信息
        pointInfomation = baiduMap.getAddressInfo(rad2deg(coor_L), rad2deg(coor_B))
        # print("Poi0",pointInfomation)
        self._sendInfo("地理信息", pointInfomation)
        # 精度评价： GDOP / PDOP / TDOP / HDOP / VDOP
        # 三维点位精度衰减因子
        mo = sigma_o * sigma_o
        PDOP = sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2])
        mP = mo * PDOP
        # 时间精度衰减因子
        TDOP = sqrt(Q[3, 3])
        mT = mo * TDOP
        # 几何精度衰减因子
        GDOP = sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2] + Q[3, 3])
        mG = mo * GDOP
        # 坐标系统转换为BLH的系数矩阵
        matrix_BLH_B = mat([[-sin(coor_B) * cos(coor_L), -sin(coor_B) * sin(coor_L), cos(coor_B)],
                            [-sin(coor_L), cos(coor_L), 0],
                            [cos(coor_B) * cos(coor_L), cos(coor_B) * cos(coor_L), sin(coor_B)]])

        Q_dot = matrix_BLH_B * Q[0:3, 0:3] * transpose(matrix_BLH_B)
        HDOP = sqrt(Q_dot[0, 0] + Q_dot[1, 1])
        mH = mo * HDOP
        VDOP = sqrt(Q_dot[2, 2])
        mV = mo * VDOP

        asd = [PDOP, mP, TDOP, mT, GDOP, mG, HDOP, mH, VDOP, mV]
        asdName = ["PDOP/m", "mP/m", "TDOP/m", "mT/m", "GDOP/m", "mG/m", "HDOP/m", "mH/m", "VDOP/m", "mV/m"]
        for g in range(len(asd)):
            self._sendInfo(asdName[g], str(round(asd[g], 5)))
        self.resDict["pointID"].append(obsClass.stationName)
        self.resDict["X"].append(stationPosition[0])
        self.resDict["Y"].append(stationPosition[1])
        self.resDict["Z"].append(stationPosition[2])
        self.resDict["B"].append(rad2deg(coor_B))
        self.resDict["L"].append(rad2deg(coor_L))
        self.resDict["H"].append(coor_H)
        self.resDict["PDOP"].append(PDOP)
        self.resDict["mP"].append(mP)
        self.resDict["TDOP"].append(TDOP)
        self.resDict["mT"].append(mT)
        self.resDict["GDOP"].append(GDOP)
        self.resDict["mG"].append(mG)
        self.resDict["VDOP"].append(VDOP)
        self.resDict["mV"].append(mV)
        self.resDict["HDOP"].append(HDOP)
        self.resDict["mH"].append(mH)
        self.resDict["information"].append(pointInfomation)

    def _sendInfo(self, type, strInfo):
        if len(type) == 1:
            self.logger.info(strInfo)
        else:  # 符合表格数据传递信息，加入辨识头
            type = self.id + "-" + type
        self.infoEmit.emit(type, strInfo)

    def outputFormatList(self, type, twoDisslistData, pointCount=None):
        if pointCount is None:
            pointCount = 5
        for i in range(len(twoDisslistData)):
            line = ""
            for k in range(len(twoDisslistData[0])):
                if str(twoDisslistData[i][k])[0] == "-":
                    line += "{0:{1}<16}\t".format(round(twoDisslistData[i][k], pointCount), "")
                else:
                    line += " {0:{1}<16}\t".format(round(twoDisslistData[i][k], pointCount), "")
            self._sendInfo(type, line)

    def getStationPosition_PPP(self, sp3PastClass, sp3NowClass, sp3FutureClass, obsClass, obsTime, count_satellite):

        self._sendInfo("I", "正在读取文件...")

        # path_sp3FilePast = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20770.sp3"
        # path_sp3FileNow = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20771.sp3"
        # path_sp3FileFuture = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20772.sp3"
        # # path_sp3File = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20771.sp3"
        # path_oFile = r"D:\CodeProgram\Python\EMACS\workspace\GNSS\GP008301I.19o"
        #
        # sp3PastClass = readFile.read_sp3File(path_sp3FilePast)
        # sp3NowClass = readFile.read_sp3File(path_sp3FileNow)
        # sp3FutureClass = readFile.read_sp3File(path_sp3FileFuture)
        # # sp3Class = readFile.read_sp3File(path_sp3File)
        # obsClass = readFile.read_obsFile(path_oFile)

        sp3PastEpoch = sp3PastClass.ephemeris.index.values.tolist()
        sp3NowEpoch = sp3NowClass.ephemeris.index.values.tolist()
        sp3FutureEpoch = sp3FutureClass.ephemeris.index.values.tolist()
        # sp3Epoch = sp3Class.ephemeris.index.values.tolist()
        obsEpoch = obsClass.observation.index.values.tolist()

        intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))

        # obsTime = obsEpoch[0][0]
        # print(obsTime)
        obsTimeList = intTimeFormat(str(obsTime))
        time = obsTimeList[3] + obsTimeList[4] / 60 + obsTimeList[5] / 3600
        print(time)
        approx_position = obsClass.approx_position

        Sat = []
        # count_satellite = 6
        for k in range(len(obsEpoch)):
            if obsTime == obsEpoch[k][0]:
                if (obsEpoch[k][1])[0] == "G":
                    Sat.append(obsEpoch[k][1])
            if len(Sat) == count_satellite:
                break
        print(Sat)

        x = []
        y = []
        z = []
        satellite_x = []
        satellite_y = []
        satellite_z = []
        B = []
        L = []
        self._sendInfo("I", "正在读取卫星数据...")
        for j in range(len(Sat)):
            print(Sat[j])
            timePastList = []
            timeNowList = []
            timeFutureList = []
            epochPast = []
            epochNow = []
            epochFuture = []
            for i in range(len(sp3PastEpoch)):
                if sp3PastEpoch[i][1] == Sat[j]:
                    timePastList.append(intTimeFormat(str(sp3PastEpoch[i][0])))
                    epochPast.append(sp3PastEpoch[i][0])

            for i in range(len(sp3NowEpoch)):
                if sp3NowEpoch[i][1] == Sat[j]:
                    timeNowList.append(intTimeFormat(str(sp3NowEpoch[i][0])))
                    epochNow.append(sp3NowEpoch[i][0])

            for i in range(len(sp3FutureEpoch)):
                if sp3FutureEpoch[i][1] == Sat[j]:
                    timeFutureList.append(intTimeFormat(str(sp3FutureEpoch[i][0])))
                    epochFuture.append(sp3FutureEpoch[i][0])
            # print(epochPast)

            timePastSeconds = []
            timeNowSeconds = []
            timeFutureSeconds = []
            dx = []
            dy = []
            dz = []
            for i in range(len(timePastList)):
                timePastSeconds.append(timePastList[i][3] + timePastList[i][4] / 60 + timePastList[i][5] / 3600)
                dx.append((sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["X"]) * 1000)
                dy.append((sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Y"]) * 1000)
                dz.append((sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Z"]) * 1000)

            for i in range(len(timeNowList)):
                timeNowSeconds.append(timeNowList[i][3] + timeNowList[i][4] / 60 + timeNowList[i][5] / 3600)
                dx.append((sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["X"]) * 1000)
                dy.append((sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Y"]) * 1000)
                dz.append((sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Z"]) * 1000)

            for i in range(len(timeFutureList)):
                timeFutureSeconds.append(
                    timeFutureList[i][3] + timeFutureList[i][4] / 60 + timeFutureList[i][5] / 3600)
                dx.append((sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["X"]) * 1000)
                dy.append((sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Y"]) * 1000)
                dz.append((sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Z"]) * 1000)

            x.append(dx)
            y.append(dy)
            z.append(dz)

            timeSeconds = []
            for i in range(len(timePastSeconds)):
                timeSeconds.append(timePastSeconds[i] - 24)

            for i in range(len(timeNowSeconds)):
                timeSeconds.append(timeNowSeconds[i])

            for i in range(len(timeFutureSeconds)):
                timeSeconds.append(timeFutureSeconds[i] + 24)

            px = 0
            py = 0
            pz = 0
            for m in range(len(timeSeconds)):
                px_delta = x[j][m] * self.coefficients(time, timeSeconds[m], timeSeconds)
                px += px_delta
                py_delta = y[j][m] * self.coefficients(time, timeSeconds[m], timeSeconds)
                py += py_delta
                pz_delta = z[j][m] * self.coefficients(time, timeSeconds[m], timeSeconds)
                pz += pz_delta
            satellite_x.append(px)
            satellite_y.append(py)
            satellite_z.append(pz)

            satelliteName = Sat[j]
            waveBand = "C1C"
            waveDistance = obsClass.observation.loc[(obsTime, satelliteName)][waveBand]

            approxDistance = np.sqrt(
                (satellite_x[j] - approx_position[0]) ** 2 + (satellite_y[j] - approx_position[1]) ** 2 + (
                        satellite_z[j] - approx_position[2]) ** 2)

            # TODO 查找卫星仰角
            satelliteAngle = self.calSatelliteAngle(approx_position, px, py, pz)
            self._sendInfo("K", " -{} 卫星仰角:{}".format(Sat[j], satelliteAngle))

            # 对流层延迟/电离层延迟改正
            Vion = 0

            Vtrop = tropCorrection.tropospheric_delay(approx_position, satelliteAngle, obsTimeList, self.ellipsoid)

            B.append(
                [-(satellite_x[j] - approx_position[0]) / approxDistance,
                 -(satellite_y[j] - approx_position[1]) / approxDistance,
                 -(satellite_z[j] - approx_position[2]) / approxDistance,
                 -1])
            L.append([approxDistance + Vion + Vtrop - approxDistance])

        self._sendInfo("I", "正在进行平差求解...")
        # 平差求解
        matrix_B = np.mat(B)
        matrix_L = np.mat(L)
        self._sendInfo("K", "--matrix_B:\n{}\n".format(matrix_B))
        self._sendInfo("K", "--matrix_L:\n{}\n".format(matrix_L.tolist()))
        Q = np.linalg.inv(np.transpose(matrix_B) * matrix_B)
        matrix_x = Q * (np.transpose(matrix_B) * matrix_L)
        matrix_v = matrix_B * matrix_x - matrix_L
        self._sendInfo("K", "--matrix_x:\n{}\n".format(matrix_x.tolist()))
        self._sendInfo("K", "--matrix_v:\n{}\n".format(matrix_v.tolist()))
        sigma_o = np.sqrt((np.transpose(matrix_v) * matrix_v)[0, 0] / (count_satellite - 4))
        self._sendInfo("K", "中误差：{} mm".format(sigma_o * 1000))
        stationPosition = [approx_position[0] + matrix_x[0, 0], approx_position[1] + matrix_x[1, 0],
                           approx_position[2] + matrix_x[2, 0]]
        self._sendInfo("K", "近似坐标：\n{} \n最后坐标：\n{}".format(approx_position, stationPosition))
        self._sendInfo("测站", obsClass.stationName)
        self._sendInfo("X/m", str(approx_position[0]))
        self._sendInfo("Y/m", str(approx_position[1]))
        self._sendInfo("Z/m", str(approx_position[2]))
        coor_B, coor_L, coor_H = coordinationTran.CoordinationTran(self.ellipsoid).XYZ_to_BLH(stationPosition)
        self._sendInfo("B/°", str(np.rad2deg(coor_B)))
        self._sendInfo("L/°", str(np.rad2deg(coor_L)))
        self._sendInfo("H/m", str(coor_H))

        # 调用百度地图API获取经纬度对应的地理位置信息
        pointInfomation = baiduMap.getAddressInfo(np.rad2deg(coor_L), np.rad2deg(coor_B))
        # print("Poi0",pointInfomation)
        self._sendInfo("地理信息", pointInfomation)

        # 精度评价： GDOP / PDOP / TDOP / HDOP / VDOP
        # 三维点位精度衰减因子
        mo = sigma_o * sigma_o
        PDOP = np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2])
        mP = mo * PDOP
        # 时间精度衰减因子
        TDOP = np.sqrt(Q[3, 3])
        mT = mo * TDOP
        # 几何精度衰减因子
        GDOP = np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2] + Q[3, 3])
        mG = mo * GDOP
        # 坐标系统转换为BLH的系数矩阵
        matrix_BLH_B = np.mat([[-np.sin(coor_B) * np.cos(coor_L), -np.sin(coor_B) * np.sin(coor_L), np.cos(coor_B)],
                               [-np.sin(coor_L), np.cos(coor_L), 0],
                               [np.cos(coor_B) * np.cos(coor_L), np.cos(coor_B) * np.cos(coor_L), np.sin(coor_B)]])
        Q_dot = matrix_BLH_B * Q[0:3, 0:3] * np.transpose(matrix_BLH_B)
        HDOP = np.sqrt(Q_dot[0, 0] + Q_dot[1, 1])
        mH = mo * HDOP
        VDOP = np.sqrt(Q_dot[2, 2])
        mV = mo * VDOP

        asd = [PDOP, mP, TDOP, mT, GDOP, mG, HDOP, mH, VDOP, mV]
        asdName = ["PDOP/m", "mP/m", "TDOP/m", "mT/m", "GDOP/m", "mG/m", "HDOP/m", "mH/m", "VDOP/m", "mV/m"]
        for g in range(len(asd)):
            self._sendInfo(asdName[g], str(asd[g]))
        self.resDict["pointID"].append("nan")
        self.resDict["X"].append(stationPosition[0])
        self.resDict["Y"].append(stationPosition[1])
        self.resDict["Z"].append(stationPosition[2])
        self.resDict["B"].append(np.rad2deg(coor_B))
        self.resDict["L"].append(np.rad2deg(coor_L))
        self.resDict["H"].append(coor_H)
        self.resDict["PDOP"].append(PDOP)
        self.resDict["mP"].append(mP)
        self.resDict["TDOP"].append(TDOP)
        self.resDict["mT"].append(mT)
        self.resDict["GDOP"].append(GDOP)
        self.resDict["mG"].append(mG)
        self.resDict["VDOP"].append(VDOP)
        self.resDict["mV"].append(mV)
        self.resDict["HDOP"].append(HDOP)
        self.resDict["mH"].append(mH)
        self.resDict["information"].append(pointInfomation)

    def satelliteOrbits(self):

        sp3FileList = Database.sp3FilePathList

        if len(sp3FileList) >= 3:
            path_sp3FilePast = sp3FileList[0]
            path_sp3FileNow = sp3FileList[1]
            path_sp3FileFuture = sp3FileList[2]

            sp3PastClass = readFile.read_sp3File(path_sp3FilePast)
            sp3NowClass = readFile.read_sp3File(path_sp3FileNow)
            sp3FutureClass = readFile.read_sp3File(path_sp3FileFuture)

            sp3PastEpoch = sp3PastClass.ephemeris.index.values.tolist()
            sp3NowEpoch = sp3NowClass.ephemeris.index.values.tolist()
            sp3FutureEpoch = sp3FutureClass.ephemeris.index.values.tolist()

            Sat = []
            sp3NowTime = sp3NowEpoch[0][0]
            for k in range(len(sp3NowEpoch)):
                if sp3NowTime == sp3NowEpoch[k][0]:
                    Sat.append(sp3NowEpoch[k][1])
            self._sendInfo("K", "所有卫星列表：{}".format(Sat))

            intTimeFormat = lambda strT: list(
                map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))

            x = []
            y = []
            z = []
            timeSeconds = []
            time = np.linspace(0, 24, 24 * 5, endpoint=True)
            # allsatellite_x = []
            # allsatellite_y = []
            # allsatellite_z = []

            # 生成画布
            fig = plt.figure(num = "Satellite orbet")
            # 打开交互模式
            plt.ion()

            for j in range(len(Sat)):
                self._sendInfo("K", " - 当前轨道解算的卫星：{}".format(Sat[j]))
                timePastList = []
                timeNowList = []
                timeFutureList = []
                epochPast = []
                epochNow = []
                epochFuture = []
                for i in range(len(sp3PastEpoch)):
                    if sp3PastEpoch[i][1] == Sat[j]:
                        timePastList.append(intTimeFormat(str(sp3PastEpoch[i][0])))
                        epochPast.append(sp3PastEpoch[i][0])

                for i in range(len(sp3NowEpoch)):
                    if sp3NowEpoch[i][1] == Sat[j]:
                        timeNowList.append(intTimeFormat(str(sp3NowEpoch[i][0])))
                        epochNow.append(sp3NowEpoch[i][0])

                for i in range(len(sp3FutureEpoch)):
                    if sp3FutureEpoch[i][1] == Sat[j]:
                        timeFutureList.append(intTimeFormat(str(sp3FutureEpoch[i][0])))
                        epochFuture.append(sp3FutureEpoch[i][0])
                # print(epochPast)

                timePastSeconds = []
                timeNowSeconds = []
                timeFutureSeconds = []
                dx = []
                dy = []
                dz = []
                for i in range(len(timePastList)):
                    timePastSeconds.append(timePastList[i][3] + timePastList[i][4] / 60 + timePastList[i][5] / 3600)
                    dx.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["X"])
                    dy.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Y"])
                    dz.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Z"])

                for i in range(len(timeNowList)):
                    timeNowSeconds.append(timeNowList[i][3] + timeNowList[i][4] / 60 + timeNowList[i][5] / 3600)
                    dx.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["X"])
                    dy.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Y"])
                    dz.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Z"])

                for i in range(len(timeFutureList)):
                    timeFutureSeconds.append(
                        timeFutureList[i][3] + timeFutureList[i][4] / 60 + timeFutureList[i][5] / 3600)
                    dx.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["X"])
                    dy.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Y"])
                    dz.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Z"])

                x.append(dx)
                y.append(dy)
                z.append(dz)

                timeSeconds.clear()
                for i in range(len(timePastSeconds)):
                    timeSeconds.append(timePastSeconds[i] - 24)

                for i in range(len(timeNowSeconds)):
                    timeSeconds.append(timeNowSeconds[i])

                for i in range(len(timeFutureSeconds)):
                    timeSeconds.append(timeFutureSeconds[i] + 24)

                satellite_x = []
                satellite_y = []
                satellite_z = []
                for i in range(len(time)):
                    px = 0
                    py = 0
                    pz = 0
                    for m in range(len(timeSeconds)):
                        px_delta = x[j][m] * self.coefficients(time[i], timeSeconds[m], timeSeconds)
                        px += px_delta
                        py_delta = y[j][m] * self.coefficients(time[i], timeSeconds[m], timeSeconds)
                        py += py_delta
                        pz_delta = z[j][m] * self.coefficients(time[i], timeSeconds[m], timeSeconds)
                        pz += pz_delta
                    satellite_x.append(px)
                    satellite_y.append(py)
                    satellite_z.append(pz)

                # allsatellite_x.append(satellite_x)
                # allsatellite_y.append(satellite_y)
                # allsatellite_z.append(satellite_z)

                # # 生成画布
                # fig = plt.figure(num=str(Sat[j]))

                # 清除原有图像
                fig.clf()

                # 生成画布
                ax = fig.gca(projection='3d')

                # 设置标题
                ax.set_title("Satellite  " + str(Sat[j]) + "  Orbit")

                # 设置坐标轴范围
                ax.set_xlim(-30000, 30000)
                ax.set_ylim(-30000, 30000)
                ax.set_zlim(-30000, 30000)

                # 画三维散点图
                for i in range(len(time)):
                    ax.scatter(satellite_x[i], satellite_y[i], satellite_z[i], c="r", marker=".")

                plt.pause(0.2)

                # 保存图片到文件夹
                dirName = Database.workspace + "SatelliteOrbet"
                if not os.path.exists(dirName):
                    os.mkdir(dirName)
                plt.savefig(dirName + "/" + str(Sat[j]))

            # 关闭交互模式
            plt.ioff()

            # 图形显示
            plt.show()
        else:
            self._sendInfo("T", "SP3文件未导入或导入错误,\n需要导入连续三天的sp3文件！")

    def coefficients(self, x, m, seconds):  # 计算L系数
        l = 1
        for i in range(len(seconds)):
            if seconds[i] != m:
                l_delta = (x - seconds[i]) / (m - seconds[i])
                l *= l_delta
            else:
                l *= 1
        return l

    def calSatelliteAngle(self, approx_position, x, y, z):
        print(x, y, z)
        pos_B, pos_L, pos_H = coordinationTran.CoordinationTran(self.ellipsoid).XYZ_to_BLH(approx_position)
        print(rad2deg(pos_B), rad2deg(pos_L))
        satellite_position = []
        satellite_position.append(x)
        satellite_position.append(y)
        satellite_position.append(z)
        sat_B, sat_L, sat_H = coordinationTran.CoordinationTran(self.ellipsoid).XYZ_to_BLH(satellite_position)
        E = rad2deg(arctan((cos(sat_L - pos_L) * cos(pos_B) - 0.15) / sqrt(
            1 - (cos(sat_L - pos_L) * cos(pos_B)) ** 2)))
        return E
