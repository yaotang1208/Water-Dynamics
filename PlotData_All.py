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

df_SWC = pd.read_pickle('SWC_2012_2017.pkl')
df_SWC_R = pd.read_pickle('SWC_R_Corrected.pkl')
df_Met = pd.read_pickle('Met_2012_2017.pkl')

Time = [datetime.strptime(str(i),'%Y%m%d%H%M') for i in df_SWC['TIMESTAMP_START']]
Time_Met = [datetime.strptime(str(i),'%Y%m%d%H%M') for i in df_Met['TIMESTAMP_START']]
Time_R = df_SWC_R['TIMESTAMP']

Depth_Soil = [-5,-10,-20,-30,-40,-100]
Depth_Tem = [-2,-5,-10,-20,-50]
Depth_R = [-10, -20, -40, -60, -100]

Height_Tem = [51.1,42.5,35.5,28.0,15.6,5.2]
Height_CO2 = [50,35.3,28,15.6,5.2,0.5] # H2O and CO2 at the same heights

TA_Profile = np.vstack((df_Met['TA_1'],df_Met['TA_2'],df_Met['TA_3'],df_Met['TA_4'],df_Met['TA_5'],df_Met['TA_6']))
CO2_Profile = np.vstack((df_Met['CO2_1'],df_Met['CO2_2'],df_Met['CO2_3'],df_Met['CO2_4'],df_Met['CO2_5'],df_Met['CO2_6']))
H2O_Profile = np.vstack((df_Met['H2O_1'],df_Met['H2O_2'],df_Met['H2O_3'],df_Met['H2O_4'],df_Met['H2O_5'],df_Met['H2O_6']))

Soil_Data = np.vstack((df_SWC['SWC_1'],df_SWC['SWC_2'],df_SWC['SWC_3'],
             df_SWC['SWC_4'],df_SWC['SWC_5'],df_SWC['SWC_6']))

SoilT_Data = np.vstack((df_SWC['TS_1'],df_SWC['TS_2'],df_SWC['TS_3'],
             df_SWC['TS_4'],df_SWC['TS_5']))

SWC_p1 = np.vstack((df_SWC_R['VWC_1_Avg'],df_SWC_R['VWC_2_Avg'],df_SWC_R['VWC_3_Avg'],
df_SWC_R['VWC_4_Avg'],df_SWC_R['VWC_5_Avg']))

SWC_p2 = np.vstack((df_SWC_R['VWC_6_Avg'],df_SWC_R['VWC_7_Avg'],df_SWC_R['VWC_8_Avg'],
df_SWC_R['VWC_9_Avg'],df_SWC_R['VWC_10_Avg']))

TS_p1 = np.vstack((df_SWC_R['T_1_Avg'],df_SWC_R['T_2_Avg'],df_SWC_R['T_3_Avg'],
df_SWC_R['T_4_Avg'],df_SWC_R['T_5_Avg']))

TS_p2 = np.vstack((df_SWC_R['T_6_Avg'],df_SWC_R['T_7_Avg'],df_SWC_R['T_8_Avg'],
df_SWC_R['T_9_Avg'],df_SWC_R['T_10_Avg']))

#%%
# Soil moisture time series
plt.figure()
ax1 = plt.subplot(4,1,1)
plt.plot(Time_Met,df_Met['P_1'],Time_Met,df_Met['P_2'])
plt.ylim(0,80)
plt.legend(('k34','T1'),loc = 'upper right')
plt.ylabel('PREC (mm/30min)')

plt.subplot(4,1,2,sharex = ax1)
plt.plot(Time,df_SWC['SWC_1'],
Time,df_SWC['SWC_2'],
Time,df_SWC['SWC_3'],
Time,df_SWC['SWC_4'],
Time,df_SWC['SWC_5'],
Time,df_SWC['SWC_6'])
plt.legend(('5cm','10cm', '20 cm','30cm','40cm','100 cm'),loc = 'upper right')
plt.ylabel('K34 SWC (m3/m3)')
#plt.title('K34 Tower)')

plt.subplot(4,1,3, sharex = ax1)
plt.plot(Time_R,df_SWC_R['VWC_1_Avg'],
Time_R,df_SWC_R['VWC_2_Avg'],
Time_R,df_SWC_R['VWC_3_Avg'],
Time_R,df_SWC_R['VWC_4_Avg'],
Time_R,df_SWC_R['VWC_5_Avg'])
plt.legend(('10 cm','20 cm', '40 cm','60 cm','100 cm'),loc = 'upper right')
plt.ylabel('Pit 1 SWC (m3/m3)')
#plt.title('Pit 1 (~12 m from K34 Tower)')

plt.subplot(4,1,4, sharex = ax1)
plt.plot(Time_R,df_SWC_R['VWC_6_Avg'],
Time_R,df_SWC_R['VWC_7_Avg'],
Time_R,df_SWC_R['VWC_8_Avg'],
Time_R,df_SWC_R['VWC_9_Avg'],
Time_R,df_SWC_R['VWC_10_Avg'])
plt.legend(('10 cm','20 cm', '40 cm','60 cm','100 cm'),loc = 'upper right')
plt.ylim(0.2,0.6)
plt.ylabel('Pit 2 SWC (m3/m3)')
#plt.title('Pit 2 (~30.5 m from K34 Tower)')

