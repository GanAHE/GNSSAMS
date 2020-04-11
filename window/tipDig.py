#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:消息异常提醒小弹窗

@author: GanAH  2019/10/30.
@version 2.0.
@contact: dinggan@whu.edu.cn
"""
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore


class ActionWarnException(QtCore.QObject):

    def __init__(self, parentWight):
        super(ActionWarnException, self).__init__()
        self.Qwight = parentWight

    def actionWarnException(self, type, text):
        # 从数据库获取异常消息
        if type == "E":
            QMessageBox.critical(self.Qwight, "【☠错误༺༒༻警告☠】", text)
        elif type == "W":
            QMessageBox.warning(self.Qwight, "【⚠异常༺༒༻警告⚠】", text)
        elif type == "O":
            QMessageBox.warning(self.Qwight, "【未知༺ཌ༈༒༈ད༻警告】", "干啥呢？")
        else:
            reply = QMessageBox.information(self.Qwight, "【☠说༺༒༻明☠】", text,
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

