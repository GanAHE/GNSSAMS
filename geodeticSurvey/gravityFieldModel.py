#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 重力场模型应用
<p> 类集

@author: GanAH  2020/7/2.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import csv

from scipy import integrate
from numpy import sin, cos, pi, sqrt
from geodeticSurvey.legendre import Legendre

GM = 3.986004415E+14  # avg = GM/(R*R) 单位为m/s^2
R = 6378136.3

WGS84 = [6378137,
         6356752.3142,
         0.00335281066474748,
         0.08181919084255,
         0.08209443794965649]


# ellipsisData = Database.elliDict

class GravityField(object):
    a = 0
    b = 0
    ae = 0
    e = 0
    pow_e = 0
    legendre = Legendre()

    def __init__(self):
        elliPara = WGS84
        self.a = elliPara[0]
        self.b = elliPara[1]
        self.ae = elliPara[2]
        self.e = elliPara[3]
        self.pow_e = elliPara[4]

    def sti(self, intValue):
        """
        递归阶乘计算
        :param intValue: 整数值
        :return:
        """
        if intValue > 0:
            return intValue * self.sti(intValue - 1)
        else:
            return 1

    def get_detg(self, model, modelNormal, r, lon, lat, N):
        """
        计算重力异常值
        :param model: 重力场模型路径
        :param modelNormal: 正常椭球重力场模型路径
        :param r: 地心球坐标半径
        :param lon: 经度
        :param lat: 纬度
        :param N: 球谐展开的最大阶
        :return:
        """
        # 余纬
        theta = (90 - lat) * pi / 180
        lada = lon * pi / 180
        value = 0
        for n in range(2, N + 1):
            for m in range(n):
                Cnm = model.getCnm(n, m)
                Snm = model.getSnm(n, m)
                Cnm_N = modelNormal.getCnm(n, m)
                value += (n - 1) * ((R / r) ** n) * (
                        (Cnm - Cnm_N) * cos(m * lada) + Snm * sin(m * lada)) * self.legendre.normalizationLegendre_II(
                    n, m, cos(theta))
        print("\n==========\n", value)
        g = GM * value / (r * r)
        print("重力异常值解算结果:", g, "mGal")
        return g

    def model_N(self, model, r, lon, lat, avg_g):
        """
        利用模型计算大地水准面差距 N
        :return:
        """
        # 余纬
        theta = (90 - lat) * pi / 180
        lada = lon * pi / 180

        sumV = 0
        sumN = 0
        for n in range(2, 20):
            for m in range(n + 1):
                sumV += (model.getCnm(n, m) * cos(m * lada) + model.getSnm(n, m) * sin(
                    m * lada)) * self.legendre.normalizationLegendre_II(
                    n, m, cos(theta))
            sumN += sumV * ((self.a / r) ** n)

        N = GM * sumN / (avg_g * r)
        # print("N:", N)
        return N

    def normalGravity(self, fia, type=None, H=None):
        """
        计算正常重力值
        :param fia: 大地纬度
        :param type: 模型公式
        :param H: 大地水准面上高度
        :return: cm/s^2 or Gal
        """
        fia = fia * pi / 180
        if type == "hemote":
            yo = 978030.0 * (1 + 0.005302 * sin(fia) * sin(fia) - 0.000007 * sin(2 * fia) * sin(2 * fia))
        elif type == "casni":
            yo = 978049.0 * (1 + 0.005288 * sin(fia) * sin(fia) - 0.0000059 * sin(2 * fia) * sin(2 * fia))
        else:
            yo = 978032.0 * (1 + 0.005302 * sin(fia) * sin(fia) - 0.0000058 * sin(2 * fia) * sin(2 * fia))

        if H is None:  # 水准面上正常重力
            return yo
        else:  # 地面H出正常重力
            return yo - 0.3086 * H

    def get_r(self, B, L):
        """
        获取向径
        :param B: 纬度
        :param L: 经度
        :return: 向径：m
        """
        No = self.a / sqrt(1 - self.e * self.e * sin(B) * sin(B))
        X = No * cos(B) * cos(L)
        Y = No * cos(B) * sin(L)
        Z = No * (1 - self.e * self.e) * sin(B)
        return sqrt(X * X + Y * Y + Z * Z)

    def get_detCnmSnm(self, r, lon, lat, det_g, n):
        """
        解算阶次n,m 球谐系数Cnm,Snm
        :param det_g: 重力异常值
        :param n: 解算阶
        :return: None
        """
        result = []
        for m in range(n + 1):
            # 定义积分式
            funC = lambda theta, lada: ((r * r) * (r / self.a) ** n) * det_g * cos(
                m * lada) * self.legendre.normalizationLegendre_II(n, m, cos(theta)) * sin(theta) / (
                                               GM * (n - 1))
            funS = lambda theta, lada: ((r * r) * (r / self.a) ** n) * det_g * sin(
                m * lada) * self.legendre.normalizationLegendre_II(n, m, cos(theta)) * sin(theta) / (
                                               GM * (n - 1))
            # 积分并代入数据,由于积分后仍为乘积式，故将积分下限定为0即可
            det_Cnm, errC = integrate.dblquad(funC, 0, (90 - lat) * pi / 180, lambda g: 0, lambda h: lon * pi / 180)
            det_Snm, errS = integrate.dblquad(funS, 0, (90 - lat) * pi / 180, lambda g: 0, lambda h: lon * pi / 180)
            print("阶次：", n, m, det_Cnm, det_Snm, errC, errS)
            result.append([n, m, det_Cnm, det_Snm, errC, errS])
        return result

    def writePlus(self, path, listA):
        """
        按列宽写入反演后的模型
        :param path:
        :param listA:
        :return:
        """
        with open(path, "a+") as F:
            for i in range(len(listA)):
                LineStr = ""
                for k in range(len(listA[0])):
                    if k < 2:
                        LineStr += "  " + '{0:{1}<1}\t'.format(listA[i][k], " ")
                    else:  # 长数据间隔写入
                        LineStr += "  " + '{0:{1}<22}\t'.format(listA[i][k], " ")
                LineStr += "\n"
                F.write(LineStr)


