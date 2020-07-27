#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: GNSS文件读取类
<p> obsFile function reads the observation file
navigationFile function reads the navigation file
sp3File function reads the SP3 file
clockFile function reads the clock file
...
@author: GanAH  2020/7/2.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""

import os
import time
import datetime
import numpy as np
import pandas as pd
from GNSS.file.checkif import (isfloat, isint)
from GNSS.file.constants import _system_name
from GNSS.file.save import Observation, Navigation, PEphemeris, _ObservationTypes


def read_navFile(navigationFile):
    """
    读取导航电文
    :param navigationFile:
    :return:
    """
    start = time.time()
    f = open(navigationFile)
    nav = f.readlines()
    line = 0
    version = None
    alphaList = None
    betaList = None
    while True:
        if 'RINEX VERSION / TYPE' in nav[line]:
            version = nav[line][0:-21].split()[0]
            line += 1
        if 'ION ALPHA' in nav[line]:
            alphaList = nav[line][0:55].split()
            line += 1
        if 'ION BETA' in nav[line]:
            betaList = nav[line][0:55].split()
            line += 1
        elif 'END OF HEADER' in nav[line]:
            line += 1
            break
        else:
            line += 1
    del nav[0:line]
    nav = [lines.replace('D', 'E') for lines in nav]
    nav = [lines.replace('E ', 'E0') for lines in nav]
    nav = [lines.replace('0-', '0 -') for lines in nav]
    nav = [lines.replace('1-', '1 -') for lines in nav]
    nav = [lines.replace('2-', '2 -') for lines in nav]
    nav = [lines.replace('3-', '3 -') for lines in nav]
    nav = [lines.replace('4-', '4 -') for lines in nav]
    nav = [lines.replace('5-', '5 -') for lines in nav]
    nav = [lines.replace('6-', '6 -') for lines in nav]
    nav = [lines.replace('7-', '7 -') for lines in nav]
    nav = [lines.replace('8-', '8 -') for lines in nav]
    nav = [lines.replace('9-', '9 -') for lines in nav]
    nav = [lines.split() for lines in nav]
    ephemeris_list = []
    svList = []
    PRN_old = "X00"
    epoch_old = datetime.datetime.now()
    while True:
        # --------------------------------------------------------------
        GPS = GLONASS = GALILEO = COMPASS = SBAS = False
        PRN = nav[0][0]
        if "G" in PRN:
            GPS = True
        elif "R" in PRN:
            GLONASS = True
        elif "E" in PRN:
            GALILEO = True
        elif "C" in PRN:
            COMPASS = True
        elif "J" in PRN:
            QZSS = True
        elif "I" in PRN:
            IRSS = True
        elif "S" in PRN:
            SBAS = True
        else:
            if len(PRN) == 1:
                PRN = 'G0' + PRN
            elif len(PRN) == 2:
                PRN = 'G' + PRN

        if len(nav[0][1]) == 2:
            year = int(nav[0][1])
            if 79 < year < 100:
                year += 1900
            elif year <= 79:
                year += 2000
            else:
                # 自动触发异常
                raise Warning('Navigation year is not recognized! | Program stopped!')
        else:
            year = int(nav[0][1])
        month, day, hour, minute, second = int(nav[0][2]), int(nav[0][3]), int(nav[0][4]), int(nav[0][5]), int(float(nav[0][6]))
        epoch = datetime.datetime(year=year,
                                  month=month,
                                  day=day,
                                  hour=hour,
                                  minute=minute,
                                  second=second)
        # --------------------------------------------------------------
        clockBias = nav[0][7]
        clockDrift = nav[0][8]
        clockDriftRate = nav[0][9]
        if GLONASS or SBAS:
            x, vx, ax = float(nav[1][0]), float(nav[1][1]), float(nav[1][2])
            y, vy, ay = float(nav[2][0]), float(nav[2][1]), float(nav[2][2])
            z, vz, az = float(nav[3][0]), float(nav[3][1]), float(nav[3][2])
            health = float(nav[1][3])
            freqNumber = float(nav[2][3])
            operationDay = float(nav[3][3])
            sqrtA, toe, m0, e, delta_n, smallomega, cus, cuc, crs, crc, cis, cic, idot, i0, bigomega0, bigomegadot = [np.nan for _ in range(16)]
            if PRN == PRN_old and epoch == epoch_old:
                ephemeris_list[-1] = [PRN, epoch, clockBias, clockDrift,
                                      clockDriftRate, sqrtA, toe, m0, e, delta_n,
                                      smallomega, cus, cuc, crs, crc, cis, cic,
                                      idot, i0, bigomega0, bigomegadot,
                                      x, y, z, vx, vy, vz, ax, ay, az,
                                      health, freqNumber, operationDay]
            else:
                svList.append(PRN)
                ephemeris_list.append([PRN, epoch, clockBias, clockDrift,
                                       clockDriftRate, sqrtA, toe, m0, e, delta_n,
                                       smallomega, cus, cuc, crs, crc, cis, cic,
                                       idot, i0, bigomega0, bigomegadot,
                                       x, y, z, vx, vy, vz, ax, ay, az,
                                       health, freqNumber, operationDay])
            del nav[0:4]
        else:
            e = float(nav[2][1])
            m0 = float(nav[1][3])
            i0 = float(nav[4][0])
            toe = float(nav[3][0])
            cus = float(nav[2][2])
            cuc = float(nav[2][0])
            crs = float(nav[1][1])
            crc = float(nav[4][1])
            cis = float(nav[3][3])
            cic = float(nav[3][1])
            idot = float(nav[5][0])
            sqrtA = float(nav[2][3])
            delta_n = float(nav[1][2])
            smallomega = float(nav[4][2])
            bigomega0 = float(nav[3][2])
            bigomegadot = float(nav[4][3])
            x, y, z, vx, vy, vz, ax, ay, az, health, freqNumber, operationDay = [np.nan for _ in range(12)]
            if PRN == PRN_old and epoch == epoch_old:
                ephemeris_list[-1] = [PRN, epoch, clockBias, clockDrift,
                                      clockDriftRate, sqrtA, toe, m0, e, delta_n,
                                      smallomega, cus, cuc, crs, crc, cis, cic,
                                      idot, i0, bigomega0, bigomegadot,
                                      x, y, z, vx, vy, vz, ax, ay, az,
                                      health, freqNumber, operationDay]
            else:
                svList.append(PRN)
                ephemeris_list.append([PRN, epoch, clockBias, clockDrift,
                                       clockDriftRate, sqrtA, toe, m0, e, delta_n,
                                       smallomega, cus, cuc, crs, crc, cis, cic,
                                       idot, i0, bigomega0, bigomegadot,
                                       x, y, z, vx, vy, vz, ax, ay, az,
                                       health, freqNumber, operationDay])
            del nav[0:8]
        PRN_old = PRN
        epoch_old = epoch
        if len(nav) == 0:
            break
    columnNames = ["SV", "Epoch", "clockBias", "clockDrift", "clockDriftRate", "sqrtA", "toe", "m0", "eccentricity",
                   "delta_n","smallomega", "cus", "cuc", "crs", "crc", "cis", "cic",
                   "idot", "i0", "bigomega0", "bigomegadot",
                   "x", "y", "z", "vx", "vy", "vz", "ax", "ay", "az",
                   "health", "freqNumber", "operationDay"]
    ephemeris = pd.DataFrame(ephemeris_list, index=svList, columns=columnNames)
    ephemeris.index.name = 'SV'
    ephemeris["epoch"] = ephemeris.Epoch
    ephemeris.set_index('Epoch', append=True, inplace=True)
    ephemeris = ephemeris.reorder_levels(['Epoch', 'SV'])
    ephemeris = ephemeris.drop(["SV"], axis=1)

    fileEpoch = datetime.date(year=year,
                              month=month,
                              day=day)
    f.close()  # close the file
    finish = time.time()  # Time of finish
    print("Navigation file ", navigationFile, " is read in", "{0:.2f}".format(finish - start), "seconds.")
    return Navigation(fileEpoch, ephemeris, version, alphaList, betaList)


