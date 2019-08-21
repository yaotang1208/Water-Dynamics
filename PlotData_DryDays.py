# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:53:58 2019

@author: yaotang
"""

import sys
import os
import logging
# import datetime
import numpy as np
import numexpr
import csv
import statsmodels.api as sm
import pandas as pd



import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import gridspec


from dateutil.parser import parse
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
from matplotlib import cm

register_matplotlib_converters()

df_Met = pd.read_pickle('Met_2012_2017.pkl')

Time_Met = [datetime.strptime(str(i),'%Y%m%d%H%M') for i in df_Met['TIMESTAMP_START']]

#%%
# in a certain time range
Time_Start = pd.Timestamp('2015-7-1')
Time_End = pd.Timestamp('2016-1-1')

Start = Time_Met.index(Time_Start)
End = Time_Met.index(Time_End)

df_Met_1 = df_Met.iloc[Start:End]

Rain_Index = [];
for count,ele in enumerate(df_Met_1['P_1']):
    if ele>0:
        Rain_Index.append(count)

for count,ele in enumerate(df_Met_1['P_2']):
    if ele>0:
        Rain_Index.append(count)

Time_Rain = df_Met_1['TIMESTAMP_START'].iloc[Rain_Index]

Days = [str(i)[:8] for i in df_Met_1['TIMESTAMP_START']]
Days_Rain = [str(i)[:8] for i in Time_Rain]

Days = list(dict.fromkeys(Days))
Days_Rain = list(dict.fromkeys(Days_Rain))
Dry_Days = []
for i in Days:
    if i not in Days_Rain:
        Dry_Days.append(i)


print(Dry_Days)

with open('Dry_Days.csv','w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(Dry_Days)

csvFile.close()

#plt.figure()
#ax1 = plt.subplot(3,1,1)
#plt.plot(Time_Met,df_Met['P_1'],Time_Met,df_Met['P_2'])
#plt.ylim(0,80)
#plt.legend(('k34','T1'),loc = 'upper right')
#plt.xlim(Time_Start, Time_End)
#plt.ylabel('PREC (mm/30min)')
#
#plt.subplot(3,1,2,sharex = ax1)
#plt.plot(Time_Met,df_Met['SW_IN'])
#plt.ylabel('SW_IN (W/m2)')
#
#plt.subplot(3,1,3,sharex = ax1)
#plt.plot(Time_Met,df_Met['LW_IN'])
#plt.ylabel('LW_IN (W/m2)')
#
#
#plt.figure()
#ax1 = plt.subplot(3,1,1)
#plt.plot(Time_Met,df_Met['P_1'],Time_Met,df_Met['P_2'])
#plt.ylim(0,80)
#plt.legend(('k34','T1'),loc = 'upper right')
#plt.xlim(Time_Start, Time_End)
#plt.ylabel('PREC (mm/30min)')
#
#plt.subplot(3,1,2,sharex = ax1)
#plt.plot(Time_Met,df_Met['SW_IN'])
#plt.ylabel('SW_IN (W/m2)')
#
#plt.subplot(3,1,3,sharex = ax1)
#plt.plot(Time_Met,df_Met['NETRAD'])
#plt.ylabel('NETRAD (W/m2)')
#
#plt.show()


