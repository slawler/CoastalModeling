# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 01:25:09 2016

Description:
Input:
Output:

@author: sml
"""

#------------Import Python Modules-----------#
import pandas as pd
import sys

ModPATH = r'C:\Users\sml\Desktop'
sys.path.append(ModPATH)
from AdcircResultsExtractor import *

#-----------USER INPUTS----------------------#

fort = 'fort.61'

nodes = {'1':[],'2':[],'3':[],'4':[],'5':[]}

node_names = {'1':'CBBT','2':'SewPt','3':'WasDC','4':'Alex','5':'OcnCty'}

gage = str(8638863)

data = AdcircOutput(fort, nodes)

tstep_0 = data.parameters()[0]

params  = start, freq, period = tstep_0, 1800, 60

df_adcirc = data.tseries(params, node_names)

noaa = data.noaa_data(gage)

for col in df_adcirc:    
    for i in range(0,10):
        if type(noaa) != pd.core.frame.DataFrame:
            print 'Pinging NOAA API, Attempt #', str(i+1), col
            noaa = data.noaa_data(gage)
        else:
            print '\nPinging NOAA API, Attempt #{}'.format(str(i+1)), '\n\tData downloaded for gage {}'.format(gage) 
            df_noaa = noaa.asfreq('1800s', method='nearest')
            df = df_adcirc.merge(df_noaa, how='outer', left_index=True, right_index=True)    
            data.PlotResults(df,col)
            break



