# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'welcomeWight.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(739, 433)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.commandLinkButton_2 = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton_2.setObjectName("commandLinkButton_2")
        self.verticalLayout.addWidget(self.commandLinkButton_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.commandLinkButton_2.setText(_translate("Form", "欢迎使用EMACS测量软件"))
        self.commandLinkButton_2.setDescription(_translate("Form", "1.请在菜单栏选择相应的功能完成指定操作；\n"
"2.该软件为工程测量相关计算的集成；\n"
"3.详细使用帮助，请查看文档。"))