def read_obsFile(observationFile):
    """
    观测文件
    :param observationFile: 观测文件路径
    :return:
    """
    if observationFile.endswith(".Z") == True:
        raise Warning(
            "All I/O functions take uncompressed files as an input (remove .Z/.gz from filename) | Next release will include this feature...")
    # check if observationFile exists or not
    # isexist(observationFile)
    # open file
    f = open(observationFile, errors='ignore')
    obsLines = f.readlines()
    line = 0
    while True:
        if 'RINEX VERSION / TYPE' in obsLines[line]:
            version = obsLines[line][0:-20].split()[0]
            break
        else:
            line += 1
    if version.startswith("2"):
        return read_obsFile_v2(observationFile)
    elif version.startswith("3"):
        return read_obsFile_v3(observationFile)


def read_obsFile_v2(observationFile):
    """
    读取2代版本观测数据
    :param observationFile: 文件路径
    :return: Observation's object
    """
    start = time.time()
    f = open(observationFile, errors='ignore')
    obsLines = f.readlines()

    line = 0
    version = None
    ToB = []
    approx_position = None
    receiver_type = None
    antenna_type = None
    while True:
        if 'RINEX VERSION / TYPE' in obsLines[line]:
            version = obsLines[line][0:-21].split()[0]
            line += 1
        elif 'MARKER NAME' in obsLines[line]:
            stationName = obsLines[line][0:-20].split()[0]
            line += 1
        elif 'REC # / TYPE / VERS' in obsLines[line]:
            receiver_type = obsLines[line][0:-20].split()
            line += 1
        elif 'ANT # / TYPE' in obsLines[line]:
            antenna_type = obsLines[line][0:-20].split()
            line += 1
        elif 'APPROX POSITION XYZ' in obsLines[line]:
            approx_position = obsLines[line][0:obsLines[line].index('A')].split()
            approx_position = [float(i) for i in approx_position]
            line += 1
        elif 'TYPES OF OBSERV' in obsLines[line]:
            ToB.extend(obsLines[line][0:obsLines[line].index('#')].split())
            obsNumber = int(ToB[0])
            line += 1
        elif 'END OF HEADER' in obsLines[line]:
            line += 1
            break
        else:
            line += 1

    del obsLines[0:line]
    # --------------------------------------------------------------------------------------
    obsLines = [lines.rstrip() for lines in obsLines]
    obsList = []
    SVList = []
    epochList = []
    obsNumber = None
    while True:
        # --------------------------------------------------------------------------------------
        while True:
            if 'COMMENT' in obsLines[0]:
                del obsLines[0]
                line += 1
            elif 'APPROX POSITION XYZ' in obsLines[0]:
                del obsLines[0]
                line += 1
            elif 'REC # / TYPE / VERS' in obsLines[0]:
                raise Warning("Receiver type is changed! | Exiting...")
            elif isint(obsLines[0][1:3]) == False:
                print("Line", line, ":", obsLines[0])  # bu satırı sil!!!!
                del obsLines[0]
                line += 1
                print('Unexpected format between epochs! Line', line, 'is deleted!')
            else:
                break
        # ---------------------------------------------------------------------------------------
        year = int(obsLines[0][1:3])
        if 79 < year < 100:
            year += 1900
        elif year <= 79:
            year += 2000
        else:
            raise Warning('Observation year is not recognized! | Program stopped!')
        epoch = datetime.datetime(year=year,
                                  month=int(obsLines[0][4:6]),
                                  day=int(obsLines[0][7:9]),
                                  hour=int(obsLines[0][10:12]),
                                  minute=int(obsLines[0][13:15]),
                                  second=int(obsLines[0][16:18]) if isint(obsLines[0][16:18]) == True else 0)
        epochList.append(epoch)
        eflag = int(obsLines[0][27:29])
        if eflag != 0:
            del obsLines[0]
            while True:
                if 'COMMENT' in obsLines[0]:
                    print(obsLines[0])
                    del obsLines[0]
                    line += 1
                else:
                    break

        if len(obsLines[0]) == 80:
            receiver_clock = float(obsLines[0][-12:])
            obsLines[0] = obsLines[0][:-12]
        else:
            receiver_clock = 0
        # ---------------------------------------------------------------------------------------
        NoSV = int(obsLines[0][30:32])
        # ---------------------------------------------------------------------------------------
        if len(obsLines[0][32:]) != 3 * NoSV:
            noLine = [int(NoSV / 12) if NoSV % 12 != 0 else int(NoSV / 12) - 1]
            for i in range(noLine[0]):
                obsLines[0] = obsLines[0] + obsLines[1][32:]
                del obsLines[1]
            if len(obsLines[0][32:]) != 3 * NoSV:
                obsLines[0] = " " + obsLines[0].strip()
        # ---------------------------------------------------------------------------------------
        SV = [obsLines[0][32:][i:i + 3] for i in range(0, len(obsLines[0][32:]), 3)]
        SV = [i.replace('  ', 'G0') for i in SV]
        SV = [i.replace(' ', 'G') if i[0] == ' ' else i.replace(' ', '0') for i in SV]
        SVList.extend(SV)
        # ---------------------------------------------------------------------------------------
        obsEpoch = []
        del obsLines[0]
        rowNumber = np.ceil(obsNumber / 5).astype('int')
        for i in range(0, rowNumber * NoSV, rowNumber):
            for j in range(0, rowNumber):
                lineLenght = len(obsLines[i + j])
                if lineLenght != 80:
                    obsLines[i + j] += ' ' * (80 - lineLenght)
                if j != 0:
                    obsLines[i] += obsLines[i + j]
            obsLines[i] = [float(obsLines[i][j:j + 14]) if isfloat(obsLines[i][j:j + 14]) == True else None for j in
                           range(0, 80 * rowNumber, 16)]
            if len(obsLines[i]) != obsNumber:
                del obsLines[i][-(len(obsLines[i]) - obsNumber):]
            obsLines[i].append(epoch)
            obsEpoch.append(obsLines[i])
        obsList.extend(obsEpoch)
        del obsLines[0:rowNumber * NoSV]
        if len(obsLines) == 0:
            break
    columnNames = ToB[1:]
    columnNames.append('Epoch')
    observation = pd.DataFrame(obsList, index=SVList, columns=columnNames)
    observation.index.name = 'SV'
    observation['epoch'] = observation.Epoch
    observation['Epoch'] = observation.Epoch
    observation.set_index('Epoch', append=True, inplace=True)
    observation = observation.reorder_levels(['Epoch', 'SV'])

    observation["SYSTEM"] = _system_name(observation.index.get_level_values("SV"))
    # ---------------------------------------------------------------------------------------
    fileEpoch = datetime.date(year=epoch.year,
                              month=epoch.month,
                              day=epoch.day)
    if len(epochList) == 1:
        interval = 30
    else:
        interval = epochList[1] - epochList[0]
        interval = interval.seconds
    f.close()  # close the file
    # ---------------------------------------------------------------------------------------
    finish = time.time()
    print("Observation file ", observationFile, " is read in", "{0:.2f}".format(finish - start), "seconds.")
    return Observation(f.name, fileEpoch, observation, approx_position, receiver_type, antenna_type, interval,
                       receiver_clock, version, ToB, stationName)


