# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Reads Adcirc Station Output file fort.61 & returns plotted hydrographs
Input(s): fort.61, Stations to plot, dates, periods, freq
Output(s): jpgs

ToDo: Add lines to grab t-series info from fort.15

slawler@dewberry.com
Created on Thu Sep 15, 2016
"""

import fileinput
import pandas as pd
import matplotlib.pyplot as plt
import datetime

#------------User Inputs----------------------------#
infile = 'fort.61'

#---Initialize & Name Station Dictionaries
nodes = {'1':[],'2':[],'3':[],'4':[],'5':[]}

node_names = {'1':'CBBT','2':'SewPt','3':'WasDC',
              '4':'Alex','5':'OcnCty'}

#----Enter Run info
start, freq, period = "09/15/2016",'7.5min',960


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#------------------------------BEGIN SCRIPT----------------------------------#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

indx = pd.date_range(start=start,periods = period, freq=freq)


for line in fileinput.input(infile):
    n = line.strip().split(' ')[0]
    if n in nodes:
        data = line.strip().split()[1]
        nodes[n].append(float(data))

df = pd.DataFrame.from_dict(nodes).rename(columns =node_names)
df.replace(to_replace=-99999.000000,value=0,inplace=True)
df = df.set_index(indx)

for col in df:
    print "Plotting: ", col
    ax = df.plot(x = df.index, y = col)
    fig = ax.get_figure()
    fig.savefig('{}.jpg'.format(col))
    plt.show(block = False)
    plt.close(fig)



