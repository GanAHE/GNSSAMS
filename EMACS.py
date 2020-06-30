#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 主函数

@author: GanAH  2020/2/20.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import sys, os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from window import windowDS
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt5.QtGui import QPixmap

if __name__ == '__main__':
    # 窗体构建
    app = QApplication(sys.argv)
    # 创建启动界面，支持png透明图片
    splash = QSplashScreen(QPixmap("./source/EMACS.png"))
    splash.show()
    # 可以显示启动信息
    splash.showMessage('正在加载……')
    # 载入配置文件
    splash.showMessage('正在加载配置文件……')

    MainWindow = QMainWindow()
    # 已定界面 windows
    # ui = window.Ui_mainWindow()
    # 界面重构存储区域
    ui = windowDS.Ui_mainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
