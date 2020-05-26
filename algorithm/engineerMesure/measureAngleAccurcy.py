#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 贯通误差计算测角精度

@author: GanAH  2020/5/17.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import math


def go():
    # 导线边数
    n = 12
    s = 150 # 米
    s = s*1000
    m_bata = 1.5665518616377234

    # 导线端点的横向误差
    mq = math.sqrt(n*n*s*s*m_bata*m_bata*(n+1.5)/(3*206265*206265))
    print(mq)
def angleAccuracy():
    teta = 100 # 米
    Mq = teta/2
    s = 150
    n = 12
    m_bata = 0.58*Mq*206265/(s*1000*n*math.sqrt((n+1.5)/3))
    print("±",m_bata,"″")

go()
angleAccuracy()