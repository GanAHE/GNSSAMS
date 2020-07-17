#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 主函数

@author: GanAH  2020/2/20.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import sys, os
import time

from PyQt5 import QtCore, QtWidgets,QtGui

from database.database import Database

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from window import windowDS
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt5.QtGui import QPixmap

class SplashPanel(QtWidgets.QSplashScreen):

    def __init__(self):
        super(SplashPanel, self).__init__()
        message_font = QtGui.QFont()
        message_font.setBold(True)
        message_font.setPointSize(14)
        self.setFont(message_font)
        # 创建启动界面，支持png透明图片
        self.setPixmap(QtGui.QPixmap("./source/EMACS.png"))
        # 淡入效果
        self.setWindowOpacity(0)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() + 0.03
            if newOpacity > 1:
                break
            self.setWindowOpacity(newOpacity)
            self.show()
            t -= 1
            time.sleep(0.02)

        # 启动信息
        self.showMessage('加载配置文件...', alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, color=QtCore.Qt.black)

        # 加载配置文件
        # Database().loadJsonConfig()
        time.sleep(2)

        self.showMessage("完成所有配置文件载入，请稍等...", alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter,
                         color=QtCore.Qt.black)
        time.sleep(1)
        # 淡出效果
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() - 0.01
            if newOpacity < 0:
                break
            self.setWindowOpacity(newOpacity)
            t += 1
            time.sleep(0.03)
        # 关闭启动画面
        # splash.close()

    def mousePressEvent(self, evt):
        pass
        # 重写鼠标点击事件，阻止点击后消失

    def mouseDoubleClickEvent(self, *args, **kwargs):
        pass
        # 重写鼠标双击事件，阻止出现卡顿现象

    def enterEvent(self, *args, **kwargs):
        pass
        # 重写鼠标移动事件，阻止出现卡顿现象

    def mouseMoveEvent(self, *args, **kwargs):
        pass
        # 重写鼠标移动事件，阻止出现卡顿现象


if __name__ == '__main__':
    # 窗体构建
    app = QApplication(sys.argv)
    # 启动页面
    splash = SplashPanel()
    # 设置进程，启动加载页面时可以进行其他操作而不会卡死
    app.processEvents()

    MainWindow = QMainWindow()
    # 已定界面 windows
    # ui = window.Ui_mainWindow()
    # 界面重构存储区域
    ui = windowDS.Ui_mainWindow()
    ui.setupUi(MainWindow)
    # MainWindow.show()
    MainWindow.showMaximized()
    splash.finish(MainWindow)
    splash.deleteLater()
    sys.exit(app.exec_())