def read_obsFile_v3(obsFileName):
    """
    读取3代版本观测数据
    :param observationFile: 文件路径
    :return: Observation's object
    """
    global epoch, approx_position, receiver_type, antenna_type, version
    start = time.time()  # Time of start

    if obsFileName.endswith("crx"): obsFileName = obsFileName.split(".")[0] + ".rnx"
    f = open(obsFileName, errors='ignore')  # open file
    obsLines = f.readlines()  # read lines
    # =============================================================================

    line = 0
    ToB_GPS, ToB_GLONASS, ToB_GALILEO, ToB_COMPASS, ToB_QZSS, ToB_IRSS, ToB_SBAS = [], [], [], [], [], [], []
    while True:
        if 'RINEX VERSION / TYPE' in obsLines[line]:
            version = obsLines[line][0:-21].split()[0]
            line += 1
        elif 'MARKER NAME' in obsLines[line]:
            stationName = obsLines[line][0:-20].split()[0]
            line += 1
        elif 'REC # / TYPE / VERS' in obsLines[line]:
            receiver_type = obsLines[line][0:-20].split()
            line += 1
        elif 'ANT # / TYPE' in obsLines[line]:
            antenna_type = obsLines[line][0:-20].split()
            line += 1
        elif 'APPROX POSITION XYZ' in obsLines[line]:
            approx_position = obsLines[line][0:obsLines[line].index('A')].split()
            approx_position = [float(i) for i in approx_position]
            line += 1
        elif 'SYS / # / OBS TYPES' in obsLines[line]:
            if obsLines[line][0] == "G":  # GPS
                obsTypes = obsLines[line][0:obsLines[line].index('SYS')].split()
                obsNumber_GPS = int(obsTypes[1])
                ToB_GPS = obsTypes[2:]
                line += 1
                if obsNumber_GPS > 13:
                    for _ in range(int(np.ceil(obsNumber_GPS / 13)) - 1):
                        ToB_GPS.extend(obsLines[line][0:obsLines[line].index('SYS')].split())
                        line += 1
            elif obsLines[line][0] == "R":  # GLONASS
                obsTypes = obsLines[line][0:obsLines[line].index('SYS')].split()
                obsNumber_GLONASS = int(obsTypes[1])
                ToB_GLONASS = obsTypes[2:]
                line += 1
                if obsNumber_GLONASS > 13:
                    for _ in range(int(np.ceil(obsNumber_GLONASS / 13)) - 1):
                        ToB_GLONASS.extend(obsLines[line][0:obsLines[line].index('SYS')].split())
                        line += 1
            elif obsLines[line][0] == "E":  # GALILEO
                obsTypes = obsLines[line][0:obsLines[line].index('SYS')].split()
                obsNumber_GALILEO = int(obsTypes[1])
                ToB_GALILEO = obsTypes[2:]
                line += 1
                if obsNumber_GALILEO > 13:
                    for _ in range(int(np.ceil(obsNumber_GALILEO / 13)) - 1):
                        ToB_GALILEO.extend(obsLines[line][0:obsLines[line].index('SYS')].split())
                        line += 1
            elif obsLines[line][0] == "C":  # COMPASS
                obsTypes = obsLines[line][0:obsLines[line].index('SYS')].split()
                obsNumber_COMPASS = int(obsTypes[1])
                ToB_COMPASS = obsTypes[2:]
                line += 1
                if obsNumber_COMPASS > 13:
                    for _ in range(int(np.ceil(obsNumber_COMPASS / 13)) - 1):
                        ToB_COMPASS.extend(obsLines[line][0:obsLines[line].index('SYS')].split())
                        line += 1
            elif obsLines[line][0] == "J":  # QZSS
                obsTypes = obsLines[line][0:obsLines[line].index('SYS')].split()
                obsNumber_QZSS = int(obsTypes[1])
                ToB_QZSS = obsTypes[2:]
                line += 1
                if obsNumber_QZSS > 13:
                    for _ in range(int(np.ceil(obsNumber_QZSS / 13)) - 1):
                        ToB_QZSS.extend(obsLines[line][0:obsLines[line].index('SYS')].split())
                        line += 1
            elif obsLines[line][0] == "I":  # IRSS
                obsTypes = obsLines[line][0:obsLines[line].index('SYS')].split()
                obsNumber_IRSS = int(obsTypes[1])
                ToB_IRSS = obsTypes[2:]
                line += 1
                if obsNumber_IRSS > 13:
                    for _ in range(int(np.ceil(obsNumber_IRSS / 13)) - 1):
                        ToB_IRSS.extend(obsLines[line][0:obsLines[line].index('SYS')].split())
                        line += 1
            elif obsLines[line][0] == "S":  # SBAS
                obsTypes = obsLines[line][0:obsLines[line].index('SYS')].split()
                obsNumber_SBAS = int(obsTypes[1])
                ToB_SBAS = obsTypes[2:]
                line += 1
                if obsNumber_SBAS > 13:
                    for _ in range(int(np.ceil(obsNumber_SBAS / 13)) - 1):
                        ToB_SBAS.extend(obsLines[line][0:obsLines[line].index('SYS')].split())
                        line += 1
        elif 'END OF HEADER' in obsLines[line]:
            line += 1
            break
        else:
            line += 1
    del obsLines[0:line]
    # =============================================================================
    # Type of Observations in RINEX File
    ToB = np.unique(np.concatenate((ToB_GPS, ToB_GLONASS, ToB_GALILEO, ToB_COMPASS, ToB_QZSS, ToB_IRSS, ToB_SBAS)))
    # Indices of each satellite constellation in ToB
    index_GPS = np.searchsorted(ToB, ToB_GPS)
    index_GLONASS = np.searchsorted(ToB, ToB_GLONASS)
    index_GALILEO = np.searchsorted(ToB, ToB_GALILEO)
    index_COMPASS = np.searchsorted(ToB, ToB_COMPASS)
    index_QZSS = np.searchsorted(ToB, ToB_QZSS)
    index_IRSS = np.searchsorted(ToB, ToB_IRSS)
    index_SBAS = np.searchsorted(ToB, ToB_SBAS)
    observation_types = _ObservationTypes(ToB_GPS, ToB_GLONASS, ToB_GALILEO, ToB_COMPASS, ToB_QZSS, ToB_IRSS, ToB_SBAS)
    # =============================================================================
    obsLines = [lines.rstrip() for lines in obsLines]
    obsList = []
    svList = []
    epochList = []
    while True:
        # =============================================================================
        while True:
            if 'COMMENT' in obsLines[0]:
                del obsLines[0]
                line += 1
            elif 'APPROX POSITION XYZ' in obsLines[0]:
                del obsLines[0]
                line += 1
            elif 'REC # / TYPE / VERS' in obsLines[0]:
                raise Warning("Receiver type is changed! | Exiting...")
            else:
                break
        # =============================================================================
        if obsLines[0][0] == ">":
            epochLine = obsLines[0][1:].split()
            if len(epochLine) == 8:
                epoch_year, epoch_month, epoch_day, epoch_hour, epoch_minute, epoch_second, epoch_flag, epoch_SVNumber = \
                    obsLines[0][1:].split()
                receiver_clock = 0
            elif len(epochLine) == 9:
                epoch_year, epoch_month, epoch_day, epoch_hour, epoch_minute, epoch_second, epoch_flag, epoch_SVNumber, receiver_clock = \
                    obsLines[0][1:].split()
            else:
                raise Warning("Unexpected epoch line format detected! | Program stopped!")
        else:
            raise Warning("Unexpected format detected! | Program stopped!")
        # =========================================================================
        if epoch_flag in {"1", "3", "5", "6"}:
            raise Warning("Deal with this later!")
        elif epoch_flag == "4":
            del obsLines[0]
            while True:
                if 'COMMENT' in obsLines[0]:
                    print(obsLines[0])
                    del obsLines[0]
                    line += 1
                elif 'SYS / PHASE SHIFT' in obsLines[0]:
                    del obsLines[0]
                    # line += 1
                else:
                    break
        else:
            # =========================================================================
            epoch = datetime.datetime(year=int(epoch_year),
                                      month=int(epoch_month),
                                      day=int(epoch_day),
                                      hour=int(epoch_hour),
                                      minute=int(epoch_minute),
                                      second=int(float(epoch_second)))
            epochList.append(epoch)
            del obsLines[0]  # delete epoch header line
            # =============================================================================
            epoch_SVNumber = int(epoch_SVNumber)
            for j in range(epoch_SVNumber):
                obsEpoch = np.full((1, len(ToB)), None)
                if len(obsLines) >= epoch_SVNumber:
                    svList.append(obsLines[j][:3])
                    if obsLines[j].startswith("G"):
                        obsEpoch[0, index_GPS] = np.array([[float(obsLines[j][3:][i:i + 14]) if isfloat(
                            obsLines[j][3:][i:i + 14]) == True else None for i in range(0, len(ToB_GPS) * 16, 16)]])
                    elif obsLines[j].startswith("R"):
                        obsEpoch[0, index_GLONASS] = np.array([[float(obsLines[j][3:][i:i + 14]) if isfloat(
                            obsLines[j][3:][i:i + 14]) == True else None for i in
                                                                range(0, len(ToB_GLONASS) * 16, 16)]])
                    elif obsLines[j].startswith("E"):
                        obsEpoch[0, index_GALILEO] = np.array([[float(obsLines[j][3:][i:i + 14]) if isfloat(
                            obsLines[j][3:][i:i + 14]) == True else None for i in
                                                                range(0, len(ToB_GALILEO) * 16, 16)]])
                    elif obsLines[j].startswith("C"):
                        obsEpoch[0, index_COMPASS] = np.array([[float(obsLines[j][3:][i:i + 14]) if isfloat(
                            obsLines[j][3:][i:i + 14]) == True else None for i in
                                                                range(0, len(ToB_COMPASS) * 16, 16)]])
                    elif obsLines[j].startswith("J"):
                        obsEpoch[0, index_QZSS] = np.array([[float(obsLines[j][3:][i:i + 14]) if isfloat(
                            obsLines[j][3:][i:i + 14]) == True else None for i in range(0, len(ToB_QZSS) * 16, 16)]])
                    elif obsLines[j].startswith("I"):
                        obsEpoch[0, index_IRSS] = np.array([[float(obsLines[j][3:][i:i + 14]) if isfloat(
                            obsLines[j][3:][i:i + 14]) == True else None for i in range(0, len(ToB_IRSS) * 16, 16)]])
                    elif obsLines[j].startswith("S"):
                        obsEpoch[0, index_SBAS] = np.array([[float(obsLines[j][3:][i:i + 14]) if isfloat(
                            obsLines[j][3:][i:i + 14]) == True else None for i in range(0, len(ToB_SBAS) * 16, 16)]])
                    obsEpoch = np.append(obsEpoch, epoch)
                    obsList.append(obsEpoch)
                else:
                    break
            # =============================================================================
            del obsLines[0:epoch_SVNumber]  # number of rows in epoch equals number of visible satellites in RINEX 3
        if len(obsLines) == 0:
            break
    # =============================================================================
    columnNames = np.append(ToB, 'Epoch')
    obs = pd.DataFrame(obsList, index=svList, columns=columnNames)
    obs.index.name = 'SV'
    obs['epoch'] = obs.Epoch
    obs['Epoch'] = obs.Epoch
    obs.set_index('Epoch', append=True, inplace=True)
    obs = obs.reorder_levels(['Epoch', 'SV'])
    obs["SYSTEM"] = _system_name(obs.index.get_level_values("SV"))
    # =============================================================================
    fileEpoch = datetime.datetime(year=epoch.year,
                              month=epoch.month,
                              day=epoch.day,
                                  hour=epoch.hour,
                                  minute = epoch.minute,
                                  second=epoch.second)
    if len(epochList) == 1:
        interval = 30
    else:
        interval = epochList[1] - epochList[0]
        interval = interval.seconds
    f.close()  # close the file
    # =============================================================================
    finish = time.time()  # Time of finish
    print("Observation file ", obsFileName, " is read in", "{0:.2f}".format(finish - start), "seconds.")
    return Observation(f.name, fileEpoch, obs, approx_position, receiver_type, antenna_type, interval, receiver_clock,
                       version, observation_types, stationName)


