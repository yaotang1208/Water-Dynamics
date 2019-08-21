# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:44:17 2019

@author: yaotang
"""

import sys
import os
import logging
# import datetime
import statsmodels.api as sm
import pandas as pd


SWC_File = 'k34_SPCD30_2012_2017_v1.csv'

Start = 157826
End = 263090
N = End - Start


df_SWC_original = pd.read_csv(SWC_File, header = 0,na_values = '-9999')
df_SWC = df_SWC_original.iloc[Start:End]
#print(df_SWC_original['TIMESTAMP_START'].iloc(0))
#print(df_SWC_original['TIMESTAMP_START'].iloc(end))

df_SWC.to_pickle('SWC_2015_2017.pkl')