# soil temperature time series
plt.figure()
ax2 = plt.subplot(3,1,1)
plt.plot(Time,df_SWC['TS_1'],
Time,df_SWC['TS_2'],
Time,df_SWC['TS_3'],
Time,df_SWC['TS_4'],
Time,df_SWC['TS_5'])
plt.legend(('2cm','5cm', '10cm','20cm','50cm'),loc = 'upper right')
plt.ylabel('k34 TS (DegC)')
#plt.title('K34 Tower)')

plt.subplot(3,1,2, sharex = ax2)
plt.plot(Time_R,df_SWC_R['T_1_Avg'],
Time_R,df_SWC_R['T_2_Avg'],
Time_R,df_SWC_R['T_3_Avg'],
Time_R,df_SWC_R['T_4_Avg'],
Time_R,df_SWC_R['T_5_Avg'])
plt.ylim(22,30)
plt.legend(('10 cm','20 cm', '40 cm','60 cm','100 cm'),loc = 'upper right')
plt.ylabel('Pit 1 TS (DegC)')
#plt.title('Pit 1 (~12 m from K34 Tower)')

plt.subplot(3,1,3, sharex = ax2)
plt.plot(Time_R,df_SWC_R['T_6_Avg'],
Time_R,df_SWC_R['T_7_Avg'],
Time_R,df_SWC_R['T_8_Avg'],
Time_R,df_SWC_R['T_9_Avg'],
Time_R,df_SWC_R['T_10_Avg'])
plt.ylim(22,30)
plt.legend(('10 cm','20 cm', '40 cm','60 cm','100 cm'),loc = 'upper right')
plt.ylabel('Pit 2 TS (DegC)')
#plt.title('Pit 2 (~30.5 m from K34 Tower)')

# k34 Soil and air temperature time series

plt.figure()
ax1 = plt.subplot(4,1,1)
plt.plot(Time_Met,df_Met['CO2_1'],
Time_Met,df_Met['CO2_2'],
Time_Met,df_Met['CO2_3'],
Time_Met,df_Met['CO2_4'],
Time_Met,df_Met['CO2_5'],
Time_Met,df_Met['CO2_6'])
plt.legend(('50m','35.3m', '28m','15.6m','5.2m','0.5m'),loc = 'upper right')
plt.ylabel('K34 CO2 (ppm)')

plt.subplot(4,1,2,sharex = ax1)
plt.plot(Time_Met,df_Met['H2O_1'],
Time_Met,df_Met['H2O_2'],
Time_Met,df_Met['H2O_3'],
Time_Met,df_Met['H2O_4'],
Time_Met,df_Met['H2O_5'],
Time_Met,df_Met['H2O_6'])
plt.legend(('50m','35.3m', '28m','15.6m','5.2m','0.5m'),loc = 'upper right')
plt.ylabel('K34 H2O')

plt.subplot(4,1,3, sharex = ax1)
plt.plot(Time,df_SWC['SWC_1'],
Time,df_SWC['SWC_2'],
Time,df_SWC['SWC_3'],
Time,df_SWC['SWC_4'],
Time,df_SWC['SWC_5'],
Time,df_SWC['SWC_6'])
plt.legend(('5cm','10cm', '20 cm','30cm','40cm','100 cm'),loc = 'upper right')
plt.ylabel('K34 SWC (m3/m3)')
#plt.title('Pit 1 (~12 m from K34 Tower)')

plt.subplot(4,1,4, sharex = ax1)
plt.plot(Time_Met,df_Met['TA_1'],
Time_Met,df_Met['TA_2'],
Time_Met,df_Met['TA_3'],
Time_Met,df_Met['TA_4'],
Time_Met,df_Met['TA_5'],
Time_Met,df_Met['TA_6'],
Time,df_SWC['TS_1'],'--',
Time,df_SWC['TS_2'],'--',
Time,df_SWC['TS_3'],'--',
Time,df_SWC['TS_4'],'--',
Time,df_SWC['TS_5'],'--')
plt.legend(('51.1m','42.5m', '35.5m','28cm','15.6m','5.2m',
            '-2cm','-5cm', '-10cm','-20cm','-50cm'),loc = 'upper right')
plt.ylabel('k34 T (DegC)')
#plt.title('Pit 2 (~30.5 m from K34 Tower)')

#%%
# Soil Water Content contours
Range_SWC = np.linspace(0.1,0.7,20)
Range_TS = np.linspace(20,35,20)

gs = gridspec.GridSpec(4,2,width_ratios=[30, 1])
fig = plt.figure()
ax5 = fig.add_subplot(gs[0,0])
plt.plot(Time_Met,df_Met['P_2'])
plt.ylabel('PREC (mm/30min)')
# plt.xlim(pd.Timestamp('2015-07-01'), pd.Timestamp('2016-07-01'))
plt.title('Soil Moisture')