def read_sp3File(sp3file):
    """
    读取SP3精密星历文件
    :param sp3file: 文件路径
    :return: SP3 object
    """
    global epoch
    start = time.time()
    # isexist(sp3file)
    f = open(sp3file)
    sp3 = f.readlines()
    line = 0
    search = '/*'
    SVNo = sp3[2].split()[1]

    while True:
        if search in sp3[line]:
            if search in sp3[line + 1]:
                line += 1
            else:
                line += 1
                break
        else:
            line += 1
    del sp3[0:line]
    sp3 = [i.replace('P  ', 'PG0') for i in sp3]
    sp3 = [i.replace('P ', 'PG') for i in sp3]
    header = ['X', 'Y', 'Z', 'deltaT', 'sigmaX', 'sigmaY', 'sigmaZ', 'sigmadeltaT', 'Epoch']
    sat, pos = [], []
    while True:
        for i in range(int(SVNo) + 1):
            if '*' in sp3[i]:
                sp3[i] = sp3[i].split()
                epoch = datetime.datetime(year=int(sp3[i][1]),
                                          month=int(sp3[i][2]),
                                          day=int(sp3[i][3]),
                                          hour=int(sp3[i][4]),
                                          minute=int(sp3[i][5]),
                                          second=0)
            else:
                if '999999.999999' in sp3[i]:
                    sp3[i] = sp3[i].replace(' 999999.999999', '          None')
                else:
                    if sp3[i][60:].isspace() == True:
                        sp3[i] = sp3[i][:60]
                    if sp3[i][60:63].isspace() == True:
                        sp3[i] = sp3[i][:60] + " XX" + sp3[i][63:]
                    if sp3[i][63:66].isspace() == True:
                        sp3[i] = sp3[i][:63] + " XX" + sp3[i][66:]
                    if sp3[i][66:69].isspace() == True:
                        sp3[i] = sp3[i][:66] + " XX" + sp3[i][69:]
                    if sp3[i][69:73].isspace() == True:
                        sp3[i] = sp3[i][:69] + "  XX" + sp3[i][73:]
                        # -------------------------------------------
                sp3[i] = sp3[i].split()
                if len(sp3[i][1:]) == 4:
                    sp3[i].extend(['None', 'None', 'None', 'None'])
                sat.append(sp3[i][0][1:])
                sp3[i] = [float(j) if isfloat(j) == True else None for j in sp3[i]]
                sp3[i].append(epoch)
                pos.append(sp3[i][1:])
        del sp3[0:int(SVNo) + 1]
        if 'EOF' in sp3[0]:
            break
    position = pd.DataFrame(pos, index=sat, columns=header)
    position.index.name = 'SV'
    position.set_index('Epoch', append=True, inplace=True)
    position = position.reorder_levels(["Epoch", "SV"])
    f.close()  # close the file
    # ------------------------------------------------------------------
    end = time.time()
    print('{}'.format(sp3file), 'file is read in', '{0:.2f}'.format(end - start), 'seconds')
    return PEphemeris(epoch, position)


