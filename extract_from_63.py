# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Reads Adcirc Global Output file fort.63 & returns time series at
selected nodes. 

Input(s): fort.63, Nodes of interest
Output(s): Time series .txt files 

jdorvinen@dewberry.com, slawler@dewberry.com

Created on Tue Apr 19 15:08:33 2016 
"""
#------------Load Python Modules--------------------#
import fileinput
from datetime import datetime as dt

#------------User Inputs----------------------------#
infile = 'fort.63'

nodes = {'1':[],'3':[],'23':[],'39':[],'43':[],'75':[],'2123':[],'2656':[],'2354':[],'265665':[],'1685434':[]}

#------------------------------BEGIN SCRIPT----------------------------------#
a = dt.now()
print("\n Started reading Global File at \n") 
print(a)

f = fileinput.input(infile)

for line in f:
    n = line.strip().split(' ')[0] 
    if n in nodes:
        nodes[n].append(line)

for n in nodes:    
    output = open('extracted_%s.txt' %(n),'w')
    header = "      NODE                  SWEL\n"
    output.write(header)
    for i in range(len(nodes[n])):
        output.write(nodes[n][i])

output.close(); fileinput.close()
    
b = dt.now()
c = b-a
print("===========END========== \n")
print("Processing Time : ")
print(c)
