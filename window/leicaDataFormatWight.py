# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'leicaDataFormat.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from database.database import Database


class Ui_Form(QtCore.QObject):
    showTableEmit = QtCore.pyqtSignal()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1147, 715)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setMaximumSize(QtCore.QSize(350, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap("./source/icon/ethereum-mining.png"))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_7.addWidget(self.label_10)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_mesureFrom = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_mesureFrom.setObjectName("lineEdit_mesureFrom")
        self.horizontalLayout.addWidget(self.lineEdit_mesureFrom)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_mesureTarget = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_mesureTarget.setObjectName("lineEdit_mesureTarget")
        self.horizontalLayout.addWidget(self.lineEdit_mesureTarget)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setMaximumSize(QtCore.QSize(85, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.dateEdit_from = QtWidgets.QDateEdit(self.groupBox_2)
        self.dateEdit_from.setObjectName("dateEdit_from")
        self.horizontalLayout_2.addWidget(self.dateEdit_from)
        self.timeEdit_from = QtWidgets.QTimeEdit(self.groupBox_2)
        self.timeEdit_from.setObjectName("timeEdit_from")
        self.horizontalLayout_2.addWidget(self.timeEdit_from)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.dateEdit_target = QtWidgets.QDateEdit(self.groupBox_2)
        self.dateEdit_target.setObjectName("dateEdit_target")
        self.horizontalLayout_3.addWidget(self.dateEdit_target)
        self.timeEdit_target = QtWidgets.QTimeEdit(self.groupBox_2)
        self.timeEdit_target.setObjectName("timeEdit_target")
        self.horizontalLayout_3.addWidget(self.timeEdit_target)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.lineEdit_temperature = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_temperature.setStyleSheet("")
        self.lineEdit_temperature.setInputMask("")
        self.lineEdit_temperature.setText("")
        self.lineEdit_temperature.setPlaceholderText("")
        self.lineEdit_temperature.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.lineEdit_temperature.setClearButtonEnabled(False)
        self.lineEdit_temperature.setObjectName("lineEdit_temperature")
        self.horizontalLayout_5.addWidget(self.lineEdit_temperature)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.lineEdit_cloud = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_cloud.setText("")
        self.lineEdit_cloud.setObjectName("lineEdit_cloud")
        self.horizontalLayout_6.addWidget(self.lineEdit_cloud)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_11.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.lineEdit_wind = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_wind.setText("")
        self.lineEdit_wind.setObjectName("lineEdit_wind")
        self.horizontalLayout_9.addWidget(self.lineEdit_wind)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_10.addWidget(self.label_9)
        self.lineEdit_sun = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_sun.setText("")
        self.lineEdit_sun.setObjectName("lineEdit_sun")
        self.horizontalLayout_10.addWidget(self.lineEdit_sun)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_11)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.lineEdit_soil = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_soil.setText("")
        self.lineEdit_soil.setObjectName("lineEdit_soil")
        self.horizontalLayout_7.addWidget(self.lineEdit_soil)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.lineEdit_weather = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_weather.setText("")
        self.lineEdit_weather.setObjectName("lineEdit_weather")
        self.horizontalLayout_8.addWidget(self.lineEdit_weather)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_7.addLayout(self.verticalLayout_5)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)
        self.horizontalLayout_12.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
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
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)

        # 表格表头设定
        self.tableHeadFormat()
        self.verticalLayout_6.addWidget(self.tableWidget)
        self.horizontalLayout_12.addWidget(self.groupBox_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.showTableEmit.connect(self.dataFillFormat)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_2.setTitle(_translate("Form", "测段基本信息"))
        self.label.setText(_translate("Form", "测段由"))
        self.label_2.setText(_translate("Form", "至"))
        self.label_3.setText(_translate("Form", "时间（段）："))
        self.dateEdit_from.setDisplayFormat(_translate("Form", "yyyy-MM-dd"))
        self.timeEdit_from.setDisplayFormat(_translate("Form", "HH:mm"))
        self.dateEdit_target.setDisplayFormat(_translate("Form", "yyyy-MM-dd"))
        self.timeEdit_target.setDisplayFormat(_translate("Form", "HH:mm"))
        self.label_4.setText(_translate("Form", "温度："))
        self.label_5.setText(_translate("Form", "云量："))
        self.label_8.setText(_translate("Form", "风向风速："))
        self.label_9.setText(_translate("Form", "太阳方向："))
        self.label_7.setText(_translate("Form", "测区土质："))
        self.label_6.setText(_translate("Form", "气节及天气："))
        self.groupBox_3.setTitle(_translate("Form", "观测数据"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Form", "４"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Form", "５"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("Form", "６"))
        for i in range(8):
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("Form", "GanAH-" + chr(65 + i)))
        # __sortingEnabled = self.tableWidget.isSortingEnabled()
        # self.tableWidget.setSortingEnabled(False)
        # item = self.tableWidget.item(0, 0)
        # item.setText(_translate("Form", "测站编号"))
        # item = self.tableWidget.item(0, 1)
        # item.setText(_translate("Form", "视距差d"))
        # item = self.tableWidget.item(0, 4)
        # item.setText(_translate("Form", "基本分划"))
        # self.tableWidget.setSortingEnabled(__sortingEnabled)

    def tableHeadFormat(self):
        """
        组装表格表头
        <p>避免修改界面后消失
        :return: None
        """
        # 测站编号
        self.tableWidget.setSpan(0, 0, 4, 1)
        self.tableWidget.item(0, 0).setText("测站编号")
        self.tableWidget.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        # 后视
        self.label_back = QtWidgets.QLabel(self.groupBox_3)
        self.label_back.setText("")
        self.label_back.setPixmap(QtGui.QPixmap("./source/icon/table_back.png"))
        self.label_back.setAlignment(QtCore.Qt.AlignCenter)
        self.label_back.setObjectName("label_back")
        self.tableWidget.setSpan(0, 1, 4, 1)
        self.tableWidget.setCellWidget(0, 1, self.label_back)
        self.tableWidget.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)

        # 前视
        self.label_forwark = QtWidgets.QLabel(self.groupBox_3)
        self.label_forwark.setText("")
        self.label_forwark.setPixmap(QtGui.QPixmap("./source/icon/table_forwark.png"))
        self.label_forwark.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forwark.setObjectName("label_forwark")
        self.tableWidget.setSpan(0, 2, 4, 1)
        self.tableWidget.setCellWidget(0, 2, self.label_forwark)
        self.tableWidget.item(0, 2).setTextAlignment(QtCore.Qt.AlignCenter)

        # 标尺方向
        self.tableWidget.setSpan(0, 3, 4, 1)
        self.tableWidget.item(0, 3).setText("方向及尺号")
        self.tableWidget.item(0, 3).setTextAlignment(QtCore.Qt.AlignCenter)

        # 标尺读数
        self.tableWidget.setSpan(0, 4, 2, 2)
        self.tableWidget.item(0, 4).setText("标 尺 读 数")
        self.tableWidget.item(0, 4).setTextAlignment(QtCore.Qt.AlignCenter)

        # 标尺读数
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 5, item)

        self.tableWidget.item(2, 4).setText("基本分划")
        self.tableWidget.setSpan(2, 4, 2, 1)
        self.tableWidget.item(2, 4).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.item(2, 5).setText("辅助分划")
        self.tableWidget.setSpan(2, 5, 2, 1)
        self.tableWidget.item(2, 5).setTextAlignment(QtCore.Qt.AlignCenter)

        # 基辅算

        self.tableWidget.setSpan(0, 6, 3, 1)
        self.tableWidget.item(0, 6).setText("基+K-辅")
        self.tableWidget.item(0, 6).setTextAlignment(QtCore.Qt.AlignCenter)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 6, item)
        self.tableWidget.item(3, 6).setText("Σs")
        self.tableWidget.item(3, 6).setTextAlignment(QtCore.Qt.AlignCenter)

        # 备注
        self.tableWidget.setSpan(0, 7, 4, 1)
        self.tableWidget.item(0, 7).setText("备  注")
        self.tableWidget.item(0, 7).setTextAlignment(QtCore.Qt.AlignCenter)

    def dataFillFormat(self):
        """
        数据填充到表格
        <p> 数据为电子式
        :param strStationNumber: 一维 list
        :param strData:  二维 strData
        :return:
        """

        # 从数据库获取数据
        dictAnalysis = Database.leicaAnalysisDict
        strStationID_height = dictAnalysis.get("ID")
        strMersure = dictAnalysis.get("data")

        try:
            # 初始化表格，加上基础表头4行
            tableLength = len(strMersure) + 4

            # 追加表格范围
            self.tableWidget.setRowCount(tableLength)
            """
            # 批量定制单元格并填充
            # arithmeticProgressionCount 为定位所需的等差数列的序数！
            # 第一个为 i = 5 - 9 - 13;第二个为 i = 6 - 10 - 14...
            # 这是一个奇妙的处理思想，但是可能以后我自己的看不懂了
            """
            arithmeticProgressionCount = 2
            arithmeticProgressionCount_three = 1
            arithmeticProgressionCount_remark = 1
            for i in range(4, tableLength):
                if i % 4 == 0:  # 组一
                    item = QtWidgets.QTableWidgetItem()
                    # 编号
                    self.tableWidget.setItem(i, 0, item)
                    self.tableWidget.setSpan(i, 0, 4, 1)
                    self.tableWidget.item(i, 0).setText(strMersure[i - 4][0] + "-->" + strMersure[i - 3][0])
                    self.tableWidget.item(i, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    # 备注
                    self.tableWidget.setItem(i, 7, item)
                    self.tableWidget.setSpan(i, 7, 4, 1)

                    for k in range(1, 7):
                        item = QtWidgets.QTableWidgetItem()
                        self.tableWidget.setItem(i, k, item)

                        if k < 3:
                            self.tableWidget.item(i, k).setText((strMersure[i + k - 5][1])[2:])
                        elif k == 3:  # 尺方向
                            self.tableWidget.item(i, k).setText("后")
                        elif k == 4:
                            self.tableWidget.item(i, k).setText(strMersure[i - 4][2])
                        elif k == 5:
                            self.tableWidget.item(i, k).setText(strMersure[i - 1][2])
                        else:
                            self.tableWidget.item(i, k).setText(
                                str(int(
                                    float(self.tableWidget.item(i, k - 2).text())
                                    - float(self.tableWidget.item(i, k - 1).text())
                                )))

                        self.tableWidget.item(i, k).setTextAlignment(QtCore.Qt.AlignCenter)

                elif i == 4 * arithmeticProgressionCount - 3:  # 等差数列，奇数区域不能直接用整除来定位，组二
                    arithmeticProgressionCount += 1
                    for k in range(1, 7):
                        item = QtWidgets.QTableWidgetItem()
                        self.tableWidget.setItem(i, k, item)
                        if k == 1:
                            self.tableWidget.item(i, k).setText((strMersure[i - 2][1])[2:])
                        elif k == 2:
                            self.tableWidget.item(i, k).setText((strMersure[i - 3][1])[2:])
                        elif k == 3:
                            self.tableWidget.item(i, k).setText("前")
                        elif k == 4:
                            self.tableWidget.item(i, k).setText(strMersure[i - 3][2])
                        elif k == 5:
                            self.tableWidget.item(i, k).setText(strMersure[i - 4][2])
                        else:
                            self.tableWidget.item(i, k).setText(
                                str(
                                    int(
                                        float(self.tableWidget.item(i, k - 2).text()) -
                                        float(self.tableWidget.item(i, k - 1).text())
                                    )
                                ))

                        self.tableWidget.item(i, k).setTextAlignment(QtCore.Qt.AlignCenter)

                elif i == 4 * arithmeticProgressionCount_three + 2:  # 组三
                    arithmeticProgressionCount_three += 1
                    for k in range(1, 7):
                        item = QtWidgets.QTableWidgetItem()
                        self.tableWidget.setItem(i, k, item)
                        if k < 3:
                            self.tableWidget.item(i, k).setText(str(
                                round(
                                    (float(self.tableWidget.item(i - 1, k).text()) +
                                     float(self.tableWidget.item(i - 2, k).text())) / 2, 4)))
                        elif k == 3:
                            self.tableWidget.item(i, k).setText("后 - 前")
                        elif k > 3 and k < 6:
                            self.tableWidget.item(i, k).setText(str(
                                round((
                                        float(self.tableWidget.item(i - 2, k).text()) - float(
                                    self.tableWidget.item(i - 1, k).text())), 4)
                            ))

                        elif k == 6:
                            self.tableWidget.item(i, k).setText(
                                str(int(
                                    float(self.tableWidget.item(i, k - 2).text())
                                    - float(self.tableWidget.item(i, k - 1).text())
                                )))

                        self.tableWidget.item(i, k).setTextAlignment(QtCore.Qt.AlignCenter)

                else:  # 组四
                    for k in range(1, 8):
                        item = QtWidgets.QTableWidgetItem()
                        self.tableWidget.setItem(i, k, item)
                        if k == 1:
                            self.tableWidget.item(i, k).setText(str(
                                (round((float(self.tableWidget.item(i - 1, k).text()) -
                                        float(self.tableWidget.item(i - 1, k + 1).text())) / 1000, 2))))
                        elif k == 2:  # 累积视距差
                            if i == 7:
                                self.tableWidget.item(i, k).setText(self.tableWidget.item(i, k - 1).text())
                            else:
                                self.tableWidget.item(i, k).setText(str(
                                    (round((float(self.tableWidget.item(i - 4, k).text()) + float(
                                        self.tableWidget.item(i, k - 1).text())), 2))))
                        elif k == 3:  # 标示
                            self.tableWidget.item(i, k).setText("h | Σh")
                        elif k == 4:  # 观测尺高差
                            self.tableWidget.item(i, k).setText(str(
                                round(
                                    (float(self.tableWidget.item(i - 1, k + 1).text()) +
                                     float(self.tableWidget.item(i - 1, k).text())) / 2000, 5)))
                        elif k == 5:  # 测段尺高累积差
                            if i == 7:
                                self.tableWidget.item(i, k).setText(self.tableWidget.item(i, k - 1).text())
                            else:
                                self.tableWidget.item(i, k).setText(str(
                                    round(
                                        float(self.tableWidget.item(i - 4, k).text()) +
                                        float(self.tableWidget.item(i, k - 1).text()), 4)
                                ))

                        elif k == 6:  # 测段累积视距
                            if i == 7:
                                self.tableWidget.item(i, k).setText(str(
                                    round((float(self.tableWidget.item(i - 1, k - 4).text()) +
                                           float(self.tableWidget.item(i - 1, k - 4).text())) / 100, 4)
                                ))
                            else:
                                self.tableWidget.item(i, k).setText(str(
                                    round(
                                        (float(self.tableWidget.item(i - 4, k).text()) +
                                         (float(self.tableWidget.item(i - 1, k - 4).text()) +
                                          float(self.tableWidget.item(i - 1, k - 4).text())) / 100), 4)
                                ))
                        else:
                            # 备注测段信息等，由于滞后性（填写该处需要下三行的数据，以上逐行写入而不行），放在这里进行
                            index = i - 3
                            if index % 4 == 0:
                                item = QtWidgets.QTableWidgetItem()
                                self.tableWidget.setItem(index, k, item)
                                if i == 8 * arithmeticProgressionCount_remark + 3:
                                    self.tableWidget.item(index, k).setText(
                                        "  [测段 " + str(arithmeticProgressionCount_remark) + " 信息]\n" +
                                        "1.测段累积视距差：" + self.tableWidget.item(i, k - 5).text() + "m\n" +
                                        "2.测段高差：" + self.tableWidget.item(i, k - 2).text() + "m\n" +
                                        "3.测段视距和：" + self.tableWidget.item(i, k - 1).text() + "m"
                                    )
                                    arithmeticProgressionCount_remark += 1
                                else:
                                    self.tableWidget.item(index, k).setText("-")
                                    self.tableWidget.item(index, k).setTextAlignment(QtCore.Qt.AlignCenter)

                        # 全体居中
                        self.tableWidget.item(i, k).setTextAlignment(QtCore.Qt.AlignCenter)

        #

        except Exception as e:
            print(e.__str__())

    def saveTable(self):
        """
        保存表格信息
        :return:
        """
        tableLenght = self.tableWidget.rowCount()
        stationID = []
        stationRemark = []
        dataItemCell = []
        for i in range(4, tableLenght):
            # 跳过表头
            if i % 4 == 0:
                # 站点单元对象合并后部分无数据，故要以定位基点遍历
                stationID.append(self.tableWidget.item(i, 0).text())
                stationRemark.append(self.tableWidget.item(i, 7).text())

            dataItemCell.append([self.tableWidget.item(i, 1).text(), self.tableWidget.item(i, 2).text(),
                                 self.tableWidget.item(i, 3).text(),
                                 self.tableWidget.item(i, 4).text(), self.tableWidget.item(i, 5).text(),
                                 self.tableWidget.item(i, 6).text()])

        # 测试
        return stationID, stationRemark, dataItemCell
