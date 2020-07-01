#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 世界通用时间时间系统类

@author: GanAH  2019/11/27.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from database import database
from GNSS.timeSystem import GPSToUTC

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
    _MJD = None
    """
    # GPSTime
    """
    _GPSTimeWN = None
    _GPSTimeSec = None

    """
    # UTC
    """

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

    def GL2JD(self):
        if self._month <= 2:
            self._year = self._year - 1
            self._month = self._month + 12
        julday = int(365.25 * self._year) + int(
            30.6001 * (self._month + 1)) + self._day + 1720981.5 + self._hour / 24.0 + \
                 self._minute / 1440.0 + self._second / 86400.0

        # print(julday)
        return julday

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
        Second= int(60 * (60 * (24 * (JD + 0.5 - int(JD + 0.5)) - Hour)-Minute))
        return [Year, Month, Day, Hour, Minute, Second]

    def JD2GPST(self):
        gps_week = int((self._JD - 2444244.5) / 7)
        day_of_week = int((self._JD - 2444244.5) % 7)
        second_of_week = 24 * 60 * 60 * day_of_week + self._hour * 60 * 60 + self._minute * 60 + self._second
        # print(gps_week, day_of_week, second_of_week)
        return [gps_week, second_of_week]

    def GPSTimeToJD(self):
        return self._GPSTimeWN * 7 + self._GPSTimeSec / 86400 + 2444244.5

    def GPSTimeToUTC(self,GPST):
        UTC = GPST - GPSToUTC.get_leap_seconds(GPST)
        if self.UTCToGPSTime(UTC) - GPST != 0:
            return UTC + 1
        else:
            return UTC

    def UTCToGPSTime(self,UTC):
        GPST = UTC + GPSToUTC.get_leap_seconds(UTC)
        return GPST



if __name__ == "__main__":
    print("————————对比一下——————")
    lisT = [2010, 10, 20, 10, 20, 20]
    timeT = TimeSystemChange(2010, 10, 20, 10, 20, 20)
    print(timeT.GL2JD())
    # print(timeT.JD2GL(timeT.GL2JD()))
    timeT = TimeSystemChange(1606, 296420)
    print(timeT.GPSTimeToJD())

    timeT = TimeSystemChange(2455489.930787037)
    print(timeT.JD2GPST())