"""
##################
重力场模型
"""


class GravityModel(object):
    modelData = []

    def __init__(self, modelPath):
        with open(modelPath, "r") as f:
            for line in f:
                self.modelData.append((line.strip()).split())
        f.close()

    def getCnm(self, n, m):
        if n < 2:
            raise Warning("阶必须大于2")
        else:
            for i in range(len(self.modelData)):
                if n == int(self.modelData[i][0]):
                    for k in range(len(self.modelData[i])):
                        if m == int(self.modelData[i][1]):
                            return float(self.modelData[i][2])
                elif n < int(self.modelData[i][0]):
                    return 0

    def getSnm(self, n, m):
        if n < 2:
            raise Warning("阶必须大于2")
        else:
            for i in range(len(self.modelData)):
                if n == int(self.modelData[i][0]):
                    for k in range(len(self.modelData[i])):
                        if m == int(self.modelData[i][1]):
                            return float(self.modelData[i][3])
                elif n < int(self.modelData[i][0]):
                    return 0

    def getLineData(self, n, m):
        if n < 2:
            raise Warning("阶必须大于2")
        else:
            for i in range(len(self.modelData)):
                if n == int(self.modelData[i][0]):
                    for k in range(len(self.modelData[i])):
                        if m == int(self.modelData[i][1]):
                            # 返回数值型list行数据
                            return list(map(float, self.modelData[i]))
                elif n < int(self.modelData[i][0]):
                    return 0

    def getModelDataLength(self):
        return len(self.modelData)


"""
##############################
调用入口
"""


def getModelDet_g():
    modelPath = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\EGM08_360d"
    model2Path = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\SGG-UGM-1_360d"
    modelNormalPath = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\正常位系数(30阶)"

    csvPath = "E:/文档/大三课程/第三学期 - 物理大地测量学实习/数据/Grid.csv"
    Data = []
    model = GravityModel(modelPath)
    N_model = GravityModel(modelNormalPath)

    m = model.modelData
    gravity = GravityField()

    teta_g = []
    with open(csvPath, "r") as F:
        reader = csv.reader(F)
        count = 1
        for row in reader:
            if count == 1:  # 列表栏
                count = 2
            else:
                lineData = list(map(float, row[1:4]))
                r = gravity.get_r(lineData[0], lineData[1])
                # go = GM / (r * r)
                # print(gravity.model_N(model, r, lineData[0], lineData[1], go))
                # print("向径", r, gravity.model_N(model, r, lineData[0], lineData[1], go))
                teta_g.append(gravity.get_detg(model, N_model, r, lineData[0], lineData[1], 10))

    print("=== 最终数据")
    for i in range(len(teta_g)):
        print(teta_g[i] * 100 * 10000)


def getModelDet_g2():
    modelPath = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\EGM08_360d"
    model2Path = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\SGG-UGM-1_360d"
    modelNormalPath = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\正常位系数(30阶)"
    model = GravityModel(model2Path)
    N_model = GravityModel(modelNormalPath)
    gravity = GravityField()
    Data = [[2, 114.3569444, 30.53138889, 41, 979349.183300],
            [4, 114.353121, 30.532709, 37, 979349.738555],
            [5, 114.352441, 30.532003, 34, 979350.709845],
            [3, 114.353763, 30.531887, 39, 979350.657243],
            [6, 114.353044, 30.529602, 37, 979351.344532],
            [7, 114.35465, 30.529754, 41, 979351.081257],
            [8, 114.354571, 30.528564, 40, 979349.974796]]
    re = []
    for i in range(len(Data)):
        r = gravity.get_r(Data[i][0], Data[i][1])
        re.append(gravity.get_detg(model, N_model, r, Data[i][0], Data[i][1], 10))
    print("=== 最终数据")
    for i in range(len(re)):
        print(re[i] * 100 * 10000)


def reModel():
    """
    模型反演入口
    :return:
    """
    # 反演最大阶
    N_max = 10
    # 模拟数据读取并实时反演
    path = "E:/文档/大三课程/第三学期 - 物理大地测量学实习/数据/grav_anom_glb_30m_SGG-UGM-1_360d_sph_6371km_1group"
    savePath = "E:/文档/大三课程/第三学期 - 物理大地测量学实习/数据/MGM-O1"
    # 实例化一个重力场对象
    gravity = GravityField()
    with open(path, "r") as f:
        for line in f:
            lineList = list(map(float, line.split()))
            print("DATA_", lineList)
            for i in range(2, N_max):
                r = gravity.get_r(lineList[1], lineList[0])
                i_nRe = gravity.get_detCnmSnm(r, lineList[1], lineList[0], lineList[2], i)
                print("当前阶:---\n", i_nRe)
                # gravity.writePlus(savePath, i_nRe)

# getModelDet_g()
# getModelDet_g2()
reModel()
