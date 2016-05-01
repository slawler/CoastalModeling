# -*- coding: utf-8 -*-
"""
Purpose: Download Time Series data from NOAA API

Created on Tue Apr  5 23:21:12 2016

@author: slawler@dewberry.com
"""
#---------------LOAD PYTHON MODULES-----------------------#
from pandas import date_range, DateOffset
from datetime import datetime
from urllib import urlencode 
from urllib2 import urlopen, Request
from time import sleep

#---------------ENTER VARIABLES---------------------------#
station   = str(8510560)                      #Station ID
start     = datetime(2010, 1, 1,0)            #Start Date
stop      = datetime(2015, 1, 1,0)            #End Date
interval  = DateOffset(months=6)              #ChunkSize   
PATH      = "C:\Users\slawler\Desktop\LinuxShare\NOAA"  #Download Directory 

product   = "hourly_height"                   #Scalar of Interest  
datum     = "msl"                             #Datum
units     = "english"                         #Units  
time_zone = "lst_ldt"                         #Time Zone 
format    = "csv"                             #Format  
url       = 'http://tidesandcurrents.noaa.gov/api/datagetter'

#----------------------------------------------------------#
#-----------------------RUN SCRIPT-------------------------#
#----------------------------------------------------------#

#---Create Time Series (DatetimeIndex) 
daterange = date_range(start,stop - interval ,freq = interval)
download_start = datetime.now() #Get Program Start Time

#---Initialize Error Log in Download Directory
with open(PATH + '/ErrorLog.txt', 'w') as f: 
    f.write('Download Began    : ' + str(download_start) +'\n')

print "\n=====BEGIN PROCESS: %s" %(str(download_start)),"====="
      
#---Loop Through Date Range, Ping URL for data, write data to file      
for d in daterange:
    print "Grabbing NOAA Station Data beginning: ", d
    try:
        first    = datetime.date(d).strftime('%Y%m%d')
        last     =  datetime.date(d + interval).strftime('%Y%m%d')    
        
        params   = {'begin_date': first+" 00:00", 'end_date': last+" 00:00", 
                    'station': station,'product':product,'datum':datum,
                     'units':units,'time_zone':time_zone,'format':format,
                     'application':'web_services' }
                     
        data     = urlencode(params)
        request  = Request(url, data)
        response = urlopen(request)
        ouput    = response.read()
        
        with open(PATH + '/%s.out' % first,'w') as f:
            f.write(ouput)
            
    except:
        with open(PATH +'/ErrorLog.txt', 'a') as f:
            f.write("ERROR for date beginning: %s" %(first)  + '\n')
        print 'Check Error Log'
    
    sleep(5)

#---Write End time in Error Log
download_stop = download_start = datetime.now()

with open(PATH + '/ErrorLog.txt', 'a') as f: 
    f.write('Download Completed: ' + str(download_stop)+'\n')    

print "=====END PROCESS: %s" %(str(download_stop)),"=====" 

