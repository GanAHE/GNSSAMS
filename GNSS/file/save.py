#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 数据结构存储

@author: GanAH  2020/7/2.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""


class Observation(object):
    """
    Observations class for RINEX Observation (*.*o) files
    """

    def __init__(self, filename=None, epoch=None, observation=None, approx_position=None,
                 receiver_type=None, antenna_type=None, interval=None,
                 receiver_clock=None, version=None, observation_types=None):
        self.filename = filename
        self.epoch = epoch
        self.observation = observation
        self.approx_position = approx_position
        self.receiver_type = receiver_type
        self.antenna_type = antenna_type
        self.interval = interval
        self.receiver_clock = receiver_clock
        self.version = version
        self.observation_types = observation_types


class _ObservationTypes:
    def __init__(self, ToB_GPS=None, ToB_GLONASS=None, ToB_GALILEO=None,
                 ToB_COMPASS=None, ToB_QZSS=None, ToB_IRSS=None, ToB_SBAS=None):
        self.GPS = ToB_GPS
        self.GLONASS = ToB_GLONASS
        self.GALILEO = ToB_GALILEO
        self.COMPASS = ToB_COMPASS
        self.QZSS = ToB_QZSS
        self.IRSS = ToB_IRSS
        self.SBAS = ToB_SBAS


class Navigation(object):
    """
    Navigation class for RINEX Observation (*.*n/p) files
    """

    def __init__(self, epoch=None, navigation=None, version=None, alphalist=None, betalist=None):
        self.epoch = epoch
        self.navigation = navigation
        self.version = version
        self.alphalist = alphalist
        self.betalist = betalist


class Navigation_DEPRECATED(object):
    """
    Broadcast Ephemeris in RINEX file
    """

    def __init__(self, PRN=None, epoch=None, roota=None, toe=None,
                 m0=None, e=None, delta_n=None, smallomega=None,
                 cus=None, cuc=None, crs=None, crc=None, cis=None,
                 cic=None, idot=None, i0=None, bigomega0=None,
                 bigomegadot=None):
        self.PRN = PRN
        self.epoch = epoch
        self.roota = roota
        self.toe = toe
        self.m0 = m0
        self.e = e
        self.delta_n = delta_n
        self.smallomega = smallomega
        self.cus = cus
        self.cuc = cuc
        self.crs = crs
        self.crc = crc
        self.cis = cis
        self.cic = cic
        self.idot = idot
        self.i0 = i0
        self.bigomega0 = bigomega0
        self.bigomegadot = bigomegadot


class PEphemeris(object):
    """
    Class definition for SP3 file (Precise Ephemeris)
    """

    def __init__(self, epoch=None, ephemeris=None):
        self.epoch = epoch
        self.ephemeris = ephemeris
