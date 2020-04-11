#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 日志格式

@author: GanAH  2020/2/9.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_LOG = os.path.join(BASE_DIR, './log/access.log')

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字

simple_format = '[task_id:%(name)s][%(levelname)s][%(asctime)s] %(message)s'

id_simple_format = '[task_id:%(name)s]-[%(levelname)s] - %(asctime)s-[%(filename)s-->>line:%(lineno)d]: %(message)s'
# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,

    # 1、定义日志的格式
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'id_simple': {
            'format': id_simple_format
        }
    },
    'filters': {},

    # 2、定义日志输出的目标：文件或者终端
    'handlers': {
        # 打印到终端的日志
        'stream': {
            'level': 'DEBUG',  # 定义接收级别
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'id_simple'  # 定义什么的格式输出
        },
        # 打印到文件的日志,收集info及以上的日志
        'access': {
            'level': 'DEBUG',  # 定义接收级别
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'id_simple',  # 定义什么的格式输出
            'filename': BASE_LOG,  # 日志文件
            # 'maxBytes': 1024*1024*5,  # 日志大小 5M
            'maxBytes': 1024 * 2,  # 每个日志文件的大小
            'backupCount': 5,  # 存5个文件
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },

    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['access', 'stream'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': False,  # 向上（更高level的logger）传递
        },
    },
}
