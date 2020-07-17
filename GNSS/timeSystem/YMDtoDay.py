#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:由年月日计算该日属于今年第几天

@author: GanAH  2019/10/3.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""

month_of_days31 = [1, 3, 5, 7, 8, 10, 12]
month_of_days30 = [4, 6, 9, 11]
feb_month = 2
def get_day_of_year(year, month, day):
    """
    获取一个日期在这一年中的第几天
    :param year: 年份
    :param month: 月份
    :param day: 日期
    :return: 在这一年中的第几天
    """
    # 参数校验
    error_msg = validate_param(year, month, day)
    if error_msg:
        return error_msg

    if month == 1:
        return day

    if month == 2:
        return day + 31

    days_of_31_num = 0
    days_of_30_num = 0
    # 31天月份数
    for days_of_31 in month_of_days31:
        if days_of_31 < month:
            days_of_31_num += 1
        else:
            break

    # 30天月份数
    for days_of_30 in month_of_days30:
        if days_of_30 < month:
            days_of_30_num += 1
        else:
            break

    return days_of_31_num * 31 + days_of_30_num * 30 + (29 if is_leap_year(year) else 28) + day

def is_leap_year(year):
    """
    判断当前年份是不是闰年，年份公元后，且不是过大年份
    :param year: 年份
    :return: True 闰年， False 平年
    """
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    return False

def validate_param(year, month, day):
    """
    参数校验
    :param year: 年份
    :param month: 月份
    :param day: 日期
    :return: error_msg 错误信息，没有为空
    """
    error_msg = u''
    if not isinstance(year, int) or year < 1:
        error_msg = u'年份输入不符合要求'
    if not isinstance(month, int) or month < 1 or month > 12:
        error_msg = u'月份输入不符合要求'
    if not isinstance(day, int) or day < 1 \
            or (month in month_of_days31 and day > 31) \
            or (month in month_of_days30 and day > 30) \
            or (month == feb_month and (day > 29 if is_leap_year(year) else day > 28)):
        error_msg = u'日期输入不符合要求'
    return error_msg


