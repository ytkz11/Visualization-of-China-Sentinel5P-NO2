Visualization of No2 air pollution data in Sentinel 5P China

If it helps you, please click Star.

- [x] Visualization of China region

- [x] Conversion from NC to TIF

- [x] Automatically downloads data

- [x] Provincial numerical visualization

![Rp26rd.png](https://z3.ax1x.com/2021/06/18/Rp26rd.png)

**sentinel5p.py**

Possible bugs, and repair methods:

<font color="**#28B9CF**"> Cause </font> : The vector SHP file for the Chinese region is missing.

< font color = # A9DFBF > repair < / font > : download the SHP to local China area: https://github.com/ytkz11/china-shapefiles

After unzipping the file, <font color="#EC49A7">"E: china-shapefiles-master shapefiles\ China ",</font><font color="#EC49A7"> 'china'</font>, drawbounds=True)



## Provincial numerical visualization

A province SHP file cutting, extraction results as shown below. Take Shandong Province for example.

[![WfmAFH.png](https://z3.ax1x.com/2021/07/26/WfmAFH.png)





Because many online SHPS are made abroad, some sensitive areas are missing, such as southern Tibet and Taiwan Province. The investigation found that Autonavi provided vector data in China

