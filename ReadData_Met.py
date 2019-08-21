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


Met_File = 'k34_Met_2012_2017_v4.csv'

df_Met_original = pd.read_csv(Met_File, header = 0,na_values = '-9999')
df_Met = df_Met_original
#print(df_SWC_original['TIMESTAMP_START'].iloc(0))
#print(df_SWC_original['TIMESTAMP_START'].iloc(end))

df_Met.to_pickle('Met_2012_2017.pkl')
