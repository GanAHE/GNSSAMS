# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modelTrainWight.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from window.actionOperate.actionTrainThread import TrainModel


class Ui_Form(QtCore.QObject):
    infoEmit = QtCore.pyqtSignal(str, str)
    defaultDir = "./source/train_data/"
    dictPara = {"annotation": None, "classes": None, "anchors": None, "batch_size": 4, "num_epoche": 5,
                "load_pretrained": False, "weights": None, "freeze": True, "savePath": None}
    count = 0

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1196, 706)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setMaximumSize(QtCore.QSize(400, 500))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setMaximumSize(QtCore.QSize(100000, 100000))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.lineEdit_annotation_path = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_annotation_path.setReadOnly(True)
        self.lineEdit_annotation_path.setObjectName("lineEdit_annotation_path")
        self.horizontalLayout_5.addWidget(self.lineEdit_annotation_path)
        self.toolButton_annotation_path = QtWidgets.QToolButton(self.groupBox_3)
        self.toolButton_annotation_path.setObjectName("toolButton_annotation_path")
        self.horizontalLayout_5.addWidget(self.toolButton_annotation_path)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.lineEdit_classes_path = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_classes_path.setReadOnly(True)
        self.lineEdit_classes_path.setObjectName("lineEdit_classes_path")
        self.horizontalLayout_6.addWidget(self.lineEdit_classes_path)
        self.toolButton_classes_path = QtWidgets.QToolButton(self.groupBox_3)
        self.toolButton_classes_path.setObjectName("toolButton_classes_path")
        self.horizontalLayout_6.addWidget(self.toolButton_classes_path)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.lineEdit_anchors_path = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_anchors_path.setReadOnly(True)
        self.lineEdit_anchors_path.setObjectName("lineEdit_anchors_path")
        self.horizontalLayout_7.addWidget(self.lineEdit_anchors_path)
        self.toolButton_anchors_path = QtWidgets.QToolButton(self.groupBox_3)
        self.toolButton_anchors_path.setObjectName("toolButton_anchors_path")
        self.horizontalLayout_7.addWidget(self.toolButton_anchors_path)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.spinBox_onceTrainImages = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBox_onceTrainImages.setProperty("value", 4)
        self.spinBox_onceTrainImages.setObjectName("spinBox_onceTrainImages")
        self.horizontalLayout_8.addWidget(self.spinBox_onceTrainImages)
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.spinBox_detectionCount = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBox_detectionCount.setProperty("value", 5)
        self.spinBox_detectionCount.setObjectName("spinBox_detectionCount")
        self.horizontalLayout_8.addWidget(self.spinBox_detectionCount)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.checkBox_load_pretrainedModel = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_load_pretrainedModel.setObjectName("checkBox_load_pretrainedModel")
        self.horizontalLayout_10.addWidget(self.checkBox_load_pretrainedModel)
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_10.addWidget(self.label_9)
        self.lineEdit_pretrainedModelPath = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_pretrainedModelPath.setReadOnly(True)
        self.lineEdit_pretrainedModelPath.setObjectName("lineEdit_pretrainedModelPath")
        self.horizontalLayout_10.addWidget(self.lineEdit_pretrainedModelPath)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.checkBox_freeze = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_freeze.setObjectName("checkBox_freeze")
        self.verticalLayout_2.addWidget(self.checkBox_freeze)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_11.addWidget(self.label_10)
        self.lineEdit_saveModelPath = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_saveModelPath.setReadOnly(True)
        self.lineEdit_saveModelPath.setObjectName("lineEdit_saveModelPath")
        self.horizontalLayout_11.addWidget(self.lineEdit_saveModelPath)
        self.toolButton_saveModelPath = QtWidgets.QToolButton(self.groupBox_3)
        self.toolButton_saveModelPath.setObjectName("toolButton_saveModelPath")
        self.horizontalLayout_11.addWidget(self.toolButton_saveModelPath)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_startTrain = QtWidgets.QPushButton(self.groupBox_2)
        self.button_startTrain.setObjectName("button_startTrain")
        self.verticalLayout.addWidget(self.button_startTrain)
        self.button_violenceStop = QtWidgets.QPushButton(self.groupBox_2)
        self.button_violenceStop.setObjectName("button_violenceStop")
        self.verticalLayout.addWidget(self.button_violenceStop)
        self.button_testModel = QtWidgets.QPushButton(self.groupBox_2)
        self.button_testModel.setObjectName("button_testModel")
        self.verticalLayout.addWidget(self.button_testModel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lcdNumber = QtWidgets.QLCDNumber(self.groupBox_2)
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.HLine)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setMode(QtWidgets.QLCDNumber.Hex)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout.addWidget(self.lcdNumber)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./source/icon/QTUM.png"))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.horizontalLayout_3.addWidget(self.groupBox)

        self.retranslateUi(Form)
        # 初始化
        self._initPara()

        self.trainThread = TrainModel()
        self.trainThread.infoEmit.connect(self.actionInfoEvent)

        self.toolButton_annotation_path.clicked.connect(self.actionLoadAnnotationPath)
        self.toolButton_classes_path.clicked.connect(self.actionLoadClassesPath)
        self.toolButton_anchors_path.clicked.connect(self.actionLoadAnchorsPath)
        self.checkBox_load_pretrainedModel.clicked.connect(self.actionLoadPretrained_weights)
        self.toolButton_saveModelPath.clicked.connect(self.actionLoadSavePath)

        self.button_startTrain.clicked.connect(self.actionStartTrainModel)
        self.button_violenceStop.clicked.connect(self.actionViolenceStop)
        self.button_testModel.clicked.connect(self.actionTestModel)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_3.setTitle(_translate("Form", "训练参数"))
        self.label_3.setText(_translate("Form", "标注文件路径："))
        self.toolButton_annotation_path.setText(_translate("Form", "..."))
        self.label_4.setText(_translate("Form", "标注文件配套类名文件路径："))
        self.toolButton_classes_path.setText(_translate("Form", "..."))
        self.label_5.setText(_translate("Form", "anchors文件路径："))
        self.toolButton_anchors_path.setText(_translate("Form", "..."))
        self.label_6.setText(_translate("Form", "batch size："))
        self.label_7.setText(_translate("Form", "umber of epoches："))
        self.checkBox_load_pretrainedModel.setText(_translate("Form", "加载预训练模型"))
        self.label_9.setText(_translate("Form", "权重文件路径："))
        self.checkBox_freeze.setText(_translate("Form", "冻结darnet主体"))
        self.label_10.setText(_translate("Form", "训练模型保存路径："))
        self.toolButton_saveModelPath.setText(_translate("Form", "..."))
        self.button_startTrain.setText(_translate("Form", "训练模型"))
        self.button_violenceStop.setText(_translate("Form", "强制终止"))
        self.button_testModel.setText(_translate("Form", "测试模型"))
        self.label.setText(_translate("Form", "进程："))
        self.groupBox.setTitle(_translate("Form", "模型训练信息"))

    def _initPara(self):
        self.checkBox_freeze.setChecked(True)
        self.lineEdit_saveModelPath.setText("./workspace/trained_weights.h5")
        self.dictPara["savePath"] = "./workspace/trained_weights.h5"
        self.textEdit.setText("\t\t=== 模型训练 ===")

    def actionInfoEvent(self, type, strinfo):
        if type == "train":
            self.textEdit.append(strinfo)
            self.count += 1
            self.lcdNumber.setProperty("value", self.count)
        else:
            self.infoEmit.emit(type, strinfo)

    def actionLoadAnnotationPath(self):
        filepath = self.loadPath("annotation")
        if filepath is not None:
            self.lineEdit_annotation_path.setText(filepath)

    def actionLoadClassesPath(self):
        filepath = self.loadPath("classes")
        if filepath is not None:
            self.lineEdit_classes_path.setText(filepath)

    def actionLoadAnchorsPath(self):
        filepath = self.loadPath("anchors")
        if filepath is not None:
            self.lineEdit_anchors_path.setText(filepath)

    def actionLoadPretrained_weights(self):
        if self.checkBox_load_pretrainedModel.isChecked():
            self.dictPara["load_pretrained"] = True
            filepath = self.loadPath("weights")
            if filepath is not None:
                self.lineEdit_pretrainedModelPath.setText(filepath)
        else:
            self.dictPara["load_pretrained"] = False

    def actionLoadSavePath(self):
        filepath = self.loadPath("savePath")
        if filepath is not None:
            self.lineEdit_saveModelPath.setText(filepath)

    def loadPath(self, key):
        # 获取字典键值映射信息
        comment = self.dictKeyMap(key)
        filePath, t = QtWidgets.QFileDialog.getOpenFileName(self.parent(), comment + "文件", self.defaultDir,
                                                            "All Files(*);;txt(*.txt);;")
        if filePath != "":
            (dir, fileName) = os.path.split(filePath)
            self.defaultDir = dir
            self.dictPara[key] = filePath
            return filePath
        else:
            return None

    def actionStartTrainModel(self):
        self.dictPara["batch_size"] = self.spinBox_onceTrainImages.value()
        self.dictPara["num_epoche"] = self.spinBox_detectionCount.value()
        self.dictPara["freeze"] = self.checkBox_freeze.isChecked()
        self.trainThread.setPara(self.dictPara)
        justice = 0
        # 判断字典是否有空值
        for (key, value) in self.dictPara.items():
            # 获取字典键值映射信息
            comment = self.dictKeyMap(key)
            if value is None and key != "weights":
                self.actionInfoEvent("V", "警告，" + comment + "文件路径未导入！请检查参数设置！")
                self.actionInfoEvent("W", "警告，" + comment + "文件路径未导入！")
                justice = 0
                break
            else:
                justice = 1
        if justice == 1:
            self.actionInfoEvent("V", "启动模型训练线程")
            self.actionInfoEvent("I", "传入参数：" + str(self.dictPara))

            # 开启线程
            self.trainThread.start()
            self.actionInfoEvent("I", "已开启线程...")
            self.actionInfoEvent("I", "模型训练中...")

    def killThread(self):
        self.trainThread.quit()

    def actionViolenceStop(self):
        pass

    def actionTestModel(self):
        """
        测试模型
        :return:
        """
        self.actionInfoEvent("testModel", None)

    def dictKeyMap(self, key):
        if key == "annotation":
            comment = "标注"
        elif key == "classes":
            comment = "标注文件对应类名"
        elif key == "anchors":
            comment = "anchors"
        elif key == "weights":
            comment = "预加载模型"
        else:
            comment = "保存训练结果模型"
        return comment
