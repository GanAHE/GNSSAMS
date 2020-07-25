#!usr/bin/env python
# -*- coding: utf-8 -*-
from arcgis.gis import GIS
from arcgis.mapping import WebMap
gis = GIS()
webmap = gis.content.get('41281c51f9de45edaf1c8ed44bb10e30')
webmap

la_parks_trails = WebMap(webmap)
la_parks_trails