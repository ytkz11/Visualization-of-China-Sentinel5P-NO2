# -*- coding: utf-8 -*-
# @Time    : 2021/6/25 10:59
'''
@author: ricardo_sakura
@date: 2021.4.21
@function: 生成想要的城市shp文件
'''

import geopandas
import requests
import json
import os

province_list = ['西藏自治区', '新疆维吾尔自治区', '甘肃省', '青海省', '四川省', '云南省', '广西壮族自治区', '贵州省', '重庆市', '陕西省',
                 '宁夏回族自治区', '内蒙古自治区', '山西省', '河南省', '湖北省', '湖南省', '广东省', '海南省', '台湾省', '福建省', '江西省',
                 '浙江省', '上海市', '安徽省', '江苏省', '山东省', '河北省', '天津市', '北京市', '辽宁省', '吉林省', '黑龙江省', '澳门特别行政区', '香港特别行政区']
province = {'西藏自治区': {'code': 540000, 'english': 'xizang'},
            '新疆维吾尔自治区': {'code': 650000, 'english': 'xinjiang'},
            '甘肃省': {'code': 620000, 'english': 'gansu'},
            '青海省': {'code': 630000, 'english': 'qinghai'},
            '四川省': {'code': 510000, 'english': 'sichuan'},
            '云南省': {'code': 530000, 'english': 'qinghai'},
            '广西壮族自治区': {'code': 450000, 'english': 'guangxi'},
            '贵州省': {'code': 520000, 'english': 'guizhou'},
            '重庆市': {'code': 500000, 'english': 'chongqin'},
            '陕西省': {'code': 610000, 'english': 'shaanxi'},
            '宁夏回族自治区': {'code': 640000, 'english': 'ningxia'},
            '内蒙古自治区': {'code': 150000, 'english': 'neimenggu'},
            '山西省': {'code': 140000, 'english': 'shanxi'},
            '河南省': {'code': 410000, 'english': 'henan'},
            '湖北省': {'code': 420000, 'english': 'hubei'},
            '湖南省': {'code': 430000, 'english': 'hunan'},
            '广东省': {'code': 440000, 'english': 'guangdong'},
            '海南省': {'code': 460000, 'english': 'hainan'},
            '台湾省': {'code': 710000, 'english': 'taiwan'},
            '福建省': {'code': 350000, 'english': 'fujian'},
            '江西省': {'code': 360000, 'english': 'jiangxi'},
            '浙江省': {'code': 330000, 'english': 'zhejiang'},
            '上海市': {'code': 310000, 'english': 'shanghai'},
            '安徽省': {'code': 340000, 'english': 'qinghai'},
            '江苏省': {'code': 320000, 'english': 'jiangsu'},
            '山东省': {'code': 370000, 'english': 'shandong'},
            '河北省': {'code': 130000, 'english': 'hebei'},
            '天津市': {'code': 120000, 'english': 'tianjin'},
            '北京市': {'code': 110000, 'english': 'beijing'},
            '辽宁省': {'code': 210000, 'english': 'liaoning'},
            '吉林省': {'code': 220000, 'english': 'jilin'},
            '黑龙江省': {'code': 230000, 'english': 'heilongjiang'},
            '澳门特别行政区': {'code': 820000, 'english': 'aomen'},
            '香港特别行政区': {'code': 810000, 'english': 'xianggang'},
            }

district_url = 'https://restapi.amap.com/v3/config/district?keywords={city}&key={api_key}'
geo_json_url = 'https://geo.datav.aliyun.com/areas/bound/{city_code}_full.json'
api_key = None  # 配置高德地图API KEY
path = None


def get_district_code(city, api_key):
    url = district_url.format(city=city, api_key=api_key)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)
    return result["districts"][0]["adcode"]


def download_geojson(city, city_code):
    file_path = os.path.join(path, city + '.json')
    if os.path.exists(file_path):
        print('Reading from local files...')
        with open(file_path, 'r') as f:
            result = json.load(f)
    else:
        print('Downloading from website...')
        url = geo_json_url.format(city_code=city_code)
        response = requests.get(url)
        result = json.loads(response.text)
        with open(file_path, 'w') as f:
            json.dump(result, f, indent=4)
    return result


def generate_shape(city, name, outpath):
    file_name = os.path.join(path, city + '.json')
    shp_file_path = os.path.join(outpath, name + '.shp')
    try:
        data = geopandas.read_file(file_name)
        localPath = str(shp_file_path)
        data.to_file(localPath, driver='ESRI Shapefile', encoding='gbk')
        print(f"{city}shp文件生成成功")
        print(f"文件存储在：{os.path.join(outpath, name + '.shp')}")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    path = 'E:\china-shapefiles-master\province'
    out_shp_path = r'E:\china-shapefiles-master\province\shp'
    if os.path.exists(out_shp_path) == 0:
        os.mkdir(out_shp_path)


    for i in range(len(province)):
        city = province_list[i]
        if api_key is None:
            city_code = province[city]['code']
        else:
            city_code = get_district_code(city, api_key)

        download_geojson(city, city_code)
        generate_shape(city, province[city]['english'], out_shp_path)
