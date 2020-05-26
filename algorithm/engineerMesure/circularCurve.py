#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 圆曲线相关计算类

@author: GanAH  2020/5/17.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import math
import numpy as np

from algorithm.common.BasicMeasurementAlgorithm import BasicMeasurementAlgorithm
from algorithm.common.angleConversion import Angle


class CircularCurve(object):

    def __init__(self):
        pass

    def singleCircularCurve_principalPointMileage(self, circularR, steerAngle_alpha, K_JD):
        """
        圆曲线主点里程计算
        :param circularR: 圆曲线半径R:m
        :param steerAngle_alpha: 线路转向角（弧度）
        :param K_JD: 交点JD里程：m
        :return:
        """
        # 圆曲线切线长
        T = circularR * math.tan(steerAngle_alpha / 2)
        # 曲线长
        L = circularR * steerAngle_alpha
        # 曲线外矢距
        # E = circularR * (1 / math.cos(steerAngle_alpha / 2) - 1)
        # 切曲差
        q = 2 * T - L

        # 计算主点里程
        K_ZY = K_JD - T
        K_QZ = K_ZY + L / 2
        K_YZ = K_ZY + L

        # 检核
        JH1 = K_QZ + q / 2
        JH2 = K_ZY + T
        print(K_JD, JH1, JH2)

        if K_JD == JH2 and K_JD == JH1:
            print("检核正确！")
            print("主点里程：", K_ZY, K_QZ, K_YZ)
            return {"code": 1,
                    "result": [K_ZY, K_QZ, K_YZ]}
        else:
            if JH1 - K_JD < 1.0E6 and JH2 - K_JD < 1.0E6:
                print("基本检核正确！")
                return {"code": 1,
                        "result": [K_ZY, K_QZ, K_YZ]}
            else:
                print("计算错误，再看看输入数据？我已经保证算法无误了")
                return {"code": 0}

    def singleCircularCurve_middlePilePointCoor(self, circularR, steerAngle_alpha, steerAngleType, K_JD, JD_CoorX,
                                                JD_CoorY,
                                                K_middlePilePoint, alpha_ZYJDorJDYZ):
        """
        计算已知里程中桩点的坐标
        <p> 前提：待求中桩点所在圆曲线的R，路线转向角alpha，交点JD里程，待求中桩点里程
        :param circularR: 中桩点所在圆曲线的半径：m
        :param steerAngle_alpha: 线路转向角（弧度）
        :param steerAngleType: 线路转向角方向：R-右折角，L-左折角
        :param K_JD: 交点JD里程：m
        :param JD_CoorX: 交点JD的X坐标
        :param JD_CoorY: 交点JD的Y坐标
        :param K_middlePilePoint: 待求中桩点里程：m
        :param alpha_ZYJDorJDYZ: 坐标方位角(弧度）：1.待求点在ZY-QZ：ZYJD；2.待求点在QZ-YZ：JDYZ
        :return:
        """
        # 圆曲线切线长
        T = circularR * math.tan(steerAngle_alpha / 2)
        # 曲线长
        L = circularR * steerAngle_alpha
        # 曲线外矢距
        # E = circularR * (1 / math.cos(steerAngle_alpha / 2) - 1)
        q = 2 * T - L

        # 计算主点里程
        K_ZY = K_JD - T
        K_QZ = K_ZY + L / 2
        K_YZ = K_ZY + L

        # 检核
        JH1 = K_QZ + q / 2
        JH2 = K_ZY + T
        print(K_JD, JH1, JH2)

        if K_JD == JH2 and K_JD == JH1:
            print("主点里程计算结果检核正确！执行下一步计算")
            # 根据QZ点判断中桩点位于圆曲线的区域
            if K_middlePilePoint < K_QZ and K_middlePilePoint > K_ZY:
                # 前半段
                distanceDifference = K_middlePilePoint - K_ZY
                # 计算独立坐标系下坐标
                seta = distanceDifference / circularR
                x = circularR * math.sin(seta)
                y = circularR * (1 - math.cos(seta))
                if steerAngleType == "L":
                    y = -y
                # 计算 ZY/YZ 的坐标，需要知道ZY-JD/JD-YZ的坐标方位角
                X_ZY = JD_CoorX - T * math.cos(alpha_ZYJDorJDYZ)
                Y_ZY = JD_CoorY - T * math.sin(alpha_ZYJDorJDYZ)
                # 统一坐标系下的坐标
                X_middlePilePoint = X_ZY + x * math.cos(alpha_ZYJDorJDYZ) - y * math.sin(alpha_ZYJDorJDYZ)
                Y_middlePilePoint = Y_ZY + x * math.sin(alpha_ZYJDorJDYZ) + y * math.cos(alpha_ZYJDorJDYZ)

            elif K_middlePilePoint < K_YZ and K_middlePilePoint > K_QZ:
                # 后半段
                distanceDifference = K_ZY - K_middlePilePoint
                # 计算独立坐标系下坐标
                seta = distanceDifference / circularR
                x = circularR * math.sin(seta)
                y = circularR * (1 - math.cos(seta))
                if steerAngleType == "L":
                    y = -y
                # 计算 ZY/YZ 的坐标，需要知道ZY-JD/JD-YZ的坐标方位角
                X_YZ = JD_CoorX - T * math.cos(alpha_ZYJDorJDYZ)
                Y_YZ = JD_CoorY - T * math.sin(alpha_ZYJDorJDYZ)
                # 统一坐标系下的坐标
                X_middlePilePoint = X_YZ + x * math.cos(alpha_ZYJDorJDYZ) + y * math.sin(alpha_ZYJDorJDYZ)
                Y_middlePilePoint = Y_YZ + x * math.sin(alpha_ZYJDorJDYZ) - y * math.cos(alpha_ZYJDorJDYZ)
            else:
                print("中桩点不在圆曲线上，错误！")
                return None
            print("计算完成！坐标为", X_middlePilePoint, Y_middlePilePoint)

        else:
            print("主点里程计算错误")

    def relief_circularCurve_principalPointMileage(self, circularR, steerAngle_alpha, Ls, K_JD):
        """
        带有缓和曲线的圆曲线主点里程计算
        :param circularR: 圆曲线半径R:m
        :param steerAngle_alpha: 线路转向角（弧度）
        :param Ls: 缓和曲线长度：m
        :param K_JD: 交点JD里程：m
        :return:
        """
        # 切垂距
        m = Ls / 2 - Ls * Ls * Ls / (240 * circularR * circularR)
        # 圆曲线内移值
        P = Ls * Ls / (24 * circularR)
        # 缓和曲线的切线角
        bata_0 = Ls * 180 / (2 * circularR * math.pi)  # 度
        print("缓和曲线的切线角DMS", Angle(bata_0).degreeToDMS())
        # 切线长
        TH = (circularR + P) * math.tan(steerAngle_alpha / 2) + m
        # 曲线长
        LH = math.pi * circularR * (steerAngle_alpha * 180 / math.pi - 2 * bata_0) / 180 + 2 * Ls
        LT = LH - 2 * Ls
        # 外矢距
        EH = (circularR + P) * (1 / math.cos(steerAngle_alpha / 2)) - circularR
        # 切曲差
        q = 2 * TH - LH

        # 主点里程
        K_ZH = K_JD - TH
        K_HY = K_ZH + Ls

        K_QZ = K_ZH + LH / 2
        K_YH = K_HY + LT
        K_HZ = K_YH + Ls

        # 检核
        print("检核：", K_QZ + 1 / 2 * q, K_JD)
        if K_JD - (K_QZ + 1 / 2 * q) < 1E-5 or (K_QZ + 1 / 2 * q) == K_JD:
            print("曲线综合要素计算检核正确")
            return {"code": 1,
                    "result": [m, P, bata_0, TH, K_ZH, K_HY, K_QZ, K_YH, K_HZ]}
        else:
            print("检核错误")
            return {"code": 0}

    def relief_circularCurve_middlePilePointCoor(self, circularR, steerAngle_alpha, steerAngleType, Ls, K_JD, JD_CoorX,
                                                 JD_CoorY,
                                                 K_middlePilePoint, alpha_ZHYJDorJDHZ):
        """
        计算已知里程中桩点的坐标
        <p> 前提：待求中桩点所在圆曲线的R，路线转向角alpha，交点JD里程，待求中桩点里程
        :param circularR: 中桩点所在圆曲线的半径：m
        :param steerAngle_alpha: 线路转向角（弧度）
        :param steerAngleType: 线路转向角方向：R-右折角，L-左折角
        :param Ls: 缓和曲线长：m
        :param K_JD: 交点JD里程：m
        :param JD_CoorX: 交点JD的X坐标
        :param JD_CoorY: 交点JD的Y坐标
        :param K_middlePilePoint: 待求中桩点里程：m
        :param alpha_ZHYJDorJDHZ: 坐标方位角：弧度
        :return:
        """
        # 获取曲线主点参数
        principalPointDict = self.relief_circularCurve_principalPointMileage(circularR, steerAngle_alpha, Ls, K_JD)
        if principalPointDict["code"] == 1:
            # 检核正确
            m = principalPointDict["result"][0]
            P = principalPointDict["result"][1]
            # bata =  principalPointDict["result"][2]
            T = principalPointDict["result"][3]
            K_ZH = principalPointDict["result"][4]
            K_HY = principalPointDict["result"][5]
            # K_QZ = principalPointDict["result"][6]
            K_YH = principalPointDict["result"][7]
            K_HZ = principalPointDict["result"][8]

            # 计算线路坐标
            X_ZHorHZ = JD_CoorX - T * math.cos(alpha_ZHYJDorJDHZ)
            Y_ZHorHZ = JD_CoorY - T * math.sin(alpha_ZHYJDorJDHZ)

            # 判断待求中桩点的位置
            if K_middlePilePoint > K_ZH and K_middlePilePoint < K_HY:
                print("在第一段缓和曲线上")
                # 在第一段缓曲线上
                L_I = K_middlePilePoint - K_ZH
                x_I = L_I - L_I ** 5 / (40 * circularR * circularR * Ls * Ls)
                y_I = L_I * L_I * L_I / (6 * circularR * Ls)
                if steerAngleType == "L":
                    y_I = - y_I
                X_middlePilePoint = X_ZHorHZ + x_I * math.cos(alpha_ZHYJDorJDHZ) - y_I * math.sin(alpha_ZHYJDorJDHZ)
                Y_middlePilePoint = Y_ZHorHZ + x_I * math.sin(alpha_ZHYJDorJDHZ) + y_I * math.cos(alpha_ZHYJDorJDHZ)


            elif K_middlePilePoint > K_HY and K_middlePilePoint < K_YH:
                # 在圆曲线区域,归并到第一个独立坐标系进行计算
                print("在圆曲线区域,归并到第一个独立坐标系进行计算")
                L_circular = K_middlePilePoint - K_ZH
                seta = (L_circular - 0.5 * Ls) / circularR
                x_circular = m + circularR * math.sin(seta)
                y_circular = P + circularR * (1 - math.cos(seta))
                if steerAngleType == "L":
                    y_circular = - y_circular
                X_middlePilePoint = X_ZHorHZ + x_circular * math.cos(alpha_ZHYJDorJDHZ) - y_circular * math.sin(
                    alpha_ZHYJDorJDHZ)
                Y_middlePilePoint = Y_ZHorHZ + x_circular * math.sin(alpha_ZHYJDorJDHZ) + y_circular * math.cos(
                    alpha_ZHYJDorJDHZ)


            elif K_middlePilePoint > K_YH and K_middlePilePoint < K_HZ:
                # 在第二段缓曲线上
                print("在第二段缓曲线上")
                L_II = K_HZ - K_middlePilePoint
                x_II = L_II - L_II ** 5 / (40 * circularR * circularR * Ls * Ls)
                y_II = L_II * L_II * L_II / (6 * circularR * Ls)
                if steerAngleType == "L":
                    y_II = - y_II
                X_middlePilePoint = X_ZHorHZ + x_II * math.cos(alpha_ZHYJDorJDHZ) + y_II * math.sin(
                    alpha_ZHYJDorJDHZ)
                Y_middlePilePoint = Y_ZHorHZ + x_II * math.sin(alpha_ZHYJDorJDHZ) - y_II * math.cos(
                    alpha_ZHYJDorJDHZ)
            else:
                print("中桩点不在曲线上！")
                return None
            print("结果：", X_middlePilePoint, Y_middlePilePoint)
        else:
            print("主点坐标计算检核错误")
            return None


