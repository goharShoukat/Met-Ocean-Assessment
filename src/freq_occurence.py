#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 11:03:46 2021

@author: goharshoukat

Generates Frequency of Occurance Tables

Creates tables by using dataframe dumping techniques

Bins data for two separate tables 

Creates heatmaps

"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.ticker import MaxNLocator, MultipleLocator
import cartopy as ct
from matplotlib.font_manager import FontProperties
import seaborn as sns


direc = 'tests/results/'
df = pd.read_csv(direc + '07_09-05_10_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])

y = df['hmax (m)'].to_numpy()
x = df['mwp (s)'].to_numpy()
bins_y = np.linspace(np.floor(min(y)), np.ceil(max(y)), int(np.ceil(max(y)) - np.floor(min(y)))*1+1) #converts height into 0.5 bins
bins_x = np.linspace(np.floor(min(x)), np.ceil(max(x)), int(np.ceil(max(x)) - np.floor(min(x)))+1) #returns bins with detla=1 bins
counts, xedges, yedges = np.histogram2d(x, y, bins=(bins_x, bins_y))
counts = counts/len(df) * 100
#following loops are important to create customized labels. 
#otherwise, instead of range, single value points are specified. 
xnew = [] 
for i in range(len(xedges)):
    if i == len(xedges)-1:
        break
    else:
        d = str(xedges[i]) + ' - ' + str(xedges[i+1])  
        xnew = np.append(xnew, d)
#add a total 
xnew = np.append(xnew, ['Sum']) #add additional column for the sum and the cumulative sum

ynew = []
for i in range(len(yedges)):
    if i == len(yedges)-1:
        break
    else:
        d = str(yedges[i]) + ' - ' + str(yedges[i+1])  
        ynew = np.append(ynew, d)

ynew = np.append(ynew, ['Sum']) #add additional column for the sum and additonal column

sum_col_arr = np.sum(counts, axis = 0).reshape(1,-1)
counts = np.append(counts, sum_col_arr, axis = 0)


sum_row_arr = np.sum(counts, axis = 1, keepdims = True)
counts = np.append(counts, sum_row_arr, axis = 1)

#function to generate a matrix of accumulative totals from the individual sums
def accumulative_(sum_arr):
    total = []
    for i in range(1, len(sum_arr)+1):
        dummy = np.sum(sum_arr[:i])
        total = np.append(total, dummy)
    return total
        
total_row = accumulative_(sum_row_arr)
total_col = accumulative_(sum_col_arr.T)
df2 = pd.DataFrame(counts)
mask = counts == 0 #exclue all 0s. cant change colour
#change the last row and the last column to True and mask it
#this will exclude them from the plotting of heatmap
#the main heatmap will still be of the actual content within the counts array
mask[13, :] = True
mask[:, 22] = True


plt.figure(figsize = (30,30))
#x and y labels are reversed to change orientation of the curve
ax = sns.heatmap(counts, annot = True, linewidths=0.5, mask = mask,\
                 cbar = False, xticklabels=ynew, yticklabels=xnew, annot_kws={"size": 'small'})
    


mask2 = counts == 0 #exclue all 0s. cant change colour
#mask all elements except the last row and last column
mask2[:,:] = True
mask2[-1,:] = False
mask2[:,-1] = False
ax2 = sns.heatmap(counts, mask = mask2, annot = True, linewidths=0.5,\
                 cbar = False, cmap='RdBu', xticklabels=ynew, yticklabels=xnew, annot_kws={"size": 'small', 'color':'white'})

plt.tick_params('both', bottom=False, left=False)
plt.ylabel('mwp (s)')
plt.xlabel('hmax (s)')
plt.title('Frequency of Occurance (mwp vs $H_{max}$)')

plt.tight_layout()
z = []
for t in ax.texts: 
    
    a = float(t.get_text())
    z = np.append(z, a)
    if (a < 0.01) & (a != 0):
        t.set_text('{0:.0E}'.format(a))
    if (a > 0.01):
        t.set_text('{:.2f}'.format(a))



