# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SPPWight.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from database.database import Database
from window.GNSS import actionSPP


class Ui_Form(QtCore.QObject):
    infoEmit = QtCore.pyqtSignal(str, str)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1114, 715)
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./../source/icon/dingweixian.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setMaximumSize(QtCore.QSize(350, 400))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_elliPara = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_elliPara.setObjectName("comboBox_elliPara")
        self.comboBox_elliPara.addItem("")
        self.comboBox_elliPara.addItem("")
        self.comboBox_elliPara.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_elliPara)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBox_satelliteCount = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBox_satelliteCount.setMinimum(5)
        self.spinBox_satelliteCount.setMaximum(50)
        self.spinBox_satelliteCount.setObjectName("spinBox_satelliteCount")
        self.horizontalLayout_2.addWidget(self.spinBox_satelliteCount)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_3)
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_SPP = QtWidgets.QWidget()
        self.tab_SPP.setObjectName("tab_SPP")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_SPP)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.button_SPP = QtWidgets.QPushButton(self.tab_SPP)
        self.button_SPP.setObjectName("button_SPP")
        self.horizontalLayout_4.addWidget(self.button_SPP)
        self.button_mapLacation = QtWidgets.QPushButton(self.tab_SPP)
        self.button_mapLacation.setObjectName("button_mapLacation")
        self.horizontalLayout_4.addWidget(self.button_mapLacation)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_SPP)
        self.pushButton_3.setText("")
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setChecked(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_5.addWidget(self.pushButton_3)
        self.status_slider = QtWidgets.QSlider(self.tab_SPP)
        self.status_slider.setAutoFillBackground(True)
        self.status_slider.setStyleSheet("color: rgb(170, 255, 255);")
        self.status_slider.setMaximum(1)
        self.status_slider.setTracking(True)
        self.status_slider.setOrientation(QtCore.Qt.Horizontal)
        self.status_slider.setInvertedAppearance(False)
        self.status_slider.setInvertedControls(False)
        self.status_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.status_slider.setTickInterval(0)
        self.status_slider.setObjectName("status_slider")
        self.horizontalLayout_5.addWidget(self.status_slider)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_SPP)
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_5.addWidget(self.pushButton_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./source/icon/icon_educa.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_SPP, icon1, "")
        self.tab_PPP = QtWidgets.QWidget()
        self.tab_PPP.setObjectName("tab_PPP")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./source/icon/QTUM.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_PPP, icon2, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("./source/icon/decentralized-02.png"))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.horizontalLayout_6.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_6.addWidget(self.groupBox)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.button_SPP.clicked.connect(self.actionButtonSPP)
        self.actionGetStationPosition = actionSPP.ActionSPP()
        self.actionGetStationPosition.infoEmit.connect(self.sendTopInfo)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_3.setTitle(_translate("Form", "操作区"))
        self.label.setText(_translate("Form", "参考椭球："))
        self.comboBox_elliPara.setItemText(0, _translate("Form", "WGS84"))
        self.comboBox_elliPara.setItemText(1, _translate("Form", "CGCS2000"))
        self.comboBox_elliPara.setItemText(2, _translate("Form", "克拉斯夫椭球"))
        self.label_2.setText(_translate("Form", "计算卫星数："))
        self.button_SPP.setText(_translate("Form", "标准单点定位"))
        self.button_mapLacation.setText(_translate("Form", "查看地图点位"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_SPP), _translate("Form", "SPP"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_PPP), _translate("Form", "PPP"))
        self.groupBox.setTitle(_translate("Form", "数据"))

    def setFileInfo(self):
        fileList = Database.oFilePathList
        self.tableWidget.setRowCount(len(fileList))
        self.tableWidget.setColumnCount(4)
        headList = ["测站", "年积日", "文件序号", "观测时间"]
        for i in range(len(headList)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(headList[i])
        # self.tableWidget.setHorizontalHeaderItem(2)
        # 构建表格数据模型
        for i in range(len(fileList)):
            dir, fileName = os.path.split(fileList[i])
            for k in range(self.tableWidget.columnCount()):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, k, item)
                if k == 0:
                    self.tableWidget.item(i, k).setText(fileName[:4])
                elif k == 1:
                    self.tableWidget.item(i, k).setText(fileName[4:7])
                elif k == 2:
                    self.tableWidget.item(i, k).setText(fileName[7])
                else:
                    self.tableWidget.item(i, k).setText("20" + fileName[9:11])

                print("检测是否进入数据表设定")

    def actionButtonSPP(self):
        self.sendTopInfo("I", "\n==单点定位：")
        ellipsoid = self.comboBox_elliPara.currentText()
        # 将界面显示选择的椭球转为内部标准查询参数，其他参数符合的不需要转换
        if ellipsoid == "1975国际椭球":
            ellipsoid = "IE1975"
        elif ellipsoid == "格拉索夫斯基椭球":
            ellipsoid = "Krasovski"

        reCode = self.actionGetStationPosition.actionReadFile(ellipsoid)
        if reCode:
            self.sendTopInfo("T", "完成单点定位解算！")
            self.status_slider.setValue(1)
            self.pushButton_3.setChecked(False)
            self.pushButton_4.setCheckable(True)
            self.pushButton_4.setChecked(True)

    def sendTopInfo(self, type, strInfo):
        if len(type) > 1:
            # 分开序号与信息
            [id, title] = type.split("-")
            id = int(id)
            # 检查列名是否存在:不存在，新建一个列名，如果已经存在，则需要加行写入数据
            columnCount = self.tableWidget.columnCount()
            rowCount = self.tableWidget.rowCount()
            exitCode = False
            for i in range(columnCount):
                if title == self.tableWidget.horizontalHeaderItem(i).text():
                    exitCode = True
                    # 存在，按照行号检查,大于现有行宽度则新增一行
                    if id >= rowCount:
                        self.tableWidget.setRowCount(rowCount + 1)
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(id, i, item)
                    self.tableWidget.item(id, i).setText(strInfo)
                    break
            if exitCode is False:
                self.tableWidget.setColumnCount(columnCount + 1)
                columnCount = self.tableWidget.columnCount()
                # 新增一列,设置列名
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(columnCount - 1, item)
                item.setText(title)
                # 按照行号检查,大于现有行宽度则新增一行
                if id >= rowCount:
                    self.tableWidget.setRowCount(rowCount + 1)
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(id, columnCount - 1, item)
                self.tableWidget.item(id, columnCount - 1).setText(strInfo)

        else:
            self.infoEmit.emit(type, strInfo)

    def initTableWight(self):
        pass
