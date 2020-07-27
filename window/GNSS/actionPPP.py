#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: DengGZC  2020/7/23.
@version 1.0.
@contact: dgzc159@163.com
"""

from GNSS.file import readFile
from GNSS.correctionModel import tropCorrection, ionCorrection
import numpy as np
import pandas
from GNSS.map import baiduMap
from database.database import Database
from measureTool import coordinationTran
from myConfig.logger import Logger
from PyQt5.QtCore import QObject, pyqtSignal

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.mplot3d import Axes3D

class ActionPPP(QObject):
    infoEmit = pyqtSignal(str, str)
    logger = Logger().get_logger("ACTION_GET_STATION_POSITION")
    id = "0"
    ellipsoid = None
    resDict = {"pointID": [], "X": [], "Y": [], "Z": [], "B": [], "L": [], "H": [], "PDOP": [], "mP": [], "TDOP": [],
               "mT": [], "GDOP": [], "mG": [], "VDOP": [], "mV": [], "HDOP": [], "mH": [], "information": []}

    def __init__(self):
        super(ActionPPP, self).__init__()



    def stationPosition(self, sp3PastClass, sp3NowClass, sp3FutureClass, obsClass, obsTime, count_satellite):

        self._sendInfo("I", "正在读取文件。。。")

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
        self._sendInfo("I", "正在读取卫星数据。。。")
        for j in range(len(Sat)):
            self._sendInfo("I", str(Sat[j]))
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
                dx.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["X"])
                dy.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Y"])
                dz.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Z"])

            for i in range(len(timeNowList)):
                timeNowSeconds.append(timeNowList[i][3] + timeNowList[i][4] / 60 + timeNowList[i][5] / 3600)
                dx.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["X"])
                dy.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Y"])
                dz.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Z"])

            for i in range(len(timeFutureList)):
                timeFutureSeconds.append(timeFutureList[i][3] + timeFutureList[i][4] / 60 + timeFutureList[i][5] / 3600)
                dx.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["X"])
                dy.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Y"])
                dz.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Z"])

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

            approxDistance = np.sqrt((satellite_x[j] - approx_position[0]) ** 2 + (satellite_y[j] - approx_position[1]) ** 2 + (satellite_z[j] - approx_position[2]) ** 2)

            # TODO 查找卫星仰角
            satelliteAngle = 15

            # 对流层延迟/电离层延迟改正
            Vion = 0

            Vtrop = tropCorrection.tropospheric_delay(approx_position[0], approx_position[1], approx_position[2],
                                                      satelliteAngle, obsTimeList)

            B.append(
                [-(satellite_x[j] - approx_position[0]) / approxDistance,
                 -(satellite_y[j] - approx_position[1]) / approxDistance,
                 -(satellite_z[j] - approx_position[2]) / approxDistance,
                 -1])
            L.append([approxDistance + Vion + Vtrop - approxDistance])

        self._sendInfo("I", "正在进行平差求解。。。")
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
        stationPosition = [approx_position[0] + matrix_x[0, 0], approx_position[1] + matrix_x[1, 0], approx_position[2] + matrix_x[2, 0]]
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
        path_sp3FilePast = r"e:\CodePrograme\Python\EMACS\workspace\GNSS\igs20770.sp3"
        path_sp3FileNow = r"e:\CodePrograme\Python\EMACS\workspace\GNSS\igs20771.sp3"
        path_sp3FileFuture = r"e:\CodePrograme\Python\EMACS\workspace\GNSS\igs20772.sp3"

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
        print(Sat)

        intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))

        x = []
        y = []
        z = []
        timeSeconds = []
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
                dx.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["X"])
                dy.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Y"])
                dz.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Z"])

            for i in range(len(timeNowList)):
                timeNowSeconds.append(timeNowList[i][3] + timeNowList[i][4] / 60 + timeNowList[i][5] / 3600)
                dx.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["X"])
                dy.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Y"])
                dz.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Z"])

            for i in range(len(timeFutureList)):
                timeFutureSeconds.append(timeFutureList[i][3] + timeFutureList[i][4] / 60 + timeFutureList[i][5] / 3600)
                dx.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["X"])
                dy.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Y"])
                dz.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Z"])

            x.append(dx)
            y.append(dy)
            z.append(dz)
            # print(dx)
            # print(x)

            timeSeconds.clear()
            for i in range(len(timePastSeconds)):
                timeSeconds.append(timePastSeconds[i] - 24)

            for i in range(len(timeNowSeconds)):
                timeSeconds.append(timeNowSeconds[i])

            for i in range(len(timeFutureSeconds)):
                timeSeconds.append(timeFutureSeconds[i] + 24)

            # print(timeSeconds)
        # print(x[2][5])
        # # 生成画布
        # fig = plt.figure()

        # 打开交互模式
        plt.ion()

        # # 清除原有图像
        # fig.clf()

        time = np.linspace(0, 24, 24 * 5, endpoint=True)

        for j in range(len(Sat)):
            print(Sat[j])
            satellite_x = []
            satellite_y = []
            satellite_z = []

            # 生成画布
            fig = plt.figure()

            # 清除原有图像
            fig.clf()

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

            # 生成画布
            ax = fig.gca(projection='3d')
            # 画三维散点图
            for i in range(len(time)):
                ax.scatter(satellite_x[i], satellite_y[i], satellite_z[i], c = "r", marker = ".")

            # 设置坐标轴范围
            ax.set_xlim(-30000, 30000)
            ax.set_ylim(-30000, 30000)
            ax.set_zlim(-30000, 30000)

            plt.pause(0.2)

        # 关闭交互模式
        plt.ioff()

        # 图形显示
        plt.show()
        return



    # satelliteOrbits()
    def coefficients(self, x, m, seconds):   # 计算L系数
        l = 1
        for i in range(len(seconds)):
            if seconds[i] != m:
                l_delta = (x - seconds[i]) / (m - seconds[i])
                l *= l_delta
                # print(l_delta)
            else:
                l *= 1
        # print(l)
        return l

    def _sendInfo(self, type, strInfo):
        if len(type) == 1:
            self.logger.info(strInfo)
        else:  # 符合表格数据传递信息，加入辨识头
            type = self.id + "-" + type
        self.infoEmit.emit(type, strInfo)


    # def transMatrix(self, matrix):
    #     x = ""
    #     for i in range(matrix.shape[0]):
    #         # for j in range(matrix.shape[1]):
    #         x += str(matrix[i])
    #         x += ", "
    #     return x

    def actionReadFilePPP(self, ellipsoid):
        self.ellipsoid = ellipsoid

        oFilePathList = Database.oFilePathList
        sp3FilePathList = Database.sp3FilePathList

        if len(oFilePathList) == 0 and len(sp3FilePathList) == 0:
            self._sendInfo("T", "观测文件或sp3文件未导入！")
        else:
            path_sp3FilePast = sp3FilePathList[0]
            path_sp3FileNow = sp3FilePathList[1]
            path_sp3FileFuture = sp3FilePathList[2]

            sp3PastClass = readFile.read_sp3File(path_sp3FilePast)
            sp3NowClass = readFile.read_sp3File(path_sp3FileNow)
            sp3FutureClass = readFile.read_sp3File(path_sp3FileFuture)

            obsClass = readFile.read_obsFile(oFilePathList[0])

            # sp3PastEpoch = sp3PastClass.ephemeris.index.values.tolist()
            # sp3NowEpoch = sp3NowClass.ephemeris.index.values.tolist()
            # sp3FutureEpoch = sp3FutureClass.ephemeris.index.values.tolist()
            obsEpoch = obsClass.observation.index.values.tolist()

            obsTime = obsEpoch[0][0]
            count_satellite = 6

            self.stationPosition(sp3PastClass, sp3NowClass, sp3FutureClass, obsClass, obsTime, count_satellite)

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





