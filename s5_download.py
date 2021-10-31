from sentinel5dl import search, download

# Search for Sentinel-5 products
'7.8 49.3,13.4 49.3,13.4 52.8,7.8 52.8,7.8 49.3'
'80.15625000000003 47.279229002570844,130.078125 51.17934297928926,132.1875 21.28937435586043,111.44531249999997 12.554563528593647,88.59374999999999 25.482951175355296,79.80468749999997 47.5172006978394'
result = search(
        polygon='POLYGON((7.8 49.30000000000001,13.399999999999999 49.30000000000001,13.399999999999999 52.80000000000004,7.8 52.80000000000004,7.8 49.30000000000001))',
        begin_ts='2021-07-18T00:00:00.000Z',
        end_ts='2021-07-18T23:59:59.999Z',
        product='L2__NO2___',
        processing_level='L2',
        processing_mode='Near real time')

# Download found products to the local folder
test_outpath = r'F:\my_gui\sentinel5p\test'
download(result.get('products'), test_outpath)