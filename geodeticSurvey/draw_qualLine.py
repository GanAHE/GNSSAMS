#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 绘制场绘图

@author: GanAH  2020/7/6.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import csv

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

from database.database import Database


def gravityQualLine(X_v, Y_v, value):
    X, Y = np.meshgrid(np.array(X_v), np.array(Y_v))  # 网格化
    po = []
    C = plt.contour(X, Y, D(X, Y, value), 10, colors='black')  # 生成等值线图
    plt.contourf(X, Y, D(X, Y, value), 10)
    plt.clabel(C, inline=1, fontsize=10)
    plt.colorbar()
    plt.show()


def D(x, y, value):
    return np.exp(-x ** 2 - y ** 2) + value


def line(X_v, Y_v, value):
    xi = np.linspace(min(X_v), max(X_v), len(X_v))
    yi = np.linspace(min(Y_v), max(Y_v), len(Y_v))
    X, Y = np.meshgrid(xi, yi)  # 网格化
    po = []
    for i in range(len(X_v)):
        point = []
        point.append(X_v[i])
        point.append(Y_v[i])
        po.append(point)
    po = np.array(po)
    zi = griddata(po, value, (X, Y), method='nearest')
    C = plt.contour(X, Y, zi, 10, colors='black')  # 生成等值线图
    plt.contourf(X, Y, zi, 10)
    plt.clabel(C, inline=1, fontsize=10)
    plt.colorbar()
    plt.show()


def example():
    dx = 0.01
    dy = 0.01
    x = np.arange(-2.0, 2.0, dx)
    y = np.arange(-2.0, 2.0, dy)
    X, Y = np.meshgrid(x, y)
    C = plt.contour(X, Y, -f(X, Y), 15, colors='black')  # 生成等值线图
    plt.contourf(X, Y, -f(X, Y), 15)
    plt.clabel(C, inline=1, fontsize=10)
    plt.colorbar()
    plt.show()


def f(x, y):
    return (1 - y ** 5 + x ** 5) * np.exp(-x ** 2 - y ** 2) * 10


def ThreeDNet(X_v, Y_v, value):
    """
    三维折线
    :param X_v:
    :param Y_v:
    :param value:
    :return:
    """
    fig = plt.figure()
    ax = Axes3D(fig)

    xi = np.linspace(min(X_v), max(X_v), len(X_v))
    yi = np.linspace(min(Y_v), max(Y_v), len(Y_v))
    x, y = np.meshgrid(xi, yi)
    r = np.sqrt(x / x + y / y)
    z = r / r + value

    ax.plot_surface(x, y, z, rstride=1,  # row 行步长
                    cstride=2,  # colum 列步长
                    cmap='rainbow')  # 渐变颜色
    ax.contourf(x, y, z,
                zdir='z',  # 使用数据方向
                offset=-2,  # 填充投影轮廓位置
                cmap='rainbow')
    ax.set_zlim(-15, 15)

    plt.show()
    return fig

def sow(X_v, Y_v, value):
    """
    双页面信息
    :param X_v:
    :param Y_v:
    :param value:
    :return:
    """
    x = np.array(X_v)
    y = np.array(Y_v)
    z = np.array(value)
    # 准备待插值位置
    xi = np.linspace(x.min(), x.max(), 200)
    yi = np.linspace(y.min(), y.max(), 200)
    X, Y = np.meshgrid(xi, yi)
    # 插值
    Z = griddata((x, y), z, (X, Y), method='nearest')
    # 绘图
    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='jet')
    ax1.contour(X, Y, Z, cmap='jet')
    ax1.set_zlim(-15, 15)

    ax2 = fig.add_subplot(122)
    ax2.contourf(X, Y, Z, cmap='jet')
    plt.tight_layout()
    plt.show()
    return fig


# a = [
#     -1, -2, -3, -4, -5
# ]
# b = [-1, -2, -3, -4, -5]
# v = [5, -6, 17, 45, -6]
# # gravityQualLine(a, b, np.array(v))
# gravityQualLine(a, b, v)
# example()