fig.add_subplot(gs[1,0], sharex = ax5)
im = plt.contourf(Time, Depth_Soil,Soil_Data,levels = Range_SWC,cmap=cm.jet_r)
# plt.xlim(pd.Timestamp('2015-07-01'), pd.Timestamp('2016-07-01'))
# plt.legend(('k34'),loc = 'upper right')
# plt.colorbar()

fig.add_subplot(gs[2,0], sharex = ax5)
plt.contourf(Time_R, Depth_R,SWC_p1,levels = Range_SWC,cmap=cm.jet_r)
# plt.legend(('12 m from k34'),loc = 'upper right')
plt.ylabel('Depth (cm)')
# plt.colorbar()

fig.add_subplot(gs[3,0], sharex = ax5)
plt.contourf(Time_R, Depth_R,SWC_p2,levels = Range_SWC,cmap=cm.jet_r)
# plt.legend(('30.5 m from k34'),loc = 'upper right')

bax = fig.add_subplot(gs[1:,1])
cbar = plt.colorbar(im,bax)

# Soil Temperature
gs = gridspec.GridSpec(3,2,width_ratios=[30, 1])
fig1 = plt.figure()
ax9 = fig1.add_subplot(gs[0,0])
im = plt.contourf(Time, Depth_Tem,SoilT_Data,levels = Range_TS,cmap=cm.jet)
#plt.xlim(pd.Timestamp('2015-09-8'), pd.Timestamp('2015-10-15'))
#ax9.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"));
# plt.legend(('k34'),loc = 'upper right')
#plt.colorbar()
plt.title('Soil Temperature (DegC)')

#plt.subplot(3,1,2, sharex = ax9,sharey = ax9)
fig1.add_subplot(gs[1,0],sharex = ax9,sharey = ax9)
plt.contourf(Time_R, Depth_R,TS_p1,levels = Range_TS,cmap=cm.jet)
# plt.legend(('12 m from k34'),loc = 'upper right')
plt.ylabel('Depth (cm)')
#plt.colorbar()

fig1.add_subplot(gs[2,0],sharex = ax9,sharey = ax9)
plt.contourf(Time_R, Depth_R,TS_p2,levels = Range_TS,cmap=cm.jet)
# plt.legend(('30.5 m from k34'),loc = 'upper right')
#plt.colorbar()

bax = fig1.add_subplot(gs[0:,1])
cbar = plt.colorbar(im,bax)

# Soil Temperature, Air Temperature
Range_TA = np.linspace(20,40,20)

#gs = gridspec.GridSpec(4,2,width_ratios=[30, 1])
fig1 = plt.figure()
ax9 = fig1.add_subplot(2,1,1)
im = plt.contourf(Time_Met, Height_Tem,TA_Profile,levels = Range_TA,cmap=cm.jet)
plt.ylabel('K34 TA height (m)')
plt.colorbar()

ax10 = fig1.add_subplot(2,1,2,sharex = ax9)
plt.contourf(Time, Depth_Tem,SoilT_Data,levels = Range_TS,cmap=cm.jet)
#plt.xlim(pd.Timestamp('2015-09-8'), pd.Timestamp('2015-10-15'))
#ax9.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"));
# plt.legend(('k34'),loc = 'upper right')
plt.colorbar()
plt.ylabel('K34 TS Depth (cm)')
fig1.autofmt_xdate()

# K34 Soil Moisture, CO2, and H2O
Range_SWC = np.linspace(0.1,0.7,20)
Range_CO2 = np.linspace(350,550,20)
Range_H2O = np.linspace(0,60,20)

gs = gridspec.GridSpec(3,2,width_ratios=[30, 1])
fig1 = plt.figure()
ax9 = fig1.add_subplot(gs[0,0])
im1 = plt.contourf(Time_Met, Height_CO2,CO2_Profile,levels = Range_CO2,cmap=cm.jet)
plt.ylabel('K34 CO2 height (m)')
bax = fig1.add_subplot(gs[0,1])
cbar = plt.colorbar(im1,bax)

#plt.subplot(3,1,2, sharex = ax9,sharey = ax9)
fig1.add_subplot(gs[1,0],sharex = ax9)
im2 = plt.contourf(Time_Met, Height_CO2,H2O_Profile,levels = Range_H2O,cmap=cm.jet_r)
plt.ylabel('K34 H2O height (m)')
bax = fig1.add_subplot(gs[1,1])
cbar = plt.colorbar(im2,bax)
#plt.colorbar()

fig1.add_subplot(gs[2,0],sharex = ax9)
im3 = plt.contourf(Time, Depth_Soil,Soil_Data,levels = Range_SWC,cmap=cm.jet_r)
plt.ylabel('K34 Soil Moisture Depth (cm)')
bax = fig1.add_subplot(gs[2,1])
cbar = plt.colorbar(im3,bax)

plt.show()
