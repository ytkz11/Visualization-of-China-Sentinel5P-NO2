# -*- coding: utf-8 -*-
# @Time    : 2021/6/25 10:02
from osgeo import gdal
import numpy as np
import shapefile
import fiona
import shapefile
from matplotlib.path import Path
import geopandas
import os

path = None  # 定义存放路径


def clip_raster(tiffile, shpfile):

    from osgeo import gdal, ogr
    options = gdal.WarpOptions(cutlineDSName=shpfile,cropToCutline=True)
    outBand = gdal.Warp(srcDSOrSrcDSTab=tiffile,
                        destNameOrDestDS=r'F:\my_gui\test\out\out.tif',
                        options=options)
    OutTile = None

if __name__ == '__main__':
    file = r'F:\my_gui\test\out\S5P_NRTI_L2__NO2____20210607T065201_20210607T065701_18910_01_010400_20210607T073747.tif'
    city = '广东省'  # json文件名
 # 存放路径
    path = r'E:\china-shapefiles-master\province\shp\shandong.shp'
    clip_raster(file, path)



