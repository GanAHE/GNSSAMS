#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: DengGZC  2020/6/18.
@version 1.0.
@contact: dgzc159@163.com
"""
import win32com.client


def speaker(strText):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(strText)

