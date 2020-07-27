#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 计算百度地图API的SN值

@author: GanAH  2020/7/24.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import json
from urllib import parse, request
import hashlib

import requests

myAK = "WKoCFDIEVgwhtpk3geDBh9zOura8KhPO"
myNK = "LdqAIioVjerroI6AQ2xUZLxT0Cejrdzr"


def getJsonUrl(address):
    # 以get请求为例http://api.map.baidu.com/geocoding/v3/?address=百度大厦&output=json&ak=你的ak
    queryStr = '/geocoding/v3/?address={}&output=json&ak={}'.format(address, myAK)
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

    # 在最后直接追加上yoursk
    rawStr = encodedStr + myNK

    # 计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())

    # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    print(sn)
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")

    return url


def getLonLat(address):
    global r
    r = ''
    try:
        # 以get请求为例http://api.map.baidu.com/geocoding/v3/?address=百度大厦&output=json&ak=你的ak
        queryStr = '/geocoding/v3/?address={}&output=json&ak={}'.format(address, myAK)
        # queryStr = "http://api.map.baidu.com/reverhttp://api.map.baidu.com/telematics/v3/weather?location=foshan&output=json&WKoCFDIEVgwhtpk3geDBh9zOura8KhPO"

        # 对queryStr进行转码，safe内的保留字符不转换
        encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

        # 在最后直接追加上yoursk
        rawStr = encodedStr + myNK

        # 计算sn
        sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())

        # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
        # print(sn)
        url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
        r = requests.get(url)
        print(json.loads(r.text))
        jsonValue = json.loads(r.text)
        print("{}经度：{}°，纬度：{}°".format(address, jsonValue["result"]["location"]["lng"],
                                       jsonValue["result"]["location"]["lat"]))
        return jsonValue["result"]["location"]["lng"], jsonValue["result"]["location"]["lat"]
    except Exception as e:
        print(r, e.__str__())


def getlocation(lat, lng):
    # 31.809928, 102.537467, 3019.300
    # lat = '31.809928'
    # lng = '102.537467'
    # 以get请求为例http://api.map.baidu.com/geocoding/v3/?address=百度大厦&output=json&ak=你的ak

    queryStr = "/reverse_geocoding/v3/?ak={}&output=json&coordtype=wgs84ll&location={},{}".format(myAK, lat, lng)
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

    # 在最后直接追加上yoursk
    rawStr = encodedStr + myNK

    # 计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())

    # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    # url = 'http://api.map.baidu.com/geocoding/v3/?locati
    req = request.urlopen(url)  # json格式的返回数据
    res = req.read().decode("utf-8")  # 将其他编码的字符串解码成unicode
    return json.loads(res)


def getAddressInfo(lon, lat):
    str = getlocation(lat, lon)
    print(str)
    dictjson = {}  # 声明一个字典
    # get()获取json里面的数据
    jsonResult = str['result']
    address = jsonResult['addressComponent']
    # 国家
    country = address['country']
    # 国家编号（0：中国）
    country_code = address['country_code_iso']
    # 省
    province = address['province']
    # 城市
    city = address['city']
    # 城市等级
    city_level = address['city_level']
    # 县级
    district = address['district']
    # 把获取到的值，添加到字典里（添加）
    dictjson['country'] = country
    dictjson['country_code'] = country_code
    dictjson['province'] = province
    dictjson['city'] = city
    dictjson['city_level'] = city_level
    dictjson['district'] = district

    return dictjson


# lon, lat = getLonLat("武汉大学")
# print(getAddressInfo(lon, lat))
