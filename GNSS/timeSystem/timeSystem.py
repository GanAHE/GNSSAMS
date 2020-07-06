#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 世界通用时间时间系统类

@author: GanAH  2019/11/27.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from database import database
# from GNSS.timeSystem import GPSToUTC
import datetime

class TimeSystemChange:
    """
    #GLTime
    """
    _year = None
    _month = None
    _day = None
    _hour = None
    _minute = None
    _second = None
    """
    # JDTime
    """
    _JD = None
    _JDSec = None
    """
    # GPSTime
    """
    _GPSTimeWN = None
    _GPSTimeSec = None

    """
    #BDTime
    """
    _BDTimeWN = None
    _BDTimeSec = None

    """
    # UTC
    """
    _UTC_year = None
    _UTC_month = None
    # _UTC_day = None
    _UTC_hour = None
    _UTC_minute = None
    _UTC_second = None

    def __init__(self, *args):
        # GLTime
        if len(args) == 6:
            self._year = args[0]
            self._month = args[1]
            self._day = args[2]
            self._hour = args[3]
            self._minute = args[4]
            self._second = args[5]
        # GPSTime
        elif len(args) == 2:
            self._GPSTimeWN = args[0]
            self._GPSTimeSec = args[1]
        elif len(args) == 1:
            self._JD = args[0]
        else:
            # Database()已实例化，直接类名为静态存储！
            database.Database.warnExceptionText = "错误的参数数目！"
            print(database.Database.warnExceptionText)

    """格里高利历 与 儒略历 的转换"""

    def GL2JD(self):
        if self._month <= 2:
            self._year = self._year - 1
            self._month = self._month + 12
        JD = int(365.25 * self._year) + int(30.6001 * (self._month + 1)) + self._day + 1720981.5 + self._hour / 24.0 + \
            self._minute / 1440.0 + self._second / 86400.0
        # print(JD)
        return JD

    def JD2GL(self, JD):
        a = int(JD + 0.5)
        #    print(a)
        b = a + 1537
        #    print(b)
        c = int((b - 122.1) / 365.25)
        #    print(c)
        d = int(365.25 * c)
        e = int((b - d) / 30.6)
        Day = b - d - int(30.6001 * e)
        Month = e - 1 - 12 * int(e / 14)
        Year = c - 4715 - int((7 + Month) / 10)
        Hour = int(24 * (JD + 0.5 - int(JD + 0.5)))
        Minute = int(60 * (24 * (JD + 0.5 - int(JD + 0.5)) - Hour))
        Second = int(60 * (60 * (24 * (JD + 0.5 - int(JD + 0.5)) - Hour) - Minute))
        return Year, Month, Day, Hour, Minute, Second

    """儒略历 与 GPS时间 的转换"""

    def JD2GPSTime(self, JD):
        julday = int(JD)
        juldaySec = (JD - julday) * 60.0 * 60.0 * 24
        gps_week = int((JD - 2444244.5) / 7)
        second_of_week = round(((julday - 2444244) % 7 + (juldaySec / (60.0 * 60.0 * 24) - 0.5)) * 86400)
        # print(gps_week, second_of_week)
        return gps_week, second_of_week

    def GPSTime2JD(self):
        JD = self._GPSTimeWN * 7 + self._GPSTimeSec / 86400 + 2444244.5
        return JD

    """GPS时 与 UTC 的转换"""

    def GPSTime2UTC(self):
        JD = self.GPSTime2JD()
        Year, Month, Day, Hour, Minute, Second = self.JD2GL(JD)
        self._year = Year
        self._month = Month
        self._day = Day
        self._hour = Hour
        self._minute = Minute
        self._second = Second
        leapseconds = self.getGPSLeapSeconds()
        time = datetime.datetime(Year, Month, Day, Hour, Minute, Second)
        time = time + datetime.timedelta(seconds=-leapseconds)
        return time.year, time.month, time.day, time.hour, time.minute, time.second

    def UTC2GPSTime(self):
        Year = self._year
        Month = self._month
        Day = self._day
        Hour = self._hour
        Minute = self._minute
        Second = self._second
        leapseconds = self.getGPSLeapSeconds()
        time = datetime.datetime(Year, Month, Day, Hour, Minute, Second)
        time = time + datetime.timedelta(seconds=leapseconds)
        if time.month <= 2:
            time.year += 1
            time.month += 12
        JD = int(365.25 * time.year) + int(30.6001 * (time.month + 1)) + time.day + 1720981.5 + time.hour / 24.0 + \
            time.minute / 1440.0 + time.second / 86400.0
        gps_week, second_of_week = self.JD2GPSTime(JD)
        return gps_week, second_of_week

    def getGPSLeapSeconds(self):
        if self._year <= 2006 & self._month <= 1:
            raise ValueError("Don't know how many leap seconds to use before 2006")
        elif self._year <= 2009 & self._month <= 1:
            return 14
        elif self._year <= 2012 & self._month <= 7:
            return 15
        elif self._year <= 2015 & self._month <= 7:
            return 16
        elif self._year <= 2017 & self._month <= 1:
            return 17
        else:
            return 18

    """BD时 与 儒略历 的转换"""

    def BDTime2JD(self):
        JD = self._BDTimeWN * 7 + self._BDTimeSec / 86400 + 2453736.5
        return JD

    def JD2BDTime(self, JD):
        julday = int(JD)
        juldaySec = (JD - julday) * 60.0 * 60.0 * 24
        bd_week = int((JD - 2453736.5) / 7)
        second_of_week = round(((julday - 2453736) % 7 + (juldaySec / (60.0 * 60.0 * 24) - 0.5)) * 86400)
        # print(bd_week, second_of_week)
        return bd_week, second_of_week

    """BD时 与 UTC 的转换"""

    def BDTime2UTC(self):
        JD = self.BDTime2JD()
        Year, Month, Day, Hour, Minute, Second = self.JD2GL(JD)
        self._year = Year
        self._month = Month
        self._day = Day
        self._hour = Hour
        self._minute = Minute
        self._second = Second
        leapseconds = self.getBDLeapSeconds()
        time = datetime.datetime(Year, Month, Day, Hour, Minute, Second)
        time = time + datetime.timedelta(seconds=-leapseconds)
        return time.year, time.month, time.day, time.hour, time.minute, time.second

    def UTC2BDTime(self):
        Year = self._year
        Month = self._month
        Day = self._day
        Hour = self._hour
        Minute = self._minute
        Second = self._second
        leapseconds = self.getBDLeapSeconds()
        time = datetime.datetime(Year, Month, Day, Hour, Minute, Second)
        time = time + datetime.timedelta(seconds=leapseconds)
        if time.month <= 2:
            time.year += 1
            time.month += 12
        JD = int(365.25 * time.year) + int(30.6001 * (time.month + 1)) + time.day + 1720981.5 + time.hour / 24.0 + \
            time.minute / 1440.0 + time.second / 86400.0
        bd_week, second_of_week = self.JD2BDTime(JD)
        return bd_week, second_of_week

    def getBDLeapSeconds(self):
        if self._year <= 2006 & self._month <= 1:
            raise ValueError("BD Time started at 2006")
        elif self._year <= 2009 & self._month <= 1:
            return 0
        elif self._year <= 2012 & self._month <= 7:
            return 1
        elif self._year <= 2015 & self._month <= 7:
            return 2
        elif self._year <= 2017 & self._month <= 1:
            return 3
        else:
            return 4

if __name__ == "__main__":
    print("————————对比一下——————")
    timeT = TimeSystemChange(2006, 1, 1, 0, 0, 0)
    print(timeT.GL2JD())
    print(timeT.JD2BDTime(timeT.GL2JD()))

    timeT = TimeSystemChange(1980, 1, 6, 0, 0, 0)
    print(timeT.GL2JD())
    print(timeT.JD2GPSTime(timeT.GL2JD()))

    timeT = TimeSystemChange(2020, 7, 2, 12, 30, 30)
    print(timeT.UTC2GPSTime())
    print(timeT.UTC2BDTime())

