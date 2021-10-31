# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 16:05
from scipy.interpolate import griddata
from netCDF4 import Dataset
import numpy as np
from matplotlib.colors import LogNorm


import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def data(file):
    fh = Dataset(file, mode='r')
    lon = fh.groups['PRODUCT'].variables['longitude'][:][0, :, :]
    lat = fh.groups['PRODUCT'].variables['latitude'][:][0, :, :]
    no2 = fh.groups['PRODUCT'].variables['nitrogendioxide_tropospheric_column_precision'][0, :, :]
    no2_units = fh.groups['PRODUCT'].variables['nitrogendioxide_tropospheric_column_precision'].units
    return lon, lat, no2, no2_units
def origin_show(lons, lats, no2):

    import matplotlib.pyplot as plt
    # plt.scatter(lons, lats, tmax, c= 'red')
    # plt.show()

    plt.figure()
    plt.pcolor(lons, lats, no2, cmap='hot')
    plt.show()
def basemap_show(lon1,lat1,data, no2_units):
    lon1 = lon1.mean()
    lat1 = lat1.mean()
    m = Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45,
                lon_0=100)
    m.readshapefile("E:\china-shapefiles-master\shapefiles\china", 'china', drawbounds=True)
    xi, yi = m(lon1, lat1)

    # Plot Data
    # cs = m.pcolor(xi, yi, np.squeeze(no2), norm=LogNorm(), cmap='jet')
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
    # plt.savefig('2.png')
    plt.show()
if __name__ == '__main__':
    my_example_nc_file1 = r'F:\my_gui\sentinel5p\test\S5P_NRTI_L2__NO2____20210721T113737_20210721T114237_19537_02_020200_20210721T124127.nc'

    a1, b1, c1, no2_units = data(my_example_nc_file1)
    origin_show( a1, b1, c1)
    basemap_show(a1, b1, c1, no2_units)
    a = 0