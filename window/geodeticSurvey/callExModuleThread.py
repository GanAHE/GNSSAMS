#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
project: EMACS
comment: 扩展模块唤醒线程

@author: GanAHE  2020/9/17.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import os
from PyQt5.QtCore import pyqtSignal, QThread
import glob
import cv2
from tqdm import tqdm
import numpy as np


class CallExModule(QThread):
    infoEmit = pyqtSignal(str, str)

    def __init__(self):
        super(CallExModule, self).__init__()

    def setPara(self, paraDict):
        self.paraDict = paraDict

    def run(self) -> None:
        code = self.paraDict["code"]
        if code == 100:
            self.callVisualSFM()
        elif code == 101:
            self.callMeshLab()
        else:
            self.getPara_CHESE()

    def sendInfo(self, type, strInfo):
        self.infoEmit.emit(type, strInfo)

    def callVisualSFM(self):
        rootDir = "./source/exModule/VMCS/VisualSFM.exe"
        rootDir = os.path.abspath(rootDir)
        try:
            r_v = os.system(rootDir)
            self.sendInfo("3D", " -[{}] 关闭 VisualSFM 三维重建模块，代码：{}".format("SFM", r_v))
            self.sendInfo("3D", " -[MeshLab]  已完成 图像匹配与点云生成，即将自动启动 MeshLab 模块...")
            self.callMeshLab()
        except Exception as e:
            self.sendInfo("E", "路径错误，扩展模块未加载！\n详细信息：" + e.__str__())

    def callMeshLab(self):
        rootDir = "./source/exModule/VMCS/MeshLab/meshlab.exe"
        rootDir = os.path.abspath(rootDir)
        try:
            r_v = os.system(rootDir)
            self.sendInfo("3D", " -[{}] 关闭 MeshLab 三维重建模块，代码：{}".format("MeshLab", r_v))
            self.sendInfo("T", "关闭扩展模块")
        except Exception as e:
            self.sendInfo("E", "路径错误，扩展模块未加载！\n详细信息：" + e.__str__())

    def getPara_CHESE(self):
        """
        棋盘法（张正友法）获取相机内参
        :param : 标准像片
        :return:
        """
        # 设置棋盘板长宽
        chessboard_size = (9, 6)

        # 定义数组存储检测到的点
        obj_points = []  # 真实世界中的三维坐标
        img_points = []  # 图片平面的二维坐标

        ####准备目标坐标 （0，0，0），（1，0，0）...（9，6，0）
        # 设置世界坐标下的坐标值
        # 假设棋盘正好在x-y平面上，z直接取零，从而简化初始步骤
        # objp包含的是10*7每一角点的坐标
        objp = np.zeros((np.prod(chessboard_size), 3), np.float32)  # 9*6个三维坐标
        objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

        # 读取图片，使用glob文件名管理工具
        calibration_paths = self.paraDict["paths"]

        # 对每张图片，识别出角点，记录世界物体坐标和图像坐标
        index = 1
        for img_path in calibration_paths:
            # 进度条监控模拟效果
            self.sendInfo("3D",
                          " -[相机参数] 进行中：{} {} {}/{}".format("#" * index, " " * (len(calibration_paths) - index), index,
                                                            len(calibration_paths)))
            index += 1
            # 加载图片
            img = cv2.imread(img_path)
            # 照片太大 缩小一半 (不能缩小!!!!内参会变！！像素变小了 并不是对原图像处理)
            # img = cv2.resize(img, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #
            # cv2.imshow('i',img)
            # cv2.waitKey(0)
            # 寻找角点将其存入corners(该图片9*6个角点坐标)，ret是找到角点的标志(True/False)
            ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

            if ret == True:
                # 检测到角点执行以下操作（一般都能检测到角点，除非图片不是规定的棋盘格）
                # 定义角点精准化迭代过程的终止条件 （包括精度和迭代次数）
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.0010)
                # 执行亚像素级角点检测
                corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)

                obj_points.append(objp)
                img_points.append(corners2)

            # 可视化角点
            # img = cv2.drawChessboardCorners(gray,(9,6),corners2,ret)
            # cv2.imshow('s',img)
            # cv2.waitKey(100)

        self.sendInfo("3D", " 完成.")
        # 相机标定
        # 每张图片都有自己的旋转和平移矩阵 但是相机内参是畸变系数只有一组（因为相机没变，焦距和主心坐标是一样的）
        ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
        saveDir, name = os.path.split(calibration_paths[0])
        # 保存参数
        np.save(saveDir + "ret", ret)
        np.save(saveDir + "K", K)
        np.save(saveDir + "dist", dist)
        np.save(saveDir + "rvecs", rvecs)
        np.save(saveDir + "tvecs", tvecs)

        self.sendInfo("3D", " 相机参数：{}".format(K))

    def killThread(self):
        self.terminate()
