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
from math import sin, cos, pi, sqrt

GM = 3.986004415E+14
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

    def Legendre(self, cos_value, n, m):
        """
        完全正规化勒让德函数
        <p> 标准向前列递推法
        :param value: cos(theta)
        :param n: 阶/次
        :param m:
        :return:
        """
        if n > 1 and m <= (n - 2):
            s1 = sqrt((4 * n * n - 1) / (n * n - m * m)) * cos_value * self.fuzhu(cos_value, n - 1, m, 0)
            s2 = sqrt((2 * n + 1) * (n * n - m * m - 2 * n + 1) / ((2 * n - 3) * (n * n - m * m))) * self.fuzhu(
                cos_value, n - 2, m, 1)
            print("勒让德结果", s1, s2, s1 - s2)
            return s1 - s2
        # 递推初值
        elif n == 0 and m == 0:
            return 1
        elif n == 1 and m == 0:
            return sqrt(3) * cos_value
        elif n == 1 and m == 1:
            return sqrt(3 * (1 - cos_value * cos_value))
        else:
            print("错误值", n, m)
            return 1

    def fuzhu(self, cos_v, n, m, index):
        if n > 1 and n != m:
            if index == 0:
                return sqrt((4 * n * n - 1) / (n * n - m * m)) * cos_v * self.fuzhu(cos_v, n - 1, m, index)
            else:
                return sqrt((2 * n + 1) * (n * n - m * m - 2 * n + 1) / ((2 * n - 3) * (n * n - m * m))) * self.fuzhu(
                    cos_v, n - 2, m, index)
        elif n == 0 and m == 0:
            return 1
        elif n == 1 and m == 0:
            return sqrt(3) * cos_v
        elif n == 1 and m == 1:
            return sqrt(3 * (1 - cos_v * cos_v))
        else:
            print("辅助错误值，该值未处理：", n, m)
            return 1

    def modelTeta_g(self, model, modelNormal, r, lon, lat, N):
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
                # if Cnm and Snm and Cnm_N is not None:
                value += (n - 1) * ((R / r) ** n) * (
                        (Cnm - Cnm_N) * cos(m * lada) + Snm * sin(m * lada)) * self.Legendre(cos(theta), n, m)
                # else:
                #     if Cnm or Snm is None:
                #         print("重力场模型缺少{0}阶：{1}次以上的数据".format(i_n, m))
                #     elif Cnm_N is None:
                #         print("正常重力场模型缺少{0}阶：{1}次以上的数据".format(i_n, m))
                # 后面次都会缺失，不必再看
                # break
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
        for n in range(2, 50):
            for m in range(n):
                sumV += (model.getCnm(n, m) * cos(m * lada) + model.getSnm(n, m) * sin(m * lada)) * self.Legendre(
                    cos(theta), n, m)
            sumN += sumV * (self.a / r) ** n

        N = GM * sumN / (avg_g * r)
        print("N:", N)
        return N

    def get_r(self, B, L):
        """
        获取向径
        :param B: 纬度
        :param L: 经度
        :return:
        """
        No = self.a / sqrt(1 - self.e * self.e * sin(B) * sin(B))
        X = No * cos(B) * cos(L)
        Y = No * cos(B) * sin(L)
        Z = No * (1 - self.e * self.e) * sin(B)
        return sqrt(X * X + Y * Y + Z * Z)


class GravityModel():
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
                            # 查看
                            # print(self.modelData[i])
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


modelPath = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\EGM08_360d"
model2Path = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\SGG-UGM-1_360d"
modelNormalPath = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\正常位系数(30阶)"

csvPath = "E:/文档/大三课程/第三学期 - 物理大地测量学实习/数据/Net.csv"
Data = []
model = GravityModel(model2Path)
# N_model = GravityModel(modelNormalPath)

m = model.modelData

# 测试勒让德级数
for i in range(50):
    G = GravityField().Legendre(cos(60 * pi / 180), int(m[i][0]), int(m[i][1]))
    print("阶次", m[i][0], m[i][1], G)

# gravity = GravityField()
# teta_g = []
# with open(csvPath, "r") as F:
#     reader = csv.reader(F)
#     count = 1
#     for row in reader:
#         if count == 1:
#             head = row
#             count = 2
#         else:
#             lineData = list(map(float, row[1:4]))
#             # gravity.model_N(model, R, lineData[0], lineData[1], 9.7)
#             r = gravity.get_r(lineData[0], lineData[1])
#             teta_g.append(gravity.modelTeta_g(model, N_model, r, lineData[0], lineData[1], 10))
#
# print("=== 最终数据")
# for i in range(len(teta_g)):
#     print(teta_g[i] * 100)
