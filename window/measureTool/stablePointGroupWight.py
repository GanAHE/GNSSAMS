# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stablePointGroupWight.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from database.database import Database
from window.controlNetwork.actionStableDotGroup import ActionStablePointGroup


class Ui_Form(QtCore.QObject):
    infoEmit = QtCore.pyqtSignal(str, str)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1130, 809)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.spinBox_lineThreshold = QtWidgets.QDoubleSpinBox(Form)
        self.spinBox_lineThreshold.setProperty("value", 20.0)
        self.spinBox_lineThreshold.setObjectName("spinBox_lineThreshold")
        self.horizontalLayout_6.addWidget(self.spinBox_lineThreshold)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.spinbox_sourcePara = QtWidgets.QDoubleSpinBox(Form)
        self.spinbox_sourcePara.setProperty("value", 0.26)
        self.spinbox_sourcePara.setObjectName("spinbox_sourcePara")
        self.horizontalLayout_3.addWidget(self.spinbox_sourcePara)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.spinBox_step = QtWidgets.QDoubleSpinBox(Form)
        self.spinBox_step.setSingleStep(0.25)
        self.spinBox_step.setProperty("value", 0.25)
        self.spinBox_step.setObjectName("spinBox_step")
        self.horizontalLayout_4.addWidget(self.spinBox_step)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.spinBox_up = QtWidgets.QDoubleSpinBox(Form)
        self.spinBox_up.setProperty("value", 10.0)
        self.spinBox_up.setObjectName("spinBox_up")
        self.horizontalLayout_2.addWidget(self.spinBox_up)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./source/icon/Excavator.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.button_cacu = QtWidgets.QPushButton(Form)
        self.button_cacu.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./source/icon/QTUM.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_cacu.setIcon(icon)
        self.button_cacu.setIconSize(QtCore.QSize(40, 40))
        self.button_cacu.setCheckable(False)
        self.button_cacu.setAutoRepeat(True)
        self.button_cacu.setAutoExclusive(False)
        self.button_cacu.setAutoRepeatInterval(100)
        self.button_cacu.setAutoDefault(False)
        self.button_cacu.setDefault(True)
        self.button_cacu.setFlat(False)
        self.button_cacu.setObjectName("button_cacu")
        self.horizontalLayout.addWidget(self.button_cacu)
        self.button_clear = QtWidgets.QPushButton(Form)
        self.button_clear.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./source/icon/icon_rb.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_clear.setIcon(icon1)
        self.button_clear.setIconSize(QtCore.QSize(40, 40))
        self.button_clear.setDefault(True)
        self.button_clear.setObjectName("button_clear")
        self.horizontalLayout.addWidget(self.button_clear)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./source/icon/Dumptruck_1.png"))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_8.addLayout(self.verticalLayout_2)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_3.addWidget(self.textEdit)
        self.horizontalLayout_8.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        # 初始化线程
        self.actionStablePointGroup = ActionStablePointGroup()
        # 绑定信号
        self.actionStablePointGroup.paraEmit.connect(self.actionStablePointGroup.setPara)
        self.actionStablePointGroup.overEmit.connect(self.killStableDotCucaThread)
        self.actionStablePointGroup.infoEmit.connect(self.infoStream)

        self.button_cacu.clicked.connect(self.stablePointGroupAnalysis)
        self.button_clear.clicked.connect(self.textEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "原始数据"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ID(第一期)"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "X1"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Y1"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Z1"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "ID(第二期)"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "X2"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Y2"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Z2"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Form", "残差teta_X"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Form", "残差teta_Y"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("Form", "残差teta_Z"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("Form", "其他"))
        self.label_7.setText(_translate("Form", "共线阈值(以坐标的单位为基准)："))
        self.label_3.setText(_translate("Form", "比例系数f调整"))
        self.label_6.setText(_translate("Form", "初始参数："))
        self.label_4.setText(_translate("Form", "自动纠正步长："))
        self.label_5.setText(_translate("Form", "纠正上限："))
        self.button_cacu.setShortcut(_translate("Form", "Del"))
        self.groupBox_2.setTitle(_translate("Form", "解算结果"))
        self.textEdit.setHtml(_translate("Form",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

    def stablePointGroupAnalysis(self):
        # 比例系数初始值
        f = float(self.spinbox_sourcePara.text())
        # 比例系数步长
        step = float(self.spinBox_step.text())
        # 比例系数自动调整上限
        upValue = float(self.spinBox_up.text())
        # 共线判定阈值
        inLine = float(self.spinBox_lineThreshold.text())
        # 发射信号设定参数
        self.actionStablePointGroup.paraEmit.emit(f, step, upValue, inLine)
        # 开启线程
        self.actionStablePointGroup.start()
        self._sendTopInfo("I", "开启线程，开始稳定点组解算....")
        # TODO：进度条

    def killStableDotCucaThread(self):
        self.actionStablePointGroup.killThread()
        # 线程关闭
        self._sendTopInfo("I", "关闭线程")

    def setTableData(self):
        try:
            self._sendTopInfo("I", "设定表格数据")
            # 获取数据
            measure_I = Database.stableDotGroupMeasure_I
            measure_II = Database.stableDotGroupMeasure_II
            if len(measure_I) != len(measure_II):
                print("两期观测数据个数不相等，错误！")
            else:
                # 将数据整合
                for i in range(len(measure_I)):
                    measure_I[i] = measure_I[i] + measure_II[i]
                # 批量定制填充表格
                # print(measure_I[0],len(measure_I))
                # 按照数据量扩展表格行数
                self.tableWidget.setRowCount(len(measure_I))

                for i in range(len(measure_I)):
                    for k in range(11):
                        item = QtWidgets.QTableWidgetItem()
                        self.tableWidget.setItem(i, k, item)
                        self.tableWidget.item(i, k).setTextAlignment(QtCore.Qt.AlignCenter)
                        if k < 8:
                            self.tableWidget.item(i, k).setText(measure_I[i][k])
                        else:
                            self.tableWidget.item(i, k).setText(str(round(
                                float(self.tableWidget.item(i, k - 7).text()) - float(
                                    self.tableWidget.item(i, k - 3).text()), 4)))
        except Exception as e:
            self._sendTopInfo("W", e.__str__())

    def infoStream(self, type, emitStrInfo):
        if type == "T":
            self._setTextEdit(emitStrInfo)
        else:
            # 发送到顶级界面信息
            self._sendTopInfo(type, emitStrInfo)

    def _setTextEdit(self, str):
        self.textEdit.append(str)

    def _sendTopInfo(self, type, emitStrInfo):
        """
        外发信号到顶级界面
        :param type: 除去T
        :param emitStrInfo:
        :return:
        """
        self.infoEmit.emit(type, emitStrInfo)

    def getTextEdit(self):
        text = self.textEdit.toPlainText()
        return text
