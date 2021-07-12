import pandas as pd
import numpy as np
import os
from tqdm import tqdm

'''
This analysis part is to filter the fuel station which are still in order.
We are going to iterate across all time series and check if the last date is in range
of the time scope end.
We want to write out the informations wether a fuel station is still in order and
do so as CSV-file representing a list of those gas stations with their related name.
The criterion is that an existing gas station related timeseries has an endtimepoint 
that is greater than the date '2019-01-01'
'''

names = []

cnt = 0
for fname in tqdm(os.listdir('../__DATA__/EXTRACTIONS_CSV')):
    name = fname.strip('.csv')
    
    df = pd.read_csv(os.path.join('../__DATA__/EXTRACTIONS_CSV', fname))
    df['date_time'] = pd.to_datetime(df['date_time'])

    #print(df['date_time'].tail(n=1))
    if df['date_time'].iloc[-1] > pd.to_datetime('2019-01-01'):
        pass
    else:
        #print(df['date_time'].iloc[-1])
        names.append(name)
    cnt += 1
    
    
    # if cnt == 1000:
        # break
        
        
df = pd.DataFrame({'name': names})

df.to_csv('./extant_petrol_stations.csv')