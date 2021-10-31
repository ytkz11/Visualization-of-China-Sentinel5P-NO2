# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 16:56
import datetime
import json
from requests import Session
from requests.auth import HTTPBasicAuth
import time


#Products constants
OZONE_TOTAL = 'L2__O3____'
OZONE_TROPOSPHIRIC = 'L2__O3_TCL'
OZONE_PROFILE = 'L2__O3__PR'
OZONE_TROPOSPHIRIC_PROFILE = 'L2__O3_TPR'
NITROGEN_DIOXIDE = 'L2__NO2___'
SULFAR_DIOXIDE = 'L2__SO2___'
CARBON_MONOXID = 'L2__CO____'
METHANE = 'L2__CH4___'
FORMALDEHYDE = 'L2__HCHO__'


def s5_quarry(days = '', wkt = '', product_type = '', ingestion_date_FROM = '', ingestion_date_TO = '', full_response = False ):
    login = 's5pguest'
    password = 's5pguest'

    quarry = ''
    #Setting up payload for auth
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    payload = {"login_username": 's5pguest',
               "login_password": 's5pguest'}

    #Auth
    with Session() as s:
        s.post('https://s5phub.copernicus.eu/dhus////login', data = payload, auth=HTTPBasicAuth(login, password), headers = headers)
        # Performing quarry depending on parameters

        #Quarring data for last X days
        if days != '':
            days = int(days) * -1
            ingestion_date_TO = datetime.datetime.now()
            ingestion_date_FROM = ingestion_date_TO + datetime.timedelta(days)
            ingestion_date_TO = str(ingestion_date_TO.date())
            ingestion_date_FROM = str(ingestion_date_FROM.date())

            #Quaring data intersecting the WKT object
        '''
        https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20footprint:%22Intersects(POLYGON((85.95280241129068%2043.18650535330309,119.36302793328738%2042.13659362743459,125.07417759516719%2035.46913658316771,119.07747045019343%2020.9348221528751,108.79740105880981%2020.13258590671309,83.0972275803508%2034.297939612206335,85.95280241129068%2043.18650535330309,85.95280241129068%2043.18650535330309)))%22)%20AND%20(%20beginPosition:[2021-07-28T00:00:00.000Z%20TO%202021-07-28T23:59:59.999Z]%20AND%20endPosition:[2021-07-28T00:00:00.000Z%20TO%202021-07-28T23:59:59.999Z]%20)%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:L2__NO2___%20AND%20processinglevel:L2%20AND%20processingmode:Near%20real%20time))&offset=0&limit=25&sortedby=ingestiondate&order=desc
        '''
        #     if wkt != '':
        #         #Quarring specific product type data
        #         if product_type != '':
        #             quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=' + \
        #                      '(%20footprint:%22Intersects(' + wkt + \
        #                      ')%22)%20AND%20' + '(%20ingestionDate:[' + ingestion_date_FROM + \
        #                      'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
        #                      'T23:59:59.999Z%20]%20)' + \
        #                      '%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:' + product_type + \
        #                      '))' + '&offset=0&limit=25&sortedby=ingestiondate&order=desc'
        #         #Quarring all data products
        #         else:
        #             quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter='\
        #                      + '(%20footprint:%22Intersects(' + wkt + \
        #                      ')%22)%20AND%20' + '(%20ingestionDate:[' + ingestion_date_FROM + \
        #                      'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
        #                      'T23:59:59.999Z%20]%20)&offset=0&limit=25&sortedby=ingestiondate&order=desc'
        #     #Quarring data
        #     else:
        #         #Quarring specific product type data
        #         if product_type != '':
        #             quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20ingestionDate:['\
        #                      + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
        #                      'T23:59:59.999Z%20]%20)' + '%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:'\
        #                      + product_type + '))' + '&offset=0&limit=25&sortedby=ingestiondate&order=desc'
        #         # Quarring all data products
        #         else:
        #             quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20ingestionDate:['\
        #                      + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
        #                      'T23:59:59.999Z%20]%20)&offset=0&limit=25&sortedby=ingestiondate&order=desc'
        #
        # else:
        #
        #     if wkt != '':
        #         if product_type != '':
        #                     # 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20footprint:%22Intersects(POLYGON((85.95280241129068%2043.18650535330309,119.36302793328738%2042.13659362743459,125.07417759516719%2035.46913658316771,119.07747045019343%2020.9348221528751,108.79740105880981%2020.13258590671309,83.0972275803508%2034.297939612206335,85.95280241129068%2043.18650535330309,85.95280241129068%2043.18650535330309)))%22)%20AND%20(%20beginPosition:[2021-07-28T00:00:00.000Z%20TO%202021-07-28T23:59:59.999Z]%20AND%20endPosition:[2021-07-28T00:00:00.000Z%20TO%202021-07-28T23:59:59.999Z]%20)%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:L2__NO2___%20AND%20processinglevel:L2%20AND%20processingmode:Near%20real%20time))&offset=0&limit=25&sortedby=ingestiondate&order=desc'
        #             quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=' + \
        #                      '(%20footprint:%22Intersects(' + wkt + ')%22)%20AND%20' + '(%20ingestionDate:['\
        #                      + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
        #                      'T23:59:59.999Z%20]%20)' + '%20AND%20(%20%20(platformname:Sentinel-5%20AND%20timeliness:Nearrealtime%20AND%20'+\
        #                      'producttype:' + product_type + '%20AND%20processinglevel:L2%20AND%20processingmode:Near%20real%20time))' + '&offset=0&limit=25&sortedby=ingestiondate&order=desc'
        #             quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter= (%20footprint:%22Intersects(POLYGON((85.95280241129068%2043.18650535330309,119.36302793328738%2042.13659362743459,125.07417759516719%2035.46913658316771,119.07747045019343%2020.9348221528751,108.79740105880981%2020.13258590671309,83.0972275803508%2034.297939612206335,85.95280241129068%2043.18650535330309,85.95280241129068%2043.18650535330309)))%22)%20AND%20(%20beginPosition:[2021-07-28T00:00:00.000Z%20TO%202021-07-28T23:59:59.999Z]%20AND%20endPosition:[2021-07-28T00:00:00.000Z%20TO%202021-07-28T23:59:59.999Z]%20)%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:L2__NO2___%20AND%20processinglevel:L2%20AND%20processingmode:Near%20real%20time))&offset=0&limit=25&sortedby=ingestiondate&order=desc'
        #
        #         else:
        #             quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=' + \
        #                      '(%20footprint:%22Intersects(' + wkt + ')%22)%20AND%20' + \
        #                      '(%20ingestionDate:[' + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
        #                      'T23:59:59.999Z%20]%20)&offset=0&limit=25&sortedby=ingestiondate&order=desc'
        #     else:
        #         if product_type != '':
        #             quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20ingestionDate:['\
        #                      + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20'\
        #                      + ingestion_date_TO + 'T23:59:59.999Z%20]%20)' + \
        #                      '%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:' + product_type + \
        #                      '))' + '&offset=0&limit=25&sortedby=ingestiondate&order=desc'
        #         else:
        #             quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20ingestionDate:['\
        #                      + ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + ingestion_date_TO + \
        #                      'T23:59:59.999Z%20]%20)&offset=0&limit=25&sortedby=ingestiondate&order=desc'

        quarry = 'https://s5phub.copernicus.eu/dhus/api/stub/products?filter=(%20footprint:%22Intersects(POLYGON((85.95280241129068%2043.18650535330309,119.36302793328738%2042.13659362743459,125.07417759516719%2035.46913658316771,119.07747045019343%2020.9348221528751,108.79740105880981%2020.13258590671309,83.0972275803508%2034.297939612206335,85.95280241129068%2043.18650535330309,85.95280241129068%2043.18650535330309)))%22)%20AND%20(%'+ \
                 '20beginPosition:['+ingestion_date_FROM +'T00:00:00.000Z%20TO%20' + \
                                    ingestion_date_TO+ 'T23:59:59.999Z]%20' + \
                 'AND%20endPosition:[' +ingestion_date_FROM + 'T00:00:00.000Z%20TO%20' + \
                                    ingestion_date_TO+ 'T23:59:59.999Z]%20)' + \
                 '%20AND%20(%20%20(platformname:Sentinel-5%20AND%20producttype:'+product_type + \
                 '%20AND%20processinglevel:L2%20AND%20processingmode:Near%20real%20time))&offset=0&limit=25&sortedby=ingestiondate&order=desc'


        r = s.get(quarry, headers=headers)
        resp = json.loads(r.text)

        if full_response == False:
            products = []
            for p in resp['products']:
                product = {
                    'identifier': p['identifier'],
                    'uuid': p['uuid'],
                    'date': p['summary'][0][7:-14]
                }
                products.append(product)
            return products

        else:
            return resp



