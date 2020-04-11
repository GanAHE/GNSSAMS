# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coorTranOpenFileDiaog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from database.database import Database
from window.file.operationFile import OperationFile


class Ui_Dialog(QtCore.QObject):
    fileReadEmit = QtCore.pyqtSignal(int,str)
    infoEmit = QtCore.pyqtSignal(str, str)

    def setupUi(self, Dialog):
        # 特别加入
        self.parentWidget = QtWidgets.QDialog(Dialog)
        Dialog.setObjectName("Dialog")
        Dialog.resize(614, 421)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./source/icon/icon_个人设置.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setModal(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("./source/icon/futuro_icons_547.png"))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton_commaSymbal = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_commaSymbal.setChecked(True)
        self.radioButton_commaSymbal.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.radioButton_commaSymbal.setObjectName("radioButton_commaSymbal")
        self.verticalLayout_2.addWidget(self.radioButton_commaSymbal)
        self.radioButton_blank = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_blank.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.radioButton_blank.setObjectName("radioButton_blank")
        self.verticalLayout_2.addWidget(self.radioButton_blank)
        self.radioButton_other = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_other.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.radioButton_other.setObjectName("radioButton_other")
        self.verticalLayout_2.addWidget(self.radioButton_other)
        self.lineEdit_otherSparate = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_otherSparate.setPlaceholderText("")
        self.lineEdit_otherSparate.setObjectName("lineEdit_otherSparate")
        self.verticalLayout_2.addWidget(self.lineEdit_otherSparate)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_openSource = QtWidgets.QPushButton(self.groupBox_2)
        self.button_openSource.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_openSource.setObjectName("button_openSource")
        self.horizontalLayout.addWidget(self.button_openSource)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_source = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_source.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lineEdit_source.setReadOnly(True)
        self.lineEdit_source.setObjectName("lineEdit_source")
        self.horizontalLayout.addWidget(self.lineEdit_source)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_openTarget = QtWidgets.QPushButton(self.groupBox_2)
        self.button_openTarget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_openTarget.setObjectName("button_openTarget")
        self.horizontalLayout_2.addWidget(self.button_openTarget)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_target = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.lineEdit_target.setFont(font)
        self.lineEdit_target.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.lineEdit_target.setToolTip("")
        self.lineEdit_target.setText("")
        self.lineEdit_target.setReadOnly(True)
        self.lineEdit_target.setObjectName("lineEdit_target")
        self.horizontalLayout_2.addWidget(self.lineEdit_target)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.button_openSource.clicked.connect(self.opensourceFile)
        self.button_openTarget.clicked.connect(self.openTargetFile)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "坐标转换数据导入"))
        self.label.setText(_translate("Dialog", "导入坐标转换数据"))
        self.groupBox.setTitle(_translate("Dialog", "文本数据分隔方式"))
        self.radioButton_commaSymbal.setText(_translate("Dialog", "英文逗号"))
        self.radioButton_blank.setText(_translate("Dialog", "空格"))
        self.radioButton_other.setText(_translate("Dialog", "其他分隔符"))
        self.groupBox_2.setTitle(_translate("Dialog", "文件导入"))
        self.button_openSource.setText(_translate("Dialog", "导入原始坐标文件"))
        self.label_2.setText(_translate("Dialog", "文件路径："))
        self.button_openTarget.setText(_translate("Dialog", "导入目标坐标文件"))
        self.label_3.setText(_translate("Dialog", "文件路径："))
        self.label_4.setText(_translate("Dialog", "说明：转换后的坐标以原始坐标进行转换"))

    def opensourceFile(self):
        try:
            filePath, dataList = self._openFileWight()
            self.lineEdit_source.setText(str(filePath))
            Database.coorTranSourceData = self._getSparateData(dataList)
            # 发送信号
            dirPath = os.path.dirname(os.path.realpath(filePath))
            self.fileReadEmit.emit(0,dirPath)

        except Exception as e:
            self.infoEmit.emit("I", "取消或文件为空,其它信息：" + e.args.__str__())

    def openTargetFile(self):
        try:
            filePath, dataList = self._openFileWight()
            self.lineEdit_target.setText(str(filePath))
            Database.coorTranTargetData = self._getSparateData(dataList)
            # 发送信号
            self.fileReadEmit.emit(1,None)
        except Exception as e:
            self.infoEmit.emit("I", "取消或文件为空,其它信息：" + e.args.__str__())

    def _sendInfo(self, type, strInfo):
        self.infoEmit.emit(type, strInfo)

    def _openFileWight(self):
        filePath, ok = QtWidgets.QFileDialog.getOpenFileName(self.parentWidget, "打开", "./source/",
                                                             "All Files (*);;Text Files (*.txt)")
        dataList = OperationFile().readlargeFile(filePath)
        return filePath, dataList

    def _getSparateData(self, originFileData):
        """
        文件数据的划分
        <p>将行数据进一步细化
        :param originFileData: 以读入的数据行为单位的一位数列List
        :return: twoDissList
        """
        dataList = []
        sparateMethod = None
        if self.radioButton_commaSymbal.isChecked() == True:  # 这一句实际上没必要，后期删掉，因为界面初始化就设定了
            sparateMethod = ","
        elif self.radioButton_blank.isChecked() == True:
            sparateMethod = " "
        else:
            sparateMethod = self.lineEdit_otherSparate.text().strip()
        for i in range(len(originFileData)):
            dataList.append(originFileData[i].split(sparateMethod))
        return dataList
