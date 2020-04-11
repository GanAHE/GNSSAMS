# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coorTranWight.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from database.database import Database
from window.action import actionCoorTran


class Ui_Form(QtCore.QObject):
    infoEmit = QtCore.pyqtSignal(str, str)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1197, 771)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5)
        self.radioButton_DirectPara_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_DirectPara_2.setObjectName("radioButton_DirectPara_2")
        self.radioButton_DirectPara_2.setChecked(True)
        self.verticalLayout_7.addWidget(self.radioButton_DirectPara_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.radioButton_LeastSquare_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_LeastSquare_2.setObjectName("radioButton_LeastSquare_2")
        self.horizontalLayout_5.addWidget(self.radioButton_LeastSquare_2)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.spinBox_leastSquares = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_leastSquares.setReadOnly(False)
        self.spinBox_leastSquares.setMinimum(3)
        self.spinBox_leastSquares.setMaximum(10000)
        self.spinBox_leastSquares.setProperty("value", 4)
        self.spinBox_leastSquares.setObjectName("spinBox_leastSquares")
        self.horizontalLayout_5.addWidget(self.spinBox_leastSquares)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.radioButton_LeastSquare_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_LeastSquare_3.setObjectName("radioButton_LeastSquare_3")
        self.horizontalLayout_6.addWidget(self.radioButton_LeastSquare_3)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.spinBox_conformalTransFormat = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_conformalTransFormat.setReadOnly(False)
        self.spinBox_conformalTransFormat.setMinimum(6)
        self.spinBox_conformalTransFormat.setMaximum(10000)
        self.spinBox_conformalTransFormat.setProperty("value", 6)
        self.spinBox_conformalTransFormat.setObjectName("spinBox_conformalTransFormat")
        self.horizontalLayout_6.addWidget(self.spinBox_conformalTransFormat)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout_7)
        self.button_twoCoorTran = QtWidgets.QPushButton(self.groupBox)
        self.button_twoCoorTran.setObjectName("button_twoCoorTran")
        self.verticalLayout_2.addWidget(self.button_twoCoorTran)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.spinBox_threeDiss = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_threeDiss.setReadOnly(False)
        self.spinBox_threeDiss.setMinimum(3)
        self.spinBox_threeDiss.setMaximum(10000)
        self.spinBox_threeDiss.setProperty("value", 4)
        self.spinBox_threeDiss.setObjectName("spinBox_threeDiss")
        self.horizontalLayout.addWidget(self.spinBox_threeDiss)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.radioButton_sixPara = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_sixPara.setObjectName("radioButton_sixPara")
        self.radioButton_sixPara.setChecked(True)
        self.verticalLayout_3.addWidget(self.radioButton_sixPara)
        self.radioButton_sevenPara = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_sevenPara.setObjectName("radioButton_sevenPara")
        self.verticalLayout_3.addWidget(self.radioButton_sevenPara)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.button_threeCoorTran = QtWidgets.QPushButton(self.groupBox_2)
        self.button_threeCoorTran.setObjectName("button_threeCoorTran")
        self.verticalLayout_4.addWidget(self.button_threeCoorTran)
        self.verticalLayout_5.addWidget(self.groupBox_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.button_clearSourceData = QtWidgets.QPushButton(Form)
        self.button_clearSourceData.setObjectName("button_clearSourceData")
        self.horizontalLayout_4.addWidget(self.button_clearSourceData)
        self.button_clearResult = QtWidgets.QPushButton(Form)
        self.button_clearResult.setObjectName("button_clearResult")
        self.horizontalLayout_4.addWidget(self.button_clearResult)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.button_reset = QtWidgets.QPushButton(Form)
        self.button_reset.setObjectName("button_reset")
        self.verticalLayout_5.addWidget(self.button_reset)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setMouseTracking(False)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./source/icon/icon_科学.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableView_source = QtWidgets.QTableView(self.groupBox_3)
        self.tableView_source.setObjectName("tableView_source")
        self.horizontalLayout_3.addWidget(self.tableView_source)
        self.verticalLayout_6.addWidget(self.groupBox_3)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.tableView_result = QtWidgets.QTableView(Form)
        self.tableView_result.setObjectName("tableView_result")
        self.verticalLayout.addWidget(self.tableView_result)
        self.horizontalLayout_7.addLayout(self.verticalLayout)

        self.retranslateUi(Form)

        self.actionTwoTranThread = actionCoorTran.ActionCoorTran()
        self.actionTwoTranThread.infoEmit.connect(self.sendInfo)
        self.actionTwoTranThread.finishEmit.connect(self.finishTwoCoorTranThread)
        self.button_twoCoorTran.clicked.connect(self.startTwoCoorTran)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "二维"))
        self.label_5.setText(_translate("Form", "转换方法："))
        self.radioButton_DirectPara_2.setText(_translate("Form", "直接参数法"))
        self.radioButton_LeastSquare_2.setText(_translate("Form", "最小二乘法"))
        self.label_6.setText(_translate("Form", "公共点个数："))
        self.radioButton_LeastSquare_3.setText(_translate("Form", "正形变换法"))
        self.label_7.setText(_translate("Form", "公共点个数："))
        self.button_twoCoorTran.setText(_translate("Form", "转换"))
        self.groupBox_2.setTitle(_translate("Form", "三维"))
        self.label_8.setText(_translate("Form", "公共点个数："))
        self.label_4.setText(_translate("Form", "转换方法："))
        self.radioButton_sixPara.setText(_translate("Form", "六参数坐标转换"))
        self.radioButton_sevenPara.setText(_translate("Form", "七参数坐标转换"))
        self.button_threeCoorTran.setText(_translate("Form", "转换"))
        self.button_clearSourceData.setText(_translate("Form", "清空初始数据"))
        self.button_clearResult.setText(_translate("Form", "清空结果数据"))
        self.button_reset.setText(_translate("Form", "重置"))
        self.groupBox_3.setTitle(_translate("Form", "原始坐标数据"))
        self.label_3.setText(_translate("Form", "转换坐标数据"))

    def startTwoCoorTran(self):

        # 先设定计算的方法
        if self.radioButton_DirectPara_2.isChecked():
            self.actionTwoTranThread.thisTypeEmit.emit("D", 0)

        elif self.radioButton_LeastSquare_2.isChecked():
            self.actionTwoTranThread.thisTypeEmit.emit("L", int(self.spinBox_leastSquares.text().strip()))

        else:
            self.actionTwoTranThread.thisTypeEmit.emit("Z", int(self.spinBox_conformalTransFormat.text().strip()))

        self.actionTwoTranThread.start()

    def sendInfo(self, type, strInfo):
        self.infoEmit.emit(type, strInfo)

    def finishTwoCoorTranThread(self):
        # 保留位数
        # 读取数据
        paraData = Database.coorTranResultDict.get("para")
        if paraData[0][0] == 0:  # 仅能作用最小二乘
            self.sendInfo("E", "错误！最小二乘迭代次数超限:" + str(paraData[1][0]))
        else:
            paraStr = []
            for i in range(len(paraData)):
                paraStr.append(str(round(paraData[i][0], 4)))

            resultData = Database.coorTranResultDict.get("result")
            sourceFileStrData = Database.coorTranSourceData
            targetFileStrData = Database.coorTranTargetData
            resultStr = []
            publicPointCount = paraData[0][0]  # 直接参数反正达不到，但是当点大于转换的直接参数第一个点坐标时就会无法显示结果
            for i in range(len(resultData)):
                if i >= publicPointCount and len(paraData) != 4:  # 解决上面 bug
                    resultStr.append(
                        [sourceFileStrData[i][0], str(round(resultData[i][0], 4)), str(round(resultData[i][1])), "None",
                         "None"])
                else:
                    teta_Xx = str(round(abs(resultData[i][0] - float(targetFileStrData[i][1])), 4))
                    teta_Yy = str(round(abs(resultData[i][1] - float(targetFileStrData[i][2])), 4))
                    resultStr.append(
                        [sourceFileStrData[i][0], str(round(resultData[i][0], 4)), str(round(resultData[i][1], 4)),
                         teta_Xx,
                         teta_Yy])
            Database.coorTranResultFormatListData = resultStr

            if self.radioButton_DirectPara_2.isChecked():
                self.setTableData(1, ["偏移量 Dx/m", "偏移量 Dy/m", "尺度因子 M/m", "旋转角度 THETA/°"], [paraStr])
                self.setTableData(2, ["点名", "X /m", "Y /m", "坐标残差TETA_X/m", "坐标残差TETA_Y/m"], resultStr)
            elif self.radioButton_LeastSquare_2.isChecked():
                self.setTableData(1, ["公共点数", "迭代次数", "偏移量 Dx", "偏移量 Dy", "旋转角度THETA/°", "尺度因子 M/m", "中误差 SIGMA/mm"],
                                  [paraStr])
                self.setTableData(2, ["点名", "X /m", "Y /m", "坐标残差TETA_X/m", "坐标残差TETA_Y/m"], resultStr)
            else:
                tableHead = ["转换参数" + str(i) for i in range(1, 11)]
                tableHead.insert(0, "公共点数")
                self.setTableData(1, tableHead, [paraStr])
                self.setTableData(2, ["点名", "X /m", "Y /m", "坐标残差TETA_X/m", "坐标残差TETA_Y/m"], resultStr)

        # 关闭线程
        self.actionTwoTranThread.killThread()

    def setTableData(self, tableType, tableHeadStrList, dataList):
        """
        设定表格内容项
        :param tableType: 1加入参数表，其他加入结果表
        :param tableHeadStrList: 一维 List
        :param dataList: 二维 List
        :return: None
        """
        model = self._tableRowModel(tableHeadStrList, dataList)
        if tableType == 1:
            self.tableView_source.setModel(model)
        else:
            self.tableView_result.setModel(model)

    def _tableRowModel(self, tableHeader, itemStrList):
        model = QtGui.QStandardItemModel(len(itemStrList), len(itemStrList[0]))

        model.setHorizontalHeaderLabels(tableHeader)
        for i in range(len(itemStrList)):
            for k in range(len(itemStrList[0])):
                model.setVerticalHeaderItem(i, QtGui.QStandardItem(str(i + 1)))
                model.setItem(i, k, QtGui.QStandardItem(itemStrList[i][k]))
                # 居中，参考电子手簿功能的QTableWight
                model.item(i, k).setTextAlignment(QtCore.Qt.AlignCenter)
        return model