def download_product(uuid, output_path):

    url = "https://s5phub.copernicus.eu/dhus/odata/v1/Products('" + str(uuid) + "')/$value"

    login = 's5pguest'
    password = 's5pguest'
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }
    # Setting up payload for auth
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.'
                      '4'
                      '389.128 Safari/537.36'}
    payload = {"login_username": 's5pguest',
               "login_password": 's5pguest'}

    # Downloading file auth request
    with Session() as s:
        s.post('https://s5phub.copernicus.eu/dhus////login', data=payload, auth=HTTPBasicAuth(login, password),
               headers=headers)
        r = s.get(url, headers=headers, proxies=proxies)
        filname = r.headers['Content-Disposition'][17:-1]

        with open(output_path + filname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    print('Downloading...')
if __name__ == '__main__':
    # data = s5_quarry(days=5, full_response=True)
    time_start = time.time()
    boundary = 'POLYGON((85.95280241129068%2043.18650535330309,119.36302793328738%2042.13659362743459,125.07417759516719%2035.46913658316771,119.07747045019343%2020.9348221528751,108.79740105880981%2020.13258590671309,83.0972275803508%2034.297939612206335,85.95280241129068%2043.18650535330309,85.95280241129068%2043.18650535330309))'
    quarry = s5_quarry(ingestion_date_FROM='2021-07-28', ingestion_date_TO='2021-07-28', product_type=NITROGEN_DIOXIDE,full_response = True)
    uuid_list = quarry['products']
    print('ready download')

    for i in range(len(uuid_list)):
        uuid = uuid_list[i]['uuid']
        print('download', uuid)
        download_product(uuid, 'F:\\my_gui\\sentinel5p\\test\\')
        print('done')
    time_end = time.time()

    print(time_end- time_start)

    a =1