#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 日志工具类

@author: GanAH  2020/2/9.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""

import logging
import logging.config
from loggerConfig import logSetting


class Logger():
    def get_logger(self, name: object) -> object:
        logging.config.dictConfig(logSetting.LOGGING_DIC)
        return logging.getLogger(name)

    def set_disableLevel(self, level):
        if level == "WARNING":
            logging.disable(logging.WARNING)
        elif level == "CRITICAL":
            logging.disable(logging.CRITICAL)
        elif level == "INFO":
            logging.disable(logging.INFO)
        elif level == "ERROR":
            logging.disable(logging.ERROR)
        else:
            logging.disable(logging.DEBUG)
