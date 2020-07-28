# -*- coding: utf-8 -*-

from numpy import sin, cos, arctan, sqrt, mat, rad2deg, deg2rad


def getSatellitePositon(t_epoch, single_epoch_data):
    """
     卫星位置定轨计算函数
    :param times the times of satellite
    :param t_epoch: 观测历元时间
    :param single_epoch_data: 一个观测历元的数据 List
    :return: matrixXYZ 地固坐标系
    """
    # 参数预定义,定义数组参数属性
    # 轨道一数据
    Crs = single_epoch_data[0][1]
    An = single_epoch_data[0][2]
    Mo = single_epoch_data[0][3]
    # 轨道二数据
    Cuc = single_epoch_data[1][0]
    e = single_epoch_data[1][1]
    Cus = single_epoch_data[1][2]
    sqrt_A = single_epoch_data[1][3]
    # 轨道三数据
    t_oe = single_epoch_data[2][0]
    Cic = single_epoch_data[2][1]
    OMEGA_0 = single_epoch_data[2][2]
    Cis = single_epoch_data[2][3]
    # 轨道四数据
    io = single_epoch_data[3][0]
    Crc = single_epoch_data[3][1]
    w = single_epoch_data[3][2]
    OMEGA_dot = single_epoch_data[3][3]
    # 其他数据
    i_dot = single_epoch_data[4][0]

    # GAST_week = single_epoch_data[4][2]

    GM = 3.9860047E14  # 注意这个参数，最开始就这个参数没有处理好！
    w_e = 7.2921151467E-5  # rad/s,不能少位，如：7.292115

    # 计算卫星平均角速度
    n0 = sqrt(GM) / (sqrt_A ** 3)
    # 对平均运动角速度进行改正
    n = n0 + An

    # 钟差改正
    # 先改正后解算
    # 计算平近点角M
    M = Mo + n * (t_epoch - t_oe)
    # 获取偏近点角E
    E = getSatellite_E(M, e)
    # 计算真近点角f
    f = arctan(sqrt(1 - e ** 2) * sin(E) / (cos(E) - e))
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
    elif t_k < -302400.0:
        t_k = t_k + 604800.0
    i = io + q_i + i_dot * t_k  # i_dot:i的变化率，摄动九参数给出

    # 计算坐标,轨道面坐标系坐标
    x = r * cos(u)
    y = r * sin(u)

    # 计算瞬时升交角经度L
    L = OMEGA_0 + (OMEGA_dot - w_e) * t_epoch - OMEGA_dot * t_oe

    # 计算卫星在瞬时地球坐标系的位置-地固坐标系
    matrixXYZ = mat([[x * cos(L) - y * cos(i) * sin(L)],
                     [x * sin(L) + y * cos(i) * cos(L)],
                     [y * sin(i)]])

    # 计算卫星在协议地球坐标系的位置
    # matrix_p = mat([[1, 0, x],
    #                 [0, 1, -y],
    #                 [-x, y, 1]])
    # matrix_xyzCTS = matrix_p * matrixXYZ

    # 目前只返回部分结果，后期存入数据库以供界面其他功能调用
    return matrixXYZ.tolist()


def getSatellitePositon_II(t_epoch, epoch_data):
    """
     卫星位置定轨计算函数
    :param t_epoch: 观测历元时间
    :param epoch_data: 一个观测历元的数据 List
    :return: matrixXYZ 地固坐标系
    """
    # 参数预定义,定义数组参数属性
    # 轨道一数据
    clockBias = float(epoch_data[0])
    clockDrift = float(epoch_data[1])
    clockDriftRate = float(epoch_data[2])

    Crs = epoch_data[11]
    An = epoch_data[7]
    Mo = epoch_data[5]
    # 轨道二数据
    Cuc = epoch_data[10]
    e = epoch_data[6]
    Cus = epoch_data[9]
    sqrt_A = epoch_data[3]
    # 轨道三数据
    t_oe = epoch_data[4]
    Cic = epoch_data[14]
    OMEGA_0 = epoch_data[17]
    Cis = epoch_data[13]
    # 轨道四数据
    io = epoch_data[16]
    Crc = epoch_data[12]
    w = epoch_data[8]
    OMEGA_dot = epoch_data[18]
    # 其他数据
    i_dot = epoch_data[15]

    GM = 3.9860047E14  # 注意这个参数，最开始就这个参数没有处理好！
    w_e = 7.2921151467E-5  # rad/s,不能少位，如：7.292115

    # 计算卫星平均角速度
    n0 = sqrt(GM) / (sqrt_A ** 3)
    # 对平均运动角速度进行改正
    n = n0 + An

    # 钟差改正
    teta_t = clockBias+clockDrift*(t_epoch-t_oe) + clockDriftRate*(t_epoch-t_oe)*(t_epoch-t_oe)
    t_epoch = t_epoch - teta_t
    # 计算平近点角M
    M = Mo + n * (t_epoch - t_oe)
    # 获取偏近点角E
    E = getSatellite_E(M, e)
    # 相对论效应
    teta_tr = -2290 * e * sin(E) * 1e-9
    t_epoch = t_epoch - teta_tr
    # 计算真近点角f
    f = arctan(sqrt(1 - e ** 2) * sin(E) / (cos(E) - e))
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
    elif t_k < -302400.0:
        t_k = t_k + 604800.0
    i = io + q_i + i_dot * t_k  # i_dot:i的变化率，摄动九参数给出

    # 计算坐标,轨道面坐标系坐标
    x = r * cos(u)
    y = r * sin(u)

    # 计算瞬时升交角经度L
    L = OMEGA_0 + (OMEGA_dot - w_e) * t_epoch - OMEGA_dot * t_oe

    # 计算卫星在瞬时地球坐标系的位置-地固坐标系
    matrixXYZ = mat([[x * cos(L) - y * cos(i) * sin(L)],
                     [x * sin(L) + y * cos(i) * cos(L)],
                     [y * sin(i)]])

    # 计算卫星在协议地球坐标系的位置
    # matrix_p = mat([[1, 0, x],
    #                 [0, 1, -y],
    #                 [-x, y, 1]])
    # matrix_xyzCTS = matrix_p * matrixXYZ

    # 目前只返回部分结果，后期存入数据库以供界面其他功能调用
    return teta_t + teta_tr, matrixXYZ.tolist()


def getSatellite_E(M, e):
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
        E = E + ((M - E + e * sin(E)) / (1 - e * cos(E)))
        a = a + 1
        if (abs(controlNumber - E) < 0.000001):
            return E  # 不用额外添加break退出


# epoch = [
#     [0.700000000000E+01, -0.129125000000E+03, 0.404481133977E-08, -0.662342822517E+00],
#     [-0.646337866783E-05, 0.100609987276E-01, 0.664591789246E-05, 0.515370931625E+04],
#     [0.518400000000E+06, 0.949949026108E-07, 0.219590371049E+01, 0.163912773132E-06],
#     [0.980759197334E+00, 0.262937500000E+03, 0.806901474822E+00, -0.799961893052E-08],
#     [-0.800033324599E-10, 0.100000000000E+01, 0.211400000000E+04, 0.000000000000E+00],
#     [0.200000000000E+01, 0.000000000000E+00, 0.512227416039E-08, 0.700000000000E+01],
#     [0.511218000000E+06, 0.400000000000E+01, 0.000000000000E+00, 0.000000000000E+00]
# ]
# print(getSatellitePositon(0.511218000000E+06, epoch))
# print(getSatellite_E(20, 0.0236))
