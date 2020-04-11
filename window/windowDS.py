# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windowDS.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from algorithm.engineerMesure.leicaGsiFormat import LeicaGSIFormat
from database.database import Database
from window import welcomeWight, coorTranOpenFileDiaog, coorTranWight, leicaDataFormatWight, controlNetAdjustmentWight
from window.action.actionLeicaGSI import ActionLeicaGSIThread
from window.action.actionReport import Report
from window.file.fileMsg import FileMsg
from window.tipDig import ActionWarnException


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1241, 725)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./source/icon/icon_资料.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setObjectName("widget")
        self.verticalLayout_4.addWidget(self.widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./source/icon/icon_流水线.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab, icon1, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout_5.addWidget(self.tableWidget)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        self.verticalLayout_5.addWidget(self.tableWidget_2)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./source/icon/icon_网络教育.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_3, icon2, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.tab_4)
        self.progressBar.setProperty("value", 40)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./source/icon/icon_混合式学习.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_4, icon3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("./source/icon/icon_垃圾桶.png"))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./source/icon/ethereum-mining.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_2, icon4, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1241, 26))
        self.menubar.setObjectName("menubar")
        self.menu_F = QtWidgets.QMenu(self.menubar)
        self.menu_F.setObjectName("menu_F")
        self.menu_C = QtWidgets.QMenu(self.menubar)
        self.menu_C.setObjectName("menu_C")
        self.menu_S = QtWidgets.QMenu(self.menubar)
        self.menu_S.setObjectName("menu_S")
        self.menu_V = QtWidgets.QMenu(self.menubar)
        self.menu_V.setObjectName("menu_V")
        self.menu_H = QtWidgets.QMenu(self.menubar)
        self.menu_H.setObjectName("menu_H")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.dockWidget_2 = QtWidgets.QDockWidget(mainWindow)
        self.dockWidget_2.setFloating(False)
        self.dockWidget_2.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.dockWidgetContents_2)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.treeView = QtWidgets.QTreeView(self.groupBox)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout.addWidget(self.textEdit_2)
        self.horizontalLayout.addWidget(self.groupBox)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        mainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_2)
        self.toolBar = QtWidgets.QToolBar(mainWindow)
        self.toolBar.setObjectName("toolBar")
        mainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menuItem_new = QtWidgets.QAction(mainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./source/icon/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuItem_new.setIcon(icon5)
        self.menuItem_new.setObjectName("menuItem_new")
        self.menuItem_openFile = QtWidgets.QAction(mainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./source/icon/futuro_icons_547.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuItem_openFile.setIcon(icon6)
        self.menuItem_openFile.setObjectName("menuItem_openFile")
        self.menuItem_saveFile = QtWidgets.QAction(mainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./source/icon/保存.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuItem_saveFile.setIcon(icon7)
        self.menuItem_saveFile.setObjectName("menuItem_saveFile")
        self.menuItem_quitSystem = QtWidgets.QAction(mainWindow)
        self.menuItem_quitSystem.setObjectName("menuItem_quitSystem")
        self.menuItem_coorTran = QtWidgets.QAction(mainWindow)
        self.menuItem_coorTran.setObjectName("menuItem_coorTran")
        self.actions_2 = QtWidgets.QAction(mainWindow)
        self.actions_2.setObjectName("actions_2")
        self.actionsd = QtWidgets.QAction(mainWindow)
        self.actionsd.setObjectName("actionsd")
        self.actionsd_2 = QtWidgets.QAction(mainWindow)
        self.actionsd_2.setObjectName("actionsd_2")
        self.actiond_2 = QtWidgets.QAction(mainWindow)
        self.actiond_2.setObjectName("actiond_2")
        self.actionsd_3 = QtWidgets.QAction(mainWindow)
        self.actionsd_3.setObjectName("actionsd_3")
        self.actiondf = QtWidgets.QAction(mainWindow)
        self.actiondf.setObjectName("actiondf")
        self.actiond_3 = QtWidgets.QAction(mainWindow)
        self.actiond_3.setObjectName("actiond_3")
        self.actiond_4 = QtWidgets.QAction(mainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("./source/icon/pc.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiond_4.setIcon(icon8)
        self.actiond_4.setObjectName("actiond_4")
        self.actionf = QtWidgets.QAction(mainWindow)
        self.actionf.setObjectName("actionf")
        self.actiond_5 = QtWidgets.QAction(mainWindow)
        self.actiond_5.setObjectName("actiond_5")
        self.actions_3 = QtWidgets.QAction(mainWindow)
        self.actions_3.setObjectName("actions_3")
        self.menuItem_resultReport = QtWidgets.QAction(mainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("./source/icon/报表统计.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuItem_resultReport.setIcon(icon9)
        self.menuItem_resultReport.setObjectName("menuItem_resultReport")
        self.actionb = QtWidgets.QAction(mainWindow)
        self.actionb.setObjectName("actionb")
        self.menuItem_backWelcome = QtWidgets.QAction(mainWindow)
        self.menuItem_backWelcome.setObjectName("menuItem_backWelcome")
        self.menu_F.addAction(self.menuItem_new)
        self.menu_F.addSeparator()
        self.menu_F.addAction(self.menuItem_openFile)
        self.menu_F.addSeparator()
        self.menu_F.addAction(self.menuItem_saveFile)
        self.menu_F.addSeparator()
        self.menu_F.addAction(self.menuItem_resultReport)
        self.menu_F.addSeparator()
        self.menu_F.addAction(self.menuItem_quitSystem)
        self.menu_C.addAction(self.menuItem_coorTran)
        self.menu_C.addSeparator()
        self.menu_C.addAction(self.actions_2)
        self.menu_C.addSeparator()
        self.menu_C.addAction(self.actionsd)
        self.menu_C.addSeparator()
        self.menu_C.addAction(self.actionsd_2)
        self.menu_C.addSeparator()
        self.menu_C.addAction(self.actiond_2)
        self.menu_C.addSeparator()
        self.menu_C.addAction(self.actionsd_3)
        self.menu_C.addSeparator()
        self.menu_S.addAction(self.actiondf)
        self.menu_S.addAction(self.actiond_3)
        self.menu_S.addAction(self.actiond_4)
        self.menu_S.addAction(self.menuItem_backWelcome)
        self.menu_V.addAction(self.actionb)
        self.menu_H.addAction(self.actiond_5)
        self.menu_H.addAction(self.actions_3)
        self.menubar.addAction(self.menu_F.menuAction())
        self.menubar.addAction(self.menu_C.menuAction())
        self.menubar.addAction(self.menu_S.menuAction())
        self.menubar.addAction(self.menu_H.menuAction())
        self.menubar.addAction(self.menu_V.menuAction())
        self.toolBar.addAction(self.menuItem_new)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actiond_4)
        self.toolBar.addAction(self.menuItem_openFile)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.menuItem_saveFile)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.menuItem_resultReport)
        self.toolBar.addSeparator()

        self.retranslateUi(mainWindow)
        self.tabWidget.setCurrentIndex(0)
        # 初始化页面
        self.welcomeWight_ui = welcomeWight.Ui_Form()
        self.welcomeWight_ui.setupUi(self.widget)
        self.welcomeWight()

        self.coorTranWight_ui = coorTranWight.Ui_Form()
        self.coorTranWight_ui.infoEmit.connect(self.displayInfo)

        # self.leicaDataFormat_ui = leicaDataFormatWight.Ui_Form()

        # self.controlNetAdjustment_ui = controlNetAdjustment.Ui_Form()

        self.dialog = QtWidgets.QDialog()
        self.dialogUi = coorTranOpenFileDiaog.Ui_Dialog()
        self.dialogUi.fileReadEmit.connect(self.setOpenFileInfo)
        self.dialogUi.infoEmit.connect(self.displayInfo)

        self.menuItem_coorTran.triggered.connect(self.coorTranQwight)
        self.actions_2.triggered.connect(self.leicaFormatWight)
        self.actionsd.triggered.connect(self.horizontalControlNetwork)
        self.menuItem_openFile.triggered.connect(self.coorTranOpenFileDialog)
        self.menuItem_backWelcome.triggered.connect(self.welcomeWight)
        self.actions_3.triggered.connect(self.dockWidget_2.show)
        self.menuItem_resultReport.triggered.connect(self.saveReport)

        self.actiond_5.triggered.connect(self.onlineHelp)

        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "工程测量软件设计窗口初稿(*测试功能用)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("mainWindow", "操作"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("mainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("mainWindow", "New Row"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "New Column"))
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("mainWindow", "New Row"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("mainWindow", "New Row"))
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText(_translate("mainWindow", "New Row"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "New Column"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "New Column"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("mainWindow", "监控"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("mainWindow", "点位"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("mainWindow", "其他"))
        self.menu_F.setTitle(_translate("mainWindow", "文件(&F)"))
        self.menu_C.setTitle(_translate("mainWindow", "功能选择(&C)"))
        self.menu_S.setTitle(_translate("mainWindow", "设置(&S)"))
        self.menu_V.setTitle(_translate("mainWindow", "版本(&V)"))
        self.menu_H.setTitle(_translate("mainWindow", "帮助(&H)"))
        self.dockWidget_2.setWindowTitle(_translate("mainWindow", "状态栏"))
        self.label_2.setText(_translate("mainWindow", "文件列表"))
        self.label.setText(_translate("mainWindow", "状态信息"))
        self.toolBar.setWindowTitle(_translate("mainWindow", "toolBar"))
        self.menuItem_new.setText(_translate("mainWindow", "新建(&N)"))
        self.menuItem_openFile.setText(_translate("mainWindow", "打开文件(&O)"))
        self.menuItem_saveFile.setText(_translate("mainWindow", "保存文件(&S)"))
        self.menuItem_quitSystem.setText(_translate("mainWindow", "退出系统(&Q)"))
        self.menuItem_coorTran.setText(_translate("mainWindow", "坐标变换(&T)"))
        self.actions_2.setText(_translate("mainWindow", "徕卡数字水准仪格式转换及输出(&P)"))
        self.actionsd.setText(_translate("mainWindow", "地面控制网平差(&D)"))
        self.actionsd_2.setText(_translate("mainWindow", "铁路曲线计算(&T)"))
        self.actiond_2.setText(_translate("mainWindow", "CPIII控制网平差(&C)"))
        self.actionsd_3.setText(_translate("mainWindow", "静态GNSS网平差(&G)"))
        self.actiondf.setText(_translate("mainWindow", "计算参数(&S)"))
        self.actiond_3.setText(_translate("mainWindow", "系统参数(&S)"))
        self.actiond_4.setText(_translate("mainWindow", "界面设置(&W)"))
        self.actionf.setText(_translate("mainWindow", "f"))
        self.actiond_5.setText(_translate("mainWindow", "在线帮助(&I)"))
        self.actions_3.setText(_translate("mainWindow", "本地文档(&)"))
        self.menuItem_resultReport.setText(_translate("mainWindow", "导出结果报告(&O)"))
        self.actionb.setText(_translate("mainWindow", "版本信息(&V)"))
        self.menuItem_backWelcome.setText(_translate("mainWindow", "返回欢迎界面(&B)"))

    def displayInfo(self, type, strInfo):

        if type == "I":
            self.textEdit_2.append(strInfo)
        else:
            ActionWarnException(self.centralwidget).actionWarnException(type, strInfo)

    def showPan(self, fileRoot):
        """
        文件列表树
        :param: 文件所在相对目录，不能包含文件名
        :return:None
        """
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(fileRoot)
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(fileRoot))

    """
    # 切换功能面板构造
    """

    def coorTranQwight(self):
        """
        坐标转换功能面板
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("mainWindow", "坐标转换"))
        # 界面重构存储区域
        self.widget.deleteLater()
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setObjectName("widget")
        self.verticalLayout_4.addWidget(self.widget)
        self.coorTranWight_ui.setupUi(self.widget)

    def leicaFormatWight(self):
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("mainWindow", "电子手簿"))
        # 界面重构存储区域
        self.widget.deleteLater()
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setObjectName("widget")
        self.verticalLayout_4.addWidget(self.widget)
        self.leicaDataFormat_ui = leicaDataFormatWight.Ui_Form()
        self.leicaDataFormat_ui.setupUi(self.widget)

    def horizontalControlNetwork(self):
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("mainWindow", "控制网"))
        # 界面重构存储区域
        self.widget.deleteLater()
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setObjectName("widget")
        self.verticalLayout_4.addWidget(self.widget)

        self.controlNetAdjustment_ui = controlNetAdjustmentWight.Ui_Form()
        self.controlNetAdjustment_ui.setupUi(self.widget)

    def welcomeWight(self):
        """
        欢迎页面
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("mainWindow", "欢迎"))
        self.widget.deleteLater()
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setObjectName("widget")
        self.verticalLayout_4.addWidget(self.widget)
        self.welcomeWight_ui.setupUi(self.widget)

    def coorTranOpenFileDialog(self):
        """
        坐标文件打开对话框
        :return: None
        """
        try:
            # 获取当前功能模块
            tabIndex = self.tabWidget.currentIndex()
            tabLable = self.tabWidget.tabText(tabIndex)
            _translate = QtCore.QCoreApplication.translate
            if tabLable == "坐标转换":
                # 界面重构存储区域
                self.dialogUi.setupUi(self.dialog)
                self.dialog.show()

            elif tabLable == "电子手簿":
                # 界面wight区域重构
                gsiDataList, filePath = FileMsg(self.centralwidget).openFile()
                Database.leicaSourceGsiData = gsiDataList
                # 显示文件区域
                self.showPan(os.path.dirname(os.path.realpath(filePath)))

                # 直接执行解析
                # ActionLeicaGSIThread().start()
                # 从数据库获取数据
                self.textEdit_2.append("---读取GSI数据文件....")
                self.displayInfo('I', "打开窗口并读取GSI数据文件")
                sourceStrData = Database.leicaSourceGsiData
                # 格式解析
                leicaGSIAnalysisDict = LeicaGSIFormat(sourceStrData).getAnalysisDict()
                self.textEdit_2.append("---完成GSI数据文件解析....")
                self.displayInfo('I', "完成GSI数据文件解析")
                # 解析显示
                self.textEdit_2.append("\n~\n")  # 分化
                self.textEdit_2.append("----【 GSI 文件解析结果 】-----")
                self.textEdit_2.append(" 一.测量模式\n" + str(leicaGSIAnalysisDict.get("model")))
                self.textEdit_2.append("\n 二.控制点或重要点ID（非普通）及地面高/mm\n * 指点名一段测段两端记录的点,点名记录值规定三位\n")
                self.textEditFormatAdd(leicaGSIAnalysisDict.get("ID"))
                self.textEdit_2.append(
                    "\n 四.BFFB 数据\n * 六位的数据前两位为标识符，非有效数据 \n 照准点ID 距离Distance/mm  后视|前视距/mm 复测次数  单次测量标准偏差/mm \n")
                self.textEditFormatAdd(leicaGSIAnalysisDict.get("data"))
                self.textEdit_2.append("\n 五.解算数据\n 当前归算点 站间差/mm 累积站差/mm   距离平衡/mm  测线总距离/mm  地面高（起点高或测量高）/mm \n")
                self.textEditFormatAdd(leicaGSIAnalysisDict.get("calculator"))
                # 解析结果，存入数据库
                Database.leicaAnalysisDict = leicaGSIAnalysisDict
                # 发送表格开始显示信号
                self.leicaDataFormat_ui.showTableEmit.emit()
                self.displayInfo('A', "\n解析数据文件完成\n# 注意：在退出请选择是否保存报告或数据")

            elif tabLable == "控制网":
                measureNetData, filePath = FileMsg(self.centralwidget).openFile()
                # 显示文件信息
                self.showPan(os.path.dirname(os.path.realpath(filePath)))
                # 显示到监控区域
                self.textEdit_2.append("--【CASA in2 测量数据】--\n")
                self.textEdit_2.append(" 1.文件路径：" + filePath + "\n")
                self.textEdit_2.append(" 2.数据：\n")
                self.textEditFormatAdd(measureNetData)
                # 存入数据库
                Database.COSAControlNetMersureData = measureNetData

            else:
                ActionWarnException(self.centralwidget).actionWarnException("W", "请先选择相应的功能！")
        except Exception as e:
            self.displayInfo("E", e.__str__())

    def setOpenFileInfo(self, typeInt, dirPath):
        """
        导入坐标文件信息监控
        :param typeInt: 文件类型
        :return:None
        """
        self.textEdit_2.append("导入文件....")
        self.textEdit_2.append("数据如下：")
        if typeInt == 0:
            self.textEdit_2.append("---【原始坐标文件】---")
            self.textEdit_2.append(str(Database.coorTranSourceData))
            self.showPan(dirPath)
        else:
            self.textEdit_2.append("---【目标坐标文件】---")
            self.textEdit_2.append(str(Database.coorTranTargetData))

    def saveReport(self):
        # 从选择判断当前执行的操作
        tabIndex = self.tabWidget.currentIndex()
        tabLabel = self.tabWidget.tabText(tabIndex)
        # 第一标签页
        try:
            if tabIndex == 0:
                if tabLabel == "坐标转换":
                    self.textEdit_2.append("坐标转换报告导出中....")
                    # 从数据库获取结果
                    resultDict = Database.coorTranResultDict
                    resultFormatList = Database.coorTranResultFormatListData

                    # 获取保存的文件路径/文件名
                    filePath = FileMsg(self.centralwidget).getWriteFilePath("txt")
                    self.report = Report("C", filePath, resultDict, resultFormatList)
                    self.report.start()
                elif tabLabel == "电子手簿":
                    """
                    # 徕卡数据
                    """
                    measureINFO, stationId, stationRemark, dataItemCell = self.leicaDataFormat_ui.saveTable()
                    # 获取状态栏的输出的文本
                    statusText = self.textEdit_2.toPlainText()
                    index = 0
                    for i in range(len(statusText)):
                        if statusText[i].strip() == "~":
                            index = i
                            break
                    statusText = statusText[index + 1:]

                    filePath = FileMsg(self.centralwidget).getWriteFilePath("docx")

                    if filePath != "":
                        self.report = Report("L", filePath, measureINFO, stationId, stationRemark, dataItemCell,
                                             statusText)
                        self.report.start()
                        # 结束弹窗
                        ActionWarnException(self.centralwidget).actionWarnException("A",
                                                                                    "【" + tabLabel + "】" + "报告导出中，文件转码时间\n较长，请耐心等待！")
                        self.textEdit_2.append("【" + tabLabel + "】" + "报告导出中，文件转码时间较长，请耐心等待！完成后将在指定目录生成")
                    else:
                        ActionWarnException(self.centralwidget).actionWarnException("A", "已取消导出操作。")
                elif tabLabel == "控制网":  # 平面控制网
                    ActionWarnException(self.centralwidget).actionWarnException("A", "暂未开发该功能。")
                else:
                    self.displayInfo("A", "当前所进行的操作无需本功能的支持。")


        except Exception as e:
            self.displayInfo("W", "错误！可能原因：\n 1.没有任何需要导出的数据；\n2. " + e.__str__())

    def onlineHelp(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://9jke6l.coding-pages.com/'))

    def textEditFormatAdd(self, twoDissList):
        listLen = len(twoDissList)
        if listLen == 0:
            return False
        else:
            for i in range(len(twoDissList)):
                self.textEdit_2.append(str(twoDissList[i]))