def read_clockFile(clkFile):
    """
    读取钟文件
    :param clkFile:
    :return:
    """
    # isexist(clkFile)
    start = time.time()
    f = open(clkFile)
    clk = f.readlines()
    line = 0
    prnlist = []
    while True:
        if 'OF SOLN SATS' not in clk[line]:
            del clk[line]
        else:
            noprn = int(clk[line][4:6])
            line += 1
            break
    while True:
        if 'PRN LIST' in clk[line]:
            prnlist.extend(clk[line])
            prnlist = ''.join(prnlist)
            prnlist = prnlist.split()
            prnlist.remove('PRN')
            prnlist.remove('LIST')
            line += 1
        else:
            break
    SV = []
    for a in range(0, len(prnlist[0]), 3):
        SV.extend([prnlist[0][a:a + 3]])

    if len(prnlist) > 1:
        SV.extend(prnlist[1:])

    line = 0
    while True:
        if 'END OF HEADER' not in clk[line]:
            line += 1
        else:
            del clk[0:line + 1]
            break

    timelist = []
    for i in range(len(clk)):
        if clk[i][0:2] == 'AS':
            timelist.append(clk[i].split())
    Sat = []
    Epochlist = []
    SVtime = []
    for i in range(len(timelist)):
        Sat.append(timelist[i][1])
        Epochlist.append((datetime.datetime(year=int(timelist[i][2]), month=int(timelist[i][3]),
                                            day=int(timelist[i][4]), hour=int(timelist[i][5]),
                                            minute=int(timelist[i][6]), second=int(float(timelist[i][7])))))
        SVtime.append(float(timelist[i][9]))
    SVTimelist = pd.DataFrame(list(zip(Epochlist, SVtime)), index=Sat,
                              columns=['Epoch', 'DeltaTSV'])
    f.close()  # close the file
    end = time.time()
    print('{}'.format(clkFile), 'file is read in', '{0:.2f}'.format(end - start), 'seconds')
    return SVTimelist