if __name__ == "__main__":
    circularCurve = CircularCurve()
    # 单圆曲线主点里程
    # circularCurve.singleCircularCurve_principalPointMileage(1155, Angle(74).toRadian(), 653.554)
    # 单圆曲线中桩点坐标
    # coorLocaAngle = BasicMeasurementAlgorithm().calc_angle(8936.445, 3517.359, 9018.059, 3665.385)
    # print("坐标方位角为：", coorLocaAngle, Angle(coorLocaAngle).degreeToDMS())
    circularCurve.singleCircularCurve_middlePilePointCoor(1155, Angle(74).toRadian(), "R", 653.554, 2282606.761,
                                                          30388001.807, 500, Angle(240).toRadian())
    # 带缓和曲线的计算主点里程
    # circularCurve.relief_circularCurve_principalPointMileage(854.4, Angle(42, 18, 25.2).getRadian(), 85, 471.762)

    # 带缓和曲线的计算中桩点坐标
    # coorLocaAngle = BasicMeasurementAlgorithm().calc_angle(399589.5506, 538373.6835, 399606.2286, 539444.3196)
    # coorLocaAngle = coorLocaAngle+Angle(42, 18, 25.2).DMSToDegree() + 180
    # print("坐标方位角为：", coorLocaAngle, Angle(coorLocaAngle).degreeToDMS())
    # circularCurve.relief_circularCurve_middlePilePointCoor(854.4, Angle(42, 18, 25.2).toRadian(), "R", 85, 471.762,
    #                                                        399606.2286,
    #                                                        539444.3196, 750, Angle(coorLocaAngle).toRadian())
