#!/usr/bin/env python 3.5.2
# -*- coding: utf-8 -*-
"""
Description:
    
Input(s):
Output(s):

@author: slawler@dewberry.com
Created on Sun Oct 23 18:10:24 2016
"""
# In[]:
#------------Load Python Modules--------------------#
import matplotlib.pyplot as plt
import fileinput
import datetime
import pandas as pd
import os
import requests
from scipy.interpolate import interp1d

# In[]:
#------------------------------------User Inputs

root_dir = r'C:\Users\sml\Desktop'
adcirc_file = 'fort.61'

start, freq = "09-2015-22 20:00","3600s" #---Date Format: %m-%Y-%d %H:%M

nodes = {'10':{'8571421':[]},'31':{'8632200':[]},'27':{'8636580':[]}}

noaa_time_step = '6T'

#--NOAA API https://tidesandcurrents.noaa.gov/api/
datum     = "msl"   #"NAVD"                  #Datum
units     = "metric"                         #Units
time_zone = "lst_ldt"                         #Time Zone
fmt       = "json"                            #Format
url       = 'http://tidesandcurrents.noaa.gov/api/datagetter'
product   = 'water_level'                     #Product


# In[]:
#------------------------------------Read file & Extract Time Series Data

f = os.path.join(root_dir,adcirc_file)

stations = dict()
for n in nodes:
    for key in nodes[n]:
        stations[n]= key

for line in fileinput.input(f):
    n = line.strip().split(' ')[0]
    if n in nodes:
        data = line.strip().split()[1]
        nodes[n][stations[n]].append(float(data))
        periods = len(nodes[n][stations[n]])

for n in nodes:
    for key in nodes[n]:
        period = len(nodes[n][key])   
        
# In[]:
#---------------------Ping NOAA API for Validation Data,Create NOAA Dataframe

noaa = pd.DataFrame()
gages = dict()

first = datetime.datetime.strptime(start,"%m-%Y-%d %H:%M" )
last =  pd.date_range(first,periods = period, freq=freq)[-1]
 
for n in nodes:
    for key in nodes[n]:
        g = int(key)
       
    t0     = first.strftime('%Y%m%d %H:%M')
    t1     = last.strftime('%Y%m%d %H:%M')
    api_params = {'begin_date': t0, 'end_date': t1,
                'station': g,'product':product,'datum':datum,
                'units':units,'time_zone':time_zone,'format':fmt,
                'application':'web_services' }
        
    pred=[];obsv=[];t=[]

    try:
        r = requests.get(url, params = api_params)
        jdata =r.json()
    
        for j in jdata['data']:
            t.append(str(j['t']))
            obsv.append(str(j['v']))
            pred.append(str(j['s']))
        colname = str(g)    
        noaa[colname]= obsv
        noaa[colname] = noaa[colname].astype(float)
        gages[jdata['metadata']['id']]=jdata['metadata']['name']
    except:
        print(g,'No Data')      
     
idx = pd.date_range(first,periods = len(noaa.index), freq=noaa_time_step)   
noaa = noaa.set_index(idx)       
        
# In[]:
#--------------------------Create ADCIRC DataFrame

adcirc = pd.DataFrame()

for key in nodes:
    adcirc[key]=nodes[key][stations[key]] 

adcirc.replace(to_replace=-99999.000000,value=0,inplace=True)
adc_idx = pd.date_range(first,periods = period, freq=freq)

adcirc = adcirc.set_index(adc_idx)
  
# In[]:
#-------------------------Join ADCIRC & NOAA Dataframes, Resample ADCIRC values

df = noaa.merge(adcirc, how='outer', left_index=True, right_index=True)

for n in nodes:
    df[n] = df[n].interpolate()

    
    
# In[]:
#--------------------------Plot Results for Each Station        
 
for n in nodes:
    for key in nodes[n]:
       df.plot(x = df.index, y = [n,key])
       plt.title(gages[key])
       plt.grid()
       print('\nPlotting Adcirc Station {} for gage {}, {}:'.format(n,key, gages[key]))  

        