def read_ionFile(IonFile):
    """
    读取气象文件
    :param IonFile: 文件路径
    :return:
    """
    # check if observationFile exists or not
    # isexist(IonFile)
    # ----------------------------------------------
    start = time.time()
    f = open(IonFile, errors='ignore')
    obsLines = f.readlines()

    line = 0
    while True:
        if 'END OF HEADER' in obsLines[line]:
            line += 1
            break
        else:
            line += 1

    del obsLines[0:line]
    # --------------------------------------------------------------------------------------
    tecuList = np.zeros([13, 71, 72])
    for etime in range(13):
        line = 0
        del obsLines[0]  # start of tec map
        epochLine = obsLines[0].split()
        epoch = datetime.datetime(year=int(epochLine[0]), month=int(epochLine[1]), day=int(epochLine[2]),
                                  hour=int(epochLine[3]), minute=int(epochLine[4]), second=int(epochLine[5]))
        del obsLines[0]  # delete epoch line
        for phi in range(71):
            temp = obsLines[0].split()
            LAT, LON1, LON2, DLON, H = temp[0], temp[1], temp[2], temp[3], temp[4]
            tecu = obsLines[1] + obsLines[2] + obsLines[3] + obsLines[4] + obsLines[5]
            tecu = tecu.split()
            tecu = [int(tec) for tec in tecu]
            for lamda in range(len(tecu) - 1):
                tecuList[etime, phi, lamda] = tecu[lamda]
            del obsLines[0:6]
        del obsLines[0]
        # ---------------------------------------------------------------------------------------
    f.close()  # close the file
    finish = time.time()
    print("Ionosphere file ", IonFile, " is read in", "{0:.2f}".format(finish - start), "seconds.")
    return tecuList

if __name__ == "__main__":
    nav = read_navFile("C:/Users/97320/Desktop/brdc2020.20n")
    print(nav.navigation)
    print(nav.alphalist)
    print(nav.betalist)
    # pass
    # nav = read_navFile("./D068305A.19N")
    # print(nav.navigation)
    #
    # obs = read_obsFile("./D068305A.19O")
    # print(obs.observation)

