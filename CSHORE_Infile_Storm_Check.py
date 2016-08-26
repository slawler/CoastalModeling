# -*- coding: utf-8 - Python 3.5.1 *-
"""
Description: Get List of Storms Not Created During CSHORE Pre-Processing
Input(s): Directory, Storm list
Output(s): Error Log
slawler@dewberry.com
Created on Fri Aug 26 12:04:50 2016
"""
#------------Load Python Modules--------------------#
import pandas as pd
from glob import glob
import os

#------------Functions------------------------------#
f = lambda x:x.split("\\")[-1] #Grab the Transect Number from the Dir Path

#------------User Inputs: PATHS---------------------#
#Parent Directory
ROOTDIR = r"P:\02\NY\Chautauqua_Co_36013C\STUDY__TO90\TECHNICAL\ENG_FLOOD_HAZ_DEV\COASTAL\WAVE_MODELING\CSHORE\CSHORE_Infile_Creater"
#StormList Path
stormlist = r"P:\02\NY\Chautauqua_Co_36013C\STUDY__TO90\TECHNICAL\ENG_FLOOD_HAZ_DEV\COASTAL\WAVE_MODELING\CSHORE\hydrographs\input\stormlist.txt"

#------------------------------BEGIN SCRIPT----------------------------------#
transects = glob(os.path.join(ROOTDIR,"output\\*"))
storms    = pd.read_csv(stormlist)

df = pd.DataFrame(columns = ['Transect','Storm','NA'], index = [0])
i=0

for t in transects:
    if os.path.isdir(t)==True:
        t_storms = glob(os.path.join(t,"*"))
        for tstorm in t_storms:
            print(i)
            df.ix[i] = [f(t), f(tstorm),1]
            i+=1


table = df.pivot(index = 'Transect',columns = 'Storm', values = 'NA')     
good_storms = pd.notnull(table)

#table.isnull().sum(axis = 1) #--Count of Storms Missing/transect
 
error_dict = {} 
tr_dict_list = []        
for t in table.index:
    ncols = len(table.ix[t])
    for c in range(ncols):
        if table.ix[t][c] != 1:
            missing_storm = table.columns[c]
            tr_dict_list.append(missing_storm)
    error_dict[t[2:]] = tr_dict_list
    tr_dict_list = []   
   
with open(os.path.join(ROOTDIR,'ERRORLOG.txt'),'w') as f:  
    f.write('Storms Not Processed for given Transect \n')
    for i, d in enumerate(error_dict):
        print("Transect : ", i+1)
        tr = str(i+1)
        output = str(tr) + str(error_dict[str(tr)]) +'\n'
        f.write(output)



