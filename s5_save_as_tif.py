from netCDF4 import Dataset
import numpy as np
import netCDF4 as nc
from osgeo import gdal, osr, ogr
import os
import glob

from scipy.interpolate import griddata
import sentinel5p


# load data
def read(list_file):
    lon, lat, no2, three, no2_units = sentinel5p.merge_data(list_file)
    min_lon, max_lon, min_lat, max_lat, total_three_data_lon_lat_no2 = sentinel5p.min_max_lon_lat(lon, lat, three)
    lat = np.linspace(min_lat, max_lat, 2000)
    lon = np.linspace(min_lon, max_lon, 2000)
    [lat1, lon1] = np.meshgrid(lat, lon)
    inter_mat = griddata(total_three_data_lon_lat_no2[:, 0:2], total_three_data_lon_lat_no2[:, 2] * 1000000,
                         (lon1, lat1),
                         method='linear')
    inter_mat = np.where(inter_mat > 300, np.nan, inter_mat / 1000000)

    return lon1, lat1, inter_mat


def save_tif(lon, lat, inter_mat, Output_folder):
    lon = np.rot90(lon, 1)
    lat = np.rot90(lat, 1)
    inter_mat = np.rot90(inter_mat, 1)

    print('save as tif')
    LonMin, LatMax, LonMax, LatMin = [lon.min(), lat.max(), lon.max(), lat.min()]

    N_Lat = 2000

    N_Lon = 2000

    Lon_Res = (LonMax - LonMin) / (float(N_Lon) - 1)

    Lat_Res = (LatMax - LatMin) / (float(N_Lat) - 1)
    driver = gdal.GetDriverByName('GTiff')

    # out_tif_name = Output_folder + '\\'+ data.split('\\')[-1].split('.')[0] + '_' + str(i+1) + '.tif'
    out_tif_name = os.path.join(Output_folder, os.path.splitext(os.path.basename(list_file[0]))[0] + '.tif')
    # out_tif_name = os.path.join(Output_folder,'1.tif')
    out_tif = driver.Create(out_tif_name, N_Lon, N_Lat, 1, gdal.GDT_Float32)

    # 设置影像的显示范围

    # -Lat_Res一定要是-的

    geotransform = (lon[0][0], Lon_Res, 0, lat[0][0], 0, -Lat_Res)

    out_tif.SetGeoTransform(geotransform)

    # 获取地理坐标系统信息，用于选取需要的地理坐标系统

    srs = osr.SpatialReference()

    srs.ImportFromEPSG(4326)  # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]

    out_tif.SetProjection(srs.ExportToWkt())  # 给新建图层赋予投影信息

    # 数据写出

    out_tif.GetRasterBand(1).WriteArray(inter_mat)  # 将数据写入内存，此时没有写入硬盘

    out_tif.FlushCache()  # 将数据写入硬盘

    out_tif = None  # 注意必须关闭tif文件

def main(list_file, out):
    lon, lat, inter_mat = read(list_file)
    save_tif(lon, lat, inter_mat, out)


if __name__ == '__main__':
    my_example_nc_file1 = r'Y:\my_gui\sentinel5p\S5P_NRTI_L2__NO2____20210607T065201_20210607T065701_18910_01_010400_20210607T073747.nc'
    my_example_nc_file2 = r'Y:\my_gui\sentinel5p\S5P_NRTI_L2__NO2____20210607T065701_20210607T070201_18910_01_010400_20210607T073816.nc'
    my_example_nc_file3 = r'Y:\my_gui\sentinel5p\S5P_NRTI_L2__NO2____20210607T051201_20210607T051701_18909_01_010400_20210607T055650.nc'
    my_example_nc_file4 = r'Y:\my_gui\sentinel5p\S5P_NRTI_L2__NO2____20210607T051701_20210607T052201_18909_01_010400_20210607T055916.nc'

    list_file = [my_example_nc_file1, my_example_nc_file2, my_example_nc_file3, my_example_nc_file4]
    
    
    Output_folder = os.path.join(os.path.dirname(my_example_nc_file1),'out')
    if os.path.exists(Output_folder) == 0:
        os.mkdir(Output_folder)
        
    main(list_file, Output_folder)
    a = 0
