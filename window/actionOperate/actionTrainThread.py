#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 自训练模型响应类

@author: GanAH  2020/6/18.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
"""
Retrain the YOLO model for your own dataset.
"""

import keras
import keras.backend as K
import numpy as np
import tensorflow as tf
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.layers import Input, Lambda
from keras.models import Model
from keras.optimizers import Adam

from MTD.yolo3.model import preprocess_true_boxes, yolo_body, yolo_loss
from MTD.yolo3.utils import get_random_data

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
from PyQt5.QtCore import QThread, pyqtSignal, QObject


class TrainModel(QThread):
    infoEmit = pyqtSignal(str, str)
    overEmit = pyqtSignal()

    def __init__(self):
        super(TrainModel, self).__init__()

    def setPara(self, dictPara):
        self.annotation_path = dictPara["annotation"]
        self.classes_path = dictPara["classes"]
        self.anchors_path = dictPara["anchors"]
        self.weights_path = dictPara["weights"]
        self.save_path = dictPara["savePath"]
        self.batch_size = dictPara["batch_size"]
        self.num_epoche = dictPara["num_epoche"]
        self.load_pretrained = dictPara["load_pretrained"]
        self.freeze = dictPara["freeze"]

    def run(self) -> None:
        try:
            logDir = "./log/"
            self.train_model(self.annotation_path, logDir, self.classes_path, self.anchors_path, self.batch_size,
                             self.num_epoche, self.load_pretrained, self.weights_path, self.freeze, self.save_path)
        except Exception as e:
            self.sendInfo("E", "发生意料之外的错误！错误原因：" + e.__str__())
            self.sendInfo("V", "发生意料之外的错误！错误原因：" + e.__str__())

    def killThread(self):
        self.quit()

    def sendInfo(self, type, info):
        self.infoEmit.emit(type, info)

    def train_model(self, annotation_path, log_dir, classes_path, anchors_path, batch_size,
                    num_epoches, load_pretrained, weights_path, is_freeze, save_path):
        """
        训练模型
        :param annotation_path: 标注文件的路径
        :param log_dir: 训练结果和日志文件储存的目录
        :param classes_path: 与标注文件配套的类名文件
        :param anchors_path: anchors文件
        :param batch_size: 每一批训练多少张图片
        :param num_epoches: 一共要识别多少次
        :param load_pretrained: 是否要加载预训练模型？
        :param weights_path: 如果加载了预训练模型，给出权重文件的路径
        :param is_freeze: 是否要冻结darnet主体
        :param save_path: 权重保存路径
        :return: None
        """
        class_names = self.get_classes(classes_path)
        num_classes = len(class_names)
        anchors = self.get_anchors(anchors_path)
        ifURL = True  # 图片路径名是否是URL

        input_shape = (416, 416)  # multiple of 32, hw

        model = self.create_model(input_shape, anchors, num_classes, load_pretrained=load_pretrained,
                                  freeze_body=2, weights_path=weights_path)  # make sure you know what you freeze

        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, verbose=1)  # learning rate delay
        early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10,
                                       verbose=1)  # early stopping when vai_loss stops reduce

        val_split = 0.1
        with open(annotation_path) as f:
            lines = f.readlines()
        np.random.seed(10101)
        np.random.shuffle(lines)
        np.random.seed(None)
        num_val = int(len(lines) * val_split)  # 验证集样本数
        num_train = len(lines) - num_val  # 训练集样本数
        customCallback = CustomCallback(num_train, batch_size, num_epoches)
        customCallback.infoEmit.connect(self.sendInfo)
        steps_per_epoch = max(1, num_train // batch_size)  # 训练时，每一epoch有多少个batch

        # Train with frozen layers first, to get a stable loss.
        # Adjust num epochs to your dataset. This step is enough to obtain a not bad model.
        sess = K.get_session()
        with sess.as_default():
            with sess.graph.as_default():
                if not is_freeze:
                    for i in range(len(model.layers)):
                        model.layers[i].trainable = True
                model.compile(optimizer=Adam(lr=1e-3), loss={'yolo_loss': lambda y_true, y_pred: y_pred})

                self.sendInfo("train",
                              'Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val,
                                                                                                   batch_size))
                history = model.fit_generator(
                    self.data_generator_wrapper(lines[:num_train], batch_size, input_shape, anchors, num_classes,
                                                URL=ifURL),
                    steps_per_epoch=steps_per_epoch,
                    validation_data=self.data_generator_wrapper(lines[num_train:], batch_size, input_shape, anchors,
                                                                num_classes,
                                                                URL=ifURL),
                    validation_steps=max(1, num_val // batch_size),
                    epochs=num_epoches,
                    initial_epoch=0,
                    verbose=0,
                    callbacks=[customCallback, reduce_lr, early_stopping])
                model.save_weights(save_path)

    def get_classes(self, classes_path):
        '''loads the classes'''
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def get_anchors(self, anchors_path):
        '''loads the anchors from a file'''
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def create_model(self, input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2,
                     weights_path='model_data/yolo_weights.h5'):
        '''create the training model'''
        K.clear_session()  # get a new session
        image_input = Input(shape=(None, None, 3))
        h, w = input_shape
        num_anchors = len(anchors)

        y_true = [Input(shape=(h // {0: 32, 1: 16, 2: 8}[l], w // {0: 32, 1: 16, 2: 8}[l], \
                               num_anchors // 3, num_classes + 5)) for l in range(3)]

        model_body = yolo_body(image_input, num_anchors // 3, num_classes)
        self.sendInfo("train", 'Create YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

        if load_pretrained:
            model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
            self.sendInfo("train", 'Load weights {}.'.format(weights_path))
            if freeze_body in [1, 2]:
                # Freeze darknet53 body or freeze all but 3 output layers.
                num = (185, len(model_body.layers) - 3)[freeze_body - 1]
                for i in range(num): model_body.layers[i].trainable = False
                self.sendInfo("train",
                              'Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

        model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
                            arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})(
            [*model_body.output, *y_true])
        model = Model([model_body.input, *y_true], model_loss)

        return model

    def data_generator(self, annotation_lines, batch_size, input_shape, anchors, num_classes, URL=False):
        '''data generator for fit_generator'''
        n = len(annotation_lines)
        i = 0
        while True:
            image_data = []
            box_data = []
            for b in range(batch_size):
                if i == 0:
                    np.random.shuffle(annotation_lines)
                image, box = get_random_data(annotation_lines[i], input_shape, random=True, URL=URL)
                image_data.append(image)
                box_data.append(box)
                i = (i + 1) % n
            image_data = np.array(image_data)
            box_data = np.array(box_data)
            y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
            yield [image_data, *y_true], np.zeros(batch_size)

    def data_generator_wrapper(self, annotation_lines, batch_size, input_shape, anchors, num_classes, URL=False):
        n = len(annotation_lines)
        if n == 0 or batch_size <= 0: return None
        return self.data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes, URL)


class CustomCallback(QObject, keras.callbacks.Callback):
    infoEmit = pyqtSignal(str, str)

    def __init__(self, num_train, batch_size, num_epoches):
        super(CustomCallback, self).__init__()
        self.num_train = num_train
        self.batch_size = batch_size
        self.num_epoches = num_epoches
        self.num_batches = max(1, num_train // batch_size)

    def on_train_begin(self, logs=None):
        self.sendTrainInfo("train", "Starting training:")

    def on_train_end(self, logs=None):
        self.sendTrainInfo("train", "Stop training.")

    def on_epoch_begin(self, epoch, logs=None):
        self.sendTrainInfo("train", "Start epoch {}/{} of training:".format(epoch, self.num_epoches))

    def on_epoch_end(self, epoch, logs=None):
        self.sendTrainInfo("train",
                           "End epoch {}/{} of training:  loss = {}".format(epoch, self.num_epoches, logs["loss"]))

    def on_train_batch_begin(self, batch, logs=None):
        self.sendTrainInfo("train", "...Training: start of batch {} / {}".format(batch, self.num_batches))

    def on_train_batch_end(self, batch, logs=None):
        self.sendTrainInfo("train",
                           "...Training: end of batch {} / {}:  loss = {}".format(batch, self.num_batches,
                                                                                  logs["loss"]))

    def sendTrainInfo(self, type, strInfo):
        """
        发送信号
        :param strInfo: 信号
        :return:
        """
        self.infoEmit.emit(type, strInfo)
