from datetime import timedelta

import pandas as pd
import numpy as np
# import xlwt
# import xlrd

jeftini_senzori_data = pd.read_csv('./data/jeftini_senzori.TXT', sep=';', usecols=[1, 2, 4, 5, 8], skip_blank_lines=True, names=['date', 'time', 'temp', 'humid', 'pm2'])
jeftini_senzori_data['date'] = jeftini_senzori_data['date'] + ' ' + jeftini_senzori_data['time']
jeftini_senzori_data['date'] = pd.to_datetime(jeftini_senzori_data['date']).dt.strftime('%m-%d-%y %H:%M:%S')
jeftini_senzori_data['date'] = pd.to_datetime(jeftini_senzori_data['date']) + pd.DateOffset(hours=0)
jeftini_senzori_data.drop('time', axis='columns', inplace=True)

skupi_senzori_data = pd.read_csv('./data/skupi_senzori.XLS', sep='\t', skiprows=4, skipfooter=6, usecols=[0, 1, 2, 3, 6])

skupi_senzori_data['date beginning'] = skupi_senzori_data['date beginning'] + ' ' + skupi_senzori_data['time beginning']
skupi_senzori_data['date beginning'] = pd.to_datetime(skupi_senzori_data['date beginning']).dt.strftime('%d-%m-%y %H:%M:%S')
skupi_senzori_data['date beginning'] = pd.to_datetime(skupi_senzori_data['date beginning']) + pd.DateOffset(hours=-2)
skupi_senzori_data.drop('time beginning', axis='columns', inplace=True)

skupi_senzori_data['date end'] = skupi_senzori_data['date end'] + ' ' + skupi_senzori_data['time end']
skupi_senzori_data['date end'] = pd.to_datetime(skupi_senzori_data['date end']).dt.strftime('%d-%m-%y %H:%M:%S')
skupi_senzori_data['date end'] = pd.to_datetime(skupi_senzori_data['date end']) + pd.DateOffset(hours=-2)
skupi_senzori_data.drop('time end', axis='columns', inplace=True)

df = pd.DataFrame(columns=['date', 'temp', 'humid', 'pm2', 'date beginning', 'date end', 'reference pm2'])
cnt = 0
for index, row in skupi_senzori_data.iterrows():
    result = jeftini_senzori_data[np.logical_and(row['date beginning'] <= jeftini_senzori_data['date'], jeftini_senzori_data['date'] < row['date end'])]
    if result.empty:
        continue

    for indx, r in result.iterrows():
        df.loc[cnt] = [r['date'], r['temp'], r['humid'], r['pm2'], row['date beginning'], row['date end'], row['PM2.5_ambient - #11']]
        cnt += 1

df['reference pm2'] = df['reference pm2'].str.replace(',', '.')
df.to_csv('./2a.xls', index=False, header=True, encoding="utf-8", sep="\t")
