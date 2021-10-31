# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 16:01
from scipy.interpolate import griddata
from netCDF4 import Dataset
import numpy as np
from matplotlib.colors import LogNorm


import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# Array rotation
def flip90_left(arr):
    new_arr = np.transpose(arr)
    new_arr = new_arr[::-1]
    return new_arr

# Output three columns of data, followed by longitude, latitude, no2
def Arranged_In_Three_Columns(data1, data2, data3):
    # 降维
    d1 = data1.flatten()
    d2 = data2.flatten()
    d3 = data3.flatten()

    # Converted to column form
    dd1 = d1[:, np.newaxis]
    dd2 = d2[:, np.newaxis]
    dd3 = d3[:, np.newaxis]

    data4 = np.c_[dd1, dd2, dd3]

    # Remove the rows where nan exists, and filter the data
    data5 = np.delete(data4, np.where(np.isnan(data4))[0], axis=0)

    return data5

def data(file):
    fh = Dataset(file, mode='r')
    lon = fh.groups['PRODUCT'].variables['longitude'][:][0, :, :]
    lat = fh.groups['PRODUCT'].variables['latitude'][:][0, :, :]
    no2 = fh.groups['PRODUCT'].variables['nitrogendioxide_tropospheric_column_precision'][0, :, :]
    no2_units = fh.groups['PRODUCT'].variables['nitrogendioxide_tropospheric_column_precision'].units
    # lon = np.array(lon)
    # lat = np.array(lat)
    # no2 = np.array(no2)

    return lon, lat, no2, no2_units
def merge_data(list_file):
    # a = np.zeros()
    lon = []
    lat = []
    no2 = []
    three_data_lon_lat_no2 = []


    for file in list_file:
        a1, b1, c1, no2_units = data(file)
        d1 = Arranged_In_Three_Columns(a1, b1, c1)
        d1 = np.array(d1)
        lon.append(a1)
        lat.append(b1)
        no2.append(c1)
        three_data_lon_lat_no2.append(d1)

    return lon, lat, no2, three_data_lon_lat_no2, no2_units
def min_max_lon_lat(lon, lat, three_data_lon_lat_no2):
    n = len(lon)
    min_lon_list = []
    max_lon_list = []
    min_lat_list = []
    max_lat_list = []
    three_data_lon_lat_no2_list = []

    for i in range(len(lon)):
        min_lon_single = np.min(lon[i])
        max_lon_single = np.max(lon[i])

        min_lat_single = np.min(lat[i])
        max_lat_single = np.max(lat[i])

        min_lon_list.append(min_lon_single)
        max_lon_list.append(max_lon_single    )
        min_lat_list.append(min_lat_single)
        max_lat_list.append(max_lat_single)

    min_lon = np.min([min_lon_list])
    max_lon = np.max([max_lon_list])
    min_lat = np.min([min_lat_list])
    max_lat = np.max([max_lat_list])

    # 0615 There are currently only 4 files, and it may increase to five in the future (adding Nanhai)
    total_three_data_lon_lat_no2 = np.r_[three_data_lon_lat_no2[0],three_data_lon_lat_no2[1],three_data_lon_lat_no2[2],three_data_lon_lat_no2[3]]

    return min_lon, max_lon, min_lat, max_lat, total_three_data_lon_lat_no2

def linear_process(list_file):
    lon, lat, no2, three, no2_units = merge_data(list_file)
    min_lon, max_lon, min_lat, max_lat, total_three_data_lon_lat_no2 = min_max_lon_lat(lon, lat, three)
    lat = np.linspace(min_lat, max_lat, 2000)
    lon = np.linspace(min_lon, max_lon, 2000)
    [lat1, lon1] = np.meshgrid(lat, lon)
    inter_mat = griddata(total_three_data_lon_lat_no2[:, 0:2], total_three_data_lon_lat_no2[:, 2] * 1000000, (lon1, lat1), method='linear')
    inter_mat = np.where(inter_mat > 300, np.nan, inter_mat/1000000)
    basemap_show(lon1, lat1, inter_mat, no2_units)

def basemap_show(lon1,lat1,data, no2_units):
    m = Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45,
                lon_0=100)
    m.readshapefile("E:\my_gui\sentinel5p\china-shapefiles-master\shapefiles\china", 'china', drawbounds=True)
    xi, yi = m(lon1, lat1)

    # Plot Data

    cs1 = m.pcolor(xi, yi, np.squeeze(data), norm=LogNorm(), cmap='jet', shading='auto')
    # m.pcolor(x2, y2, np.squeeze(c2), norm=LogNorm(), cmap='jet')
    # m.pcolor(x3,y3,np.squeeze(c3),norm=LogNorm(), cmap='jet')
    # m.pcolor(x4, y4, np.squeeze(c4),norm=LogNorm(), cmap='jet')

    # Add Grid Lines
    m.drawparallels(np.arange(-80., 81., 10.), labels=[1, 0, 0, 0], fontsize=10)
    m.drawmeridians(np.arange(-180., 181., 10.), labels=[0, 0, 0, 1], fontsize=10)

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    m.etopo(scale=0.2)
    # Add Colorbar
    cbar = m.colorbar(cs1, location='bottom', pad="10%")

    cbar.set_label(no2_units)

    # Add Title
    plt.title('N O2 in atmosphere')
    plt.savefig('2.png')
    plt.show()


if __name__ == '__main__':
    my_example_nc_file1 = r'E:\my_gui\sentinel5p\S5P_NRTI_L2__NO2____20210607T065201_20210607T065701_18910_01_010400_20210607T073747.nc'
    my_example_nc_file2 = r'E:\my_gui\sentinel5p\S5P_NRTI_L2__NO2____20210607T065701_20210607T070201_18910_01_010400_20210607T073816.nc'
    my_example_nc_file3 = r'E:\my_gui\sentinel5p\S5P_NRTI_L2__NO2____20210607T051201_20210607T051701_18909_01_010400_20210607T055650.nc'
    my_example_nc_file4 = r'E:\my_gui\sentinel5p\S5P_NRTI_L2__NO2____20210607T051701_20210607T052201_18909_01_010400_20210607T055916.nc'

    list_file = [my_example_nc_file1,my_example_nc_file2, my_example_nc_file3, my_example_nc_file4]
    linear_process(list_file)
    a = 0
