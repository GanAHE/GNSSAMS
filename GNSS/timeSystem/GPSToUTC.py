#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: DengGZC  2020/7/1.
@version 1.0.
@contact: dgzc159@163.com
"""
import datetime

def datetime_to_tow(t):
    """
    DateTime to GPS week and tow
    :param t: datetime
    :return: week,tow
    """
    week_ref = datetime.datetime(2014,2,16,0,0,0,0,None)
    refweek = 1780
    week = (t-week_ref).days//7+refweek
    tow = ((t-week_ref)-datetime.timedelta((week-refweek)*7.0)).total_seconds()
    return week,tow

def tow_to_datetime(tow,week):
    """
    GPS week and tow to DateTime
    :param tow: time of week in seconds
    :param week: GPS week
    :return: datetime
    """
    t = datetime.datetime(1980,1,6,0,0,0,0,None)
    t += datetime.timedelta(seconds=tow)
    t += datetime.timedelta(weeks=week)
    return t

def get_leap_seconds(time):
    if time <= GPSTime.from_datetime(datetime.datetime(2006,1,1)):
        raise ValueError("Don't know how many leap seconds to use before 2006")
    elif time <= GPSTime.from_datetime(datetime.datetime(2009,1,1)):
        return 14
    elif time <= GPSTime.from_datetime(datetime.datetime(2012, 1, 1)):
        return 15
    elif time <= GPSTime.from_datetime(datetime.datetime(2015, 7, 1)):
        return 16
    elif time <= GPSTime.from_datetime(datetime.datetime(2017, 7, 1)):
        return 17
    else:
        return 18

class GPSTime(object):
    def __init__(self, week, tow):
        self.week=week
        self.tow=tow
        self.seconds_in_week=604800

    @classmethod
    def from_datetime(cls, datetime):
        week, tow = datetime_to_tow(datetime)
        return cls(week, tow)

    @classmethod
    def from_meas(cls, meas):
        return cls(meas[1], meas[2])

    def __sub__(self, other):
        if isinstance(other, type(self)):
            return (self.week - other.week) * self.seconds_in_week + self.tow - other.tow
        elif isinstance(other, float) or isinstance(other, int):
            new_week = self.week
            new_tow = self.tow - other
            while new_tow < 0:
                new_tow += self.seconds_in_week
                new_week -= 1
            return GPSTime(new_week, new_tow)
        else:
            print("Type of subtraced:", type(other))
            raise NotImplementedError

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_week = self.week
            new_tow = self.tow + other
            while new_tow >= self.seconds_in_week:
                new_tow -= self.seconds_in_week
                new_week += 1
            return GPSTime(new_week, new_tow)
        else:
            print("Type of added:", type(other))
            raise NotImplementedError

    def __lt__(self, other):
        return self - other < 0

    def __gt__(self, other):
        return self - other > 0

    def __le__(self, other):
        return self - other <= 0

    def __ge__(self, other):
        return self - other >= 0

    def __eq__(self, other):
        return self - other == 0

    def as_datetime(self):
        return tow_to_datetime(self.tow, self.week)

    @property
    def day(self):
        return int(self.tow / (24 * 3600))

    def __str__(self):
        return "week: " + str(self.week) + "  tow: " + str(self.tow)

