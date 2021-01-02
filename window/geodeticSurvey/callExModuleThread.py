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
import multiprocessing
import cv2
from database.database import Database
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import pyqtSignal, QThread
from geodeticSurvey.mvs import videoKeyFrameToImage


class CallExModule(QThread):
    infoEmit = pyqtSignal(str, str)

    def __init__(self):
        super(CallExModule, self).__init__()

    def setPara(self, paraDict):
        self.paraDict = paraDict

    def run(self) -> None:
        code = self.paraDict["code"]
        try:
            if code == 100:
                self.callVisualSFM()
            elif code == 101:
                self.callMeshLab()
            elif code == 102:
                self.calib()
            else:
                self.videoFrame()
        except Exception as e:
            self.sendInfo("E", "异常警告！具体信息：" + e.__str__())

        self.sendInfo("kill", "")

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

    def calib(self):
        """
        棋盘法相机标定
        :return:
        """
        self.sendInfo("3D", " -[Camera] 开始检校...")
        horizontalCount = self.paraDict["horizontalCount"]
        verticalCount = self.paraDict["verticalCount"]
        # cp_int: 将世界地图中的角点坐标保存为 int 格式
        # 示例： (0,0,0), (1,0,0), (2,0,0) ....,(10,7,0).
        cp_int = np.zeros((horizontalCount * verticalCount, 3), np.float32)
        cp_int[:, :2] = np.mgrid[0:horizontalCount, 0:verticalCount].T.reshape(-1, 2)
        # cp_world: 将角点坐标存入世界坐标
        cp_world = cp_int * (self.paraDict["cellSize"] / 1000)
        # 世界坐标点
        obj_points = []
        # 图像空间中的点（与obj_points相关）
        img_points = []
        images = self.paraDict["paths"]
        i = 1
        for fname in images:
            # 模拟进度条
            self.sendInfo("3D",
                          " -[Camera] 解算中：{} {} | {}/{}".format("✈" * i, "-" * (len(images) - i), i, len(images)))
            i += 1
            img = cv2.imread(fname)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 求ret,cp_img:像素空间中的角点
            ret, cp_img = cv2.findChessboardCorners(gray_img, (horizontalCount, verticalCount), None)
            # 角点规格正确，标记成功
            if ret == True:
                # cv2.cornerSubPix(gray_img,cp_img,(11,11),(-1,-1),criteria)
                obj_points.append(cp_world)
                img_points.append(cp_img)
                if self.paraDict["autoSaveCorner"] is True:
                    # view and save the corners
                    cv2.drawChessboardCorners(img, (horizontalCount, verticalCount), cp_img, ret)
                    saveDir = Database.workspace + "/corner_sign"
                    if os.path.exists(saveDir) is False:  # 路径不存在，创建
                        os.mkdir(saveDir)
                    dir, name = os.path.split(fname)
                    cv2.imwrite(saveDir + "/corner_" + name, img)
                    # cv2.imshow('FoundCorners', img)
                    # cv2.waitKey(1)
            else:
                self.sendInfo("3D", " -[Camera] 当前影像查找角点错误,剔除：{} ".format(fname))
        # cv2.destroyAllWindows()

        if len(img_points) > 0:

            # 校准相机
            ret, mat_inter, coff_dis, v_rot, v_trans = cv2.calibrateCamera(obj_points, img_points, gray_img.shape[::-1],
                                                                           None, None)
            self.sendInfo("3D", " -[Camera] 外参 ret:{}".format(ret))
            self.sendInfo("3D", " -[Camera] 内参矩阵(internal matrix):{}".format(mat_inter))
            # in the form of (k_1,k_2,p_1,p_2,k_3)
            self.sendInfo("3D", " -[Camera] 畸变系数(distortion cofficients):{}".format(coff_dis))
            self.sendInfo("3D", " -[Camera] 旋转矢量(rotation vectors):{}".format(v_rot))
            self.sendInfo("3D", " -[Camera] 平移向量(translation vectors):{}".format(v_trans))
            # calculate the error of reproject
            total_error = 0
            for i in range(len(obj_points)):
                img_points_repro, _ = cv2.projectPoints(obj_points[i], v_rot[i], v_trans[i], mat_inter, coff_dis)
                error = cv2.norm(img_points[i], img_points_repro, cv2.NORM_L2) / len(img_points_repro)
                total_error += error
            self.sendInfo("3D", " -[Camera] 参数估计-平均误差:{} ".format(total_error / len(obj_points)))
        else:
            self.sendInfo("3D", " -[Camera] 角点无法检出，棋盘规格设置错误，或是图像效果较差无法识别,请检查！")

    def ca(self):
        videoKeyFrameToImage.call(self.paraDict["videoPath"])
    def videoFrame(self):
        """

        :return:
        """

        self.sendInfo("3D","执行视频关键帧抽帧...")
        pool = multiprocessing.Pool(processes=10)
        videoPath = self.paraDict["videoPath"]
        totalFrames = videoKeyFrameToImage.video2frame(videoPath)
        self.sendInfo("3D","dfdfg")
        # self.sendInfo("3D", "there are {} frames in video".format(len(totalFrames)))
        h, w, _ = totalFrames[0].shape
        hist = pool.map(videoKeyFrameToImage.calc_hist, totalFrames)
        self.sendInfo("3D", 'hist.shape: {}'.format(hist[0].shape))
        # print('hist[0]: {}'.format(hist[0]))

        si = videoKeyFrameToImage.similarity(hist[50], hist[60])
        self.sendInfo("3D", 'similarity between two frames: {}'.format(si))
        # print((hist[1]+hist[2]+hist[3])/3)
        cents, results = videoKeyFrameToImage.ekf(hist)
        self.sendInfo("3D", " {} {}".format(len(cents), results))
        # to_show = cv2.cvtColor(total_frames[cents[0][-1]], cv2.COLOR_BGR2RGB)
        # plt.imshow(to_show)
        # plt.show()
        self.sendInfo("3D", str(type(totalFrames[0])))
        # 创建文件夹
        frameDir, name = os.path.split(videoPath)
        frameDir = frameDir + "/" + name + "_keyFrame"
        if os.path.exists(frameDir) is False:  # 路径不存在，创建
            os.mkdir(frameDir)
        self.sendInfo("3D", "成功创建文件夹，抽取的关键帧将保存在：{}".format(frameDir))
        k = 0
        for inm in totalFrames:
            self.sendInfo("3D", "关键帧提取中:" + str(k + 1))
            to_show = cv2.cvtColor(totalFrames[k], cv2.COLOR_BGR2RGB)
            plt.imsave(frameDir + "/" + name + "_frame_" + str(k) + ".jpg", to_show)
            # plt.imshow(to_show)
            # plt.show()
            # inm.save("./te/" + str(k) + ".jpg")
            # cv2.imwrite("./te/" + str(k) + ".jpg", inm)
            k += 1

    def killThread(self):
        self.terminate()
