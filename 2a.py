from datetime import timedelta

import pandas as pd
# import xlwt
# import xlrd

jeftini_senzori_data = pd.read_csv('./data/jeftini_senzori.TXT', sep=';', usecols=[1, 2, 4, 5, 8], skip_blank_lines=True, names=['date', 'time', 'temp', 'humind', 'pm2'])
jeftini_senzori_data['date'] = jeftini_senzori_data['date'] + ' ' + jeftini_senzori_data['time']
jeftini_senzori_data['date'] = pd.to_datetime(jeftini_senzori_data['date']).dt.strftime('%d-%m-%y %H:%M:%S')
jeftini_senzori_data.drop('time', axis='columns', inplace=True)

# print(jeftini_senzori_data)

skupi_senzori_data = pd.read_csv('./data/skupi_senzori.XLS', sep='\t', skiprows=4, skipfooter=6, usecols=[0, 1, 2, 3, 6])

skupi_senzori_data['date beginning'] = skupi_senzori_data['date beginning'] + ' ' + skupi_senzori_data['time beginning']
skupi_senzori_data['date beginning'] = pd.to_datetime(skupi_senzori_data['date beginning']).dt.strftime('%d-%m-%y %H:%M:%S')
skupi_senzori_data['date beginning'] = pd.to_datetime(skupi_senzori_data['date beginning']) + pd.DateOffset(hours=-2)
# skupi_senzori_data['date beginning'].dt.DateOffset(hours=-2)
skupi_senzori_data.drop('time beginning', axis='columns', inplace=True)

skupi_senzori_data['date end'] = skupi_senzori_data['date end'] + ' ' + skupi_senzori_data['time end']
skupi_senzori_data['date end'] = pd.to_datetime(skupi_senzori_data['date end']).dt.strftime('%d-%m-%y %H:%M:%S')
skupi_senzori_data['date end'] = pd.to_datetime(skupi_senzori_data['date end']) + pd.DateOffset(hours=-2)
skupi_senzori_data.drop('time end', axis='columns', inplace=True)

print(skupi_senzori_data)

# jeftini_senzori_data.to_excel('./data/2aa.xls', index=False, header=False)
