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
from window import windowDS,window
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    # 窗体构建（时间紧迫，未完成逻辑调用）
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    #已定界面 windows
    # ui = window.Ui_mainWindow()
    # 界面重构存储区域
    ui = windowDS.Ui_mainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())