def drawSub(lon,lat,err1):
    # 开始绘图
    x = np.array(lon)
    y = np.array(lat)
    z = np.array(err1)
    # 准备待插值位置
    xi = np.linspace(x.min(), x.max(), 200)
    yi = np.linspace(y.min(), y.max(), 200)
    X, Y = np.meshgrid(xi, yi)
    # 插值
    Z = griddata((x, y), z, (X, Y), method='nearest')
    # 绘图
    fig = plt.figure(dpi=150)
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='jet')
    ax1.contour(X, Y, Z, cmap='jet')
    ax1.set_zlim(-15, 15)

    ax2 = fig.add_subplot(222)
    ax2.contourf(X, Y, Z, cmap='jet')

    ax3 = fig.add_subplot(223, projection='3d')
    xi = np.linspace(min(lon), max(lat), len(err1))
    yi = np.linspace(min(lon), max(lat), len(err1))
    x, y = np.meshgrid(xi, yi)
    r = np.sqrt(x / x + y / y)
    z = r / r + err1
    ax3.plot_surface(x, y, z, rstride=1,  # row 行步长
                     cstride=2,  # colum 列步长
                     cmap='rainbow')  # 渐变颜色
    ax3.contourf(x, y, z,
                 zdir='z',  # 使用数据方向
                 offset=-2,  # 填充投影轮廓位置
                 cmap='rainbow')
    ax3.set_zlim(-15, 15)

    ax4 = fig.add_subplot(224)
    x = np.arange(-2.0, 2.0, 0.01)
    y = np.arange(-2.0, 2.0, 0.01)
    X, Y = np.meshgrid(x, y)
    C = plt.contour(X, Y, -f(X, Y), 15, colors='black')  # 生成等值线图
    ax4.contourf(X, Y, -f(X, Y), 15)
    ax4.clabel(C, inline=1, fontsize=10)
    plt.colorbar()
    # ax4.contourf(X, Y, Z, cmap='jet')
    plt.tight_layout()
    plt.show()
    return fig

def drawGravityAnomaly():
    # 数据库获取文件
    data = Database.gravityAnomalyData
    lon = []
    lat = []
    err1 = []
    err2 = []
    if len(data)> 5:
        for i in range(len(data)):
            lineData = list(map(float, data[i][1:]))
            lon.append(lineData[0])
            lat.append(lineData[1])
            err1.append(lineData[4])
            if len(lineData) == 6:
                err2.append(lineData[5])
    # 开始绘图
    fig = drawSub(lon,lat,err1)
    if len(err2) > 0:
        # 绘图
        fig = drawSub(lon, lat, err2)

    return fig


def drawGrid():
    filePath = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\Grid.csv"
    Lon = []
    lat = []
    H = []
    err1 = []
    err2 = []
    err3 = []
    err4 = []
    with open(filePath, "r") as F:
        re = csv.reader(F)
        c = 1
        for row in re:
            if c == 1:
                c = 2
                print("Head", row)
            else:
                lineData = list(map(float, row[0:6]))
                Lon.append(lineData[0])
                lat.append(lineData[1])
                H.append(lineData[2])
                err1.append(lineData[4])
                err2.append(lineData[5])
                err3.append(lineData[6])
                err4.append(lineData[7])
    F.close()
    # ThreeDNet(Lon, lat, err2)
    ThreeDNet(Lon, lat, err4)
    sow(Lon, lat, err4)


def drawNet():
    filePath = "E:/文档/2020 - 物理大地测量学实习/数据/NetRe.csv"
    Lon = []
    lat = []
    H = []
    err1 = []
    err2 = []
    err3 = []
    err4 = []
    with open(filePath, "r") as F:
        re = csv.reader(F)
        c = 1
        for row in re:
            if c == 1:
                c = 2
                print("Head", row)
            else:
                lineData = list(map(float, row))
                Lon.append(lineData[1])
                lat.append(lineData[2])
                H.append(lineData[3])
                err1.append(lineData[6])
                err2.append(lineData[7])
                err3.append(lineData[8])
                err4.append(lineData[9])
    F.close()
    # ThreeDNet(Lon, lat, err1)
    # ThreeDNet(Lon, lat, err2)
    ThreeDNet(Lon, lat, err3)
    # ThreeDNet(Lon, lat, err4)
    # line(Lon,lat,err2)
    # sow(Lon, lat, err1)
    sow(Lon, lat, err3)


# drawGrid()
# drawNet()
# example()