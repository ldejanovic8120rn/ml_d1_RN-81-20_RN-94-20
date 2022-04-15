from datetime import timedelta

import pandas as pd
import numpy as np
# import xlwt
# import xlrd

jeftini_senzori_data = pd.read_csv('./data/jeftini_senzori.TXT', sep=';', usecols=[1, 2, 4, 5, 8], skip_blank_lines=True, names=['date', 'time', 'temp', 'humind', 'pm2'])
jeftini_senzori_data['date'] = jeftini_senzori_data['date'] + ' ' + jeftini_senzori_data['time']
jeftini_senzori_data['date'] = pd.to_datetime(jeftini_senzori_data['date']).dt.strftime('%m-%d-%y %H:%M:%S')
jeftini_senzori_data['date'] = pd.to_datetime(jeftini_senzori_data['date']) + pd.DateOffset(hours=0)
jeftini_senzori_data.drop('time', axis='columns', inplace=True)

# print(jeftini_senzori_data)

skupi_senzori_data = pd.read_csv('./data/skupi_senzori.XLS', sep='\t', skiprows=4, skipfooter=6, usecols=[0, 1, 2, 3, 6])

skupi_senzori_data['date beginning'] = skupi_senzori_data['date beginning'] + ' ' + skupi_senzori_data['time beginning']
skupi_senzori_data['date beginning'] = pd.to_datetime(skupi_senzori_data['date beginning']).dt.strftime('%d-%m-%y %H:%M:%S')
skupi_senzori_data['date beginning'] = pd.to_datetime(skupi_senzori_data['date beginning']) + pd.DateOffset(hours=-2)
skupi_senzori_data.drop('time beginning', axis='columns', inplace=True)

skupi_senzori_data['date end'] = skupi_senzori_data['date end'] + ' ' + skupi_senzori_data['time end']
skupi_senzori_data['date end'] = pd.to_datetime(skupi_senzori_data['date end']).dt.strftime('%d-%m-%y %H:%M:%S')
skupi_senzori_data['date end'] = pd.to_datetime(skupi_senzori_data['date end']) + pd.DateOffset(hours=-2)
skupi_senzori_data.drop('time end', axis='columns', inplace=True)

for index, row in skupi_senzori_data.iterrows():
    result = jeftini_senzori_data[np.logical_and(row['date beginning'] <= jeftini_senzori_data['date'], jeftini_senzori_data['date'] < row['date end'])]
    print(result)

# print('FOR')
# for index, row in skupi_senzori_data.iterrows():
#     print(jeftini_senzori_data[row['date beginning'] <= jeftini_senzori_data['date']])


# print(skupi_senzori_data)

# df = pd.DataFrame(columns=['date', 'temp', 'humind', 'pm2', 'date beginning', 'date end', 'reference pm2'])
# cnt = 0
# for index_j, row_j in jeftini_senzori_data.iterrows():
#     for index_s, row_s in skupi_senzori_data.iterrows():
#         if row_s['date beginning'] <= row_j['date'] <= row_s['date end']:
#             df.loc[cnt] = [row_j['date'], row_j['temp'], row_j['humind'], row_j['pm2'], row_s['date beginning'], row_s['date end'], row_s['PM2.5_ambient - #11']]
#             cnt += 1
#             print(df)

# jeftini_senzori_data.to_excel('./data/2aa.xls', index=False, header=False)
