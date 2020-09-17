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


class CallExModule(QThread):
    infoEmit = pyqtSignal(str, str)

    def __init__(self):
        super(CallExModule, self).__init__()

    def setPara(self, paraDict):
        self.code = paraDict["code"]

    def run(self) -> None:
        if self.code == 100:
            self.callVisualSFM()
        elif self.code == 101:
            self.callMeshLab()
        else:
            self.sendInfo("E", "小肚鸡肠")

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

    def killThread(self):
        self.terminate()
