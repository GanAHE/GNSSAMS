# -*- coding: utf-8 -*-

from numpy import *

"""
    卫星定轨类
    <p>
    注意：类内方法与构造函数一定要保证缩进位数相同
    
:param 卫星导航电文信息
@author GanAH 2019/9/19.
"""


class SatelliteOrbetEtc():
    def __init__(self):
        pass

    def orbetEtc(self,t_epoch, single_epoch_data):
        """
         卫星位置定轨计算函数
        :param times the times of satellite
        :param t_epoch: 观测历元时间
        :param single_epoch_data: 一个观测历元的数据
        :return: matrixXYZ 地固坐标系
        """
        # 参数预定义,定义数组参数属性


        Crs = single_epoch_data[0][1]
        An = single_epoch_data[0][2]
        Mo = single_epoch_data[0][3]

        Cuc = single_epoch_data[1][0]
        e = single_epoch_data[1][1]
        Cus = single_epoch_data[1][2]
        sqrt_A = single_epoch_data[1][3]

        t_oe = single_epoch_data[2][0]
        Cic = single_epoch_data[2][1]
        OMEGA_0 = single_epoch_data[2][2]
        Cis = single_epoch_data[2][3]

        io = single_epoch_data[3][0]
        Crc = single_epoch_data[3][1]
        w = single_epoch_data[3][2]
        OMEGA_dot = single_epoch_data[3][3]

        i_dot = single_epoch_data[4][0]

        GAST_week = single_epoch_data[4][2]

        GM = 3.9860047E14  # 注意这个参数，最开始就这个参数没有处理好！
        w_e = 7.2921151467E-5  # rad/s,不能少位，如：7.292115

        # 计算卫星平均角速度
        n0 = math.sqrt(GM) / sqrt_A ** 3
        # 对平均运动角速度进行改正
        n = n0 + An
        # 计算平近点角M
        M = Mo + n * (t_epoch - t_oe)
        # 获取偏近点角E
        E = self.getSatellite_E(M, e)
        # 计算真近点角f
        f = math.atan(math.sqrt(1 - e ** 2) * sin(E) / (cos(E) - e))
        # 计算升交角距
        u = w + f
        # 计算摄动改正数
        q_u = Cuc * cos(2 * u) + Cus * sin(2 * u)
        q_r = Crc * cos(2 * u) + Crs * sin(2 * u)
        q_i = Cic * cos(2 * u) + Cis * sin(2 * u)
        # 摄动改正,a为长半径
        a = sqrt_A ** 2
        u = u + q_u
        r = a * (1 - e * cos(E)) + q_r

        t_k = t_epoch - t_oe
        if t_k > 302400.0:
            t_k = t_k - 604800.0
        elif t_k <-302400.0:
            t_k = t_k + 604800.0
        i = io + q_i + i_dot * t_k  # i_dot:i的变化率，摄动九参数给出

        # 计算坐标,轨道面坐标系坐标
        x = r * cos(u)
        y = r * sin(u)

        # 计算瞬时升交角经度L
        L = OMEGA_0 + (OMEGA_dot - w_e) * t_epoch - OMEGA_dot * t_oe

        # 计算卫星在瞬时地球坐标系的位置
        matrixXYZ = mat([[x * cos(L) - y * cos(i) * sin(L)],
                         [x * sin(L) + y * cos(i) * cos(L)],
                         [y * sin(i)]])

        # 计算卫星在协议地球坐标系的位置
        # matrix_p = mat([[1, 0, x],
        #                 [0, 1, -y],
        #                 [-x, y, 1]])
        # matrix_xyzCTS = matrix_p * matrixXYZ

        # 改正卫星钟差


        # 目前只返回部分结果，后期存入数据库以供界面其他功能调用
        return matrixXYZ

    def getSatellite_E(self, M, e):

        """
        计算偏近点角E
        :param M 真近点角 弧度
        :param e 椭圆轨道偏心率
        :return E
        """
        E = M
        a = 0
        while a < 100:
            controlNumber = E
            E = E + ((M - E + e * math.sin(E)) / (1 - e * math.cos(E)))
            a = a + 1
            if (abs(controlNumber - E) < 0.000001):
                return E  # 不用额外添加break退出
