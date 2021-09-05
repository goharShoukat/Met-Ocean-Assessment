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
from datetime import datetime

def frequency_occurence(df, x_variable, y_variable, Coordinates, date_range, title, units, direc):
    #inputs
    #df : pd.DataFrame : the entire dataframe as it is passed through from the run_code script
    #x_variable: str : x variable name for the heatmap. like mwp
    #y_variable: ndarray : input array like swh
    #the titles are used in plotting
    
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #title : str : title of the plot e.g. mwp vs swh
    #units : list : list of two elements. units[0] = unit of x, units[1] = unit of y
    #direc : str : output directory entered by user
    #output:
        #Frequency of Occurence Plot of the two specified quantities
    
    #y is divided into bins of 0.5 deltas. inputting swh as y is recommended
    #x is divded into bins of 1 delta. inputting mwp is recommended
    #f['Date'] = pd.to_datetime(df['Date'])
   
    y = df[y_variable].to_numpy()
    x = df[x_variable].to_numpy()
    bins_y = np.linspace(np.floor(min(y)), np.ceil(max(y)), int(np.ceil(max(y)) - np.floor(min(y)))*2+1) #converts height into 0.5 bins
    bins_x = np.linspace(np.floor(min(x)), np.ceil(max(x)), int(np.ceil(max(x)) - np.floor(min(x)))+1) #returns bins with detla=1 bins
    counts, xedges, yedges = np.histogram2d(x, y, bins=(bins_x, bins_y))
    counts = counts/len(df) * 100
    counts = np.flip(counts, axis = 0)
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
    xnew = np.flip(xnew, axis = 0)
    xnew = np.append(xnew, ['Sum', 'Accumulative']) #add additional column for the sum and the cumulative sum
    
    ynew = []
    for i in range(len(yedges)):
        if i == len(yedges)-1:
            break
        else:
            d = str(yedges[i]) + ' - ' + str(yedges[i+1])  
            ynew = np.append(ynew, d)
    
    ynew = np.append(ynew, ['Sum', 'Accumulative']) #add additional column for the sum and additonal column
    
    sum_col_arr = np.sum(counts, axis = 0).reshape(1,-1)
    acc_col = [] #accumulative of each column
    for i in range(1,np.shape(sum_col_arr)[1]+1):
        acc_col = np.append(acc_col, np.sum(sum_col_arr[0, 0:i])).reshape(1, -1)
        
        
    sum_col = np.append(sum_col_arr, acc_col, axis = 0) #merge the two columns together for the sums
    #sum_col = np.round(sum_col, 3)
    counts = np.append(counts, sum_col, axis = 0)
    
    
    sum_row_arr = np.sum(counts, axis = 1, keepdims = True)
    acc_row = [] #accumulative of each row
    for i in range(1,np.shape(sum_row_arr)[0]+1):
        acc_row = np.append(acc_row, np.sum(sum_row_arr[:i, 0])).reshape(-1, 1)
    sum_row = np.append(sum_row_arr, acc_row, axis = 1)
    #sum_row = np.round(sum_row, 3)
    counts = np.append(counts, sum_row, axis = 1)
    
    counts[np.shape(counts)[0]-1, np.shape(counts)[1]-1] = 0
    counts[np.shape(counts)[0]-1, np.shape(counts)[1]-1-1] = 0
    counts[np.shape(counts)[0]-1-1, np.shape(counts)[1]-1] = 0
    
    
    
    mask = counts == 0 #exclue all 0s. cant change colour
    #change the last row and the last column to True and mask it
    #this will exclude them from the plotting of heatmap
    #the main heatmap will still be of the actual content within the counts array
    mask[-2:, :] = True
    mask[:, -2:] = True
    
    
    plt.figure(figsize = (30,30))
    #x and y labels are reversed to change orientation of the curve
    
    #mask all elements except the last row and last column
    mask2 = counts == 0 #exclue all 0s. cant change colour
    mask2[:,:] = True
    mask2[-2,:] = False
    mask2[:,-2] = False
    mask2[np.shape(counts)[0]-1, np.shape(counts)[1]-1] = True#remove the 0s at the end of the two rows and columns
    mask2[np.shape(counts)[0]-1, np.shape(counts)[1]-1-1] = True
    mask2[np.shape(counts)[0]-1-1, np.shape(counts)[1]-1] = True
    
    mask3 = counts == 0 #exclue all 0s. cant change colour
    mask3[:,:] = True
    mask3[-1:,:] = False
    mask3[:,-1:] = False
    mask3[np.shape(counts)[0]-1, np.shape(counts)[1]-1] = True#remove the 0s at the end of the two rows and columns
    mask3[np.shape(counts)[0]-1, np.shape(counts)[1]-1-1] = True
    mask3[np.shape(counts)[0]-1-1, np.shape(counts)[1]-1] = True

    
    ax = sns.heatmap(counts, annot = True, linewidths=0.5, mask = mask,\
                     cbar = False, xticklabels=ynew, yticklabels=xnew, annot_kws={"size": 'small'})
        
    ax2 = sns.heatmap(counts, mask = mask2, annot = True, linewidths=0.5,\
                     cbar = False, xticklabels=ynew, yticklabels=xnew, annot_kws={"size": 'small'}, fmt = 'f')
    
    ax3 = sns.heatmap(counts, mask = mask3, annot = True, linewidths=0.5,\
                     cbar = False, xticklabels=ynew, yticklabels=xnew, annot_kws={"size": 'small'}, fmt = 'f')
        
    z = []
    for t in ax.texts: 
        
        a = float(t.get_text())
        z = np.append(z, a)
        if (a < 0.01) & (a != 0):
            t.set_text('{0:.0E}'.format(a))
        if (a > 0.01):
            t.set_text('{:.2f}'.format(a))
        if (a > 99):
            t.set_text('{:.3f}'.format(a))
        if (a == 0):
            t.set_text('{:.0f}'.format(a))
    
    
    
    
    plt.tick_params('both', bottom=False, left=False)
    plt.ylabel(x_variable + ' (' + units[0] + ')')
    plt.xlabel(y_variable + ' (' + units[1] + ')')
    plt.xticks(rotation=70)
    plt.title('{}\nFrequency of Occurrence ({}): {}'.format(Coordinates, title, date_range))
    
    plt.tight_layout()
    plt.savefig(direc + 'Heatmap ' + title + '.pdf')
    plt.close()

#code tests
#direc = 'tests/results/'
#df = pd.read_csv('09_03-08_41_PM.csv', index_col = False)
#frequency_occurence(df, 'mwp (s)', 'swh (m)', '51.5  $^\circ$N, -8 E', '1979 - 2019', 'mwp vs swh', ['s', 'm'])

'''
direc = 'tests/results/'
df = pd.read_csv(direc + '07_09-05_10_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])

y = df['swh (m)'].to_numpy()
x = df['mwp (s)'].to_numpy()
bins_y = np.linspace(np.floor(min(y)), np.ceil(max(y)), int(np.ceil(max(y)) - np.floor(min(y)))*2+1) #converts height into 0.5 bins
bins_x = np.linspace(np.floor(min(x)), np.ceil(max(x)), int(np.ceil(max(x)) - np.floor(min(x)))+1) #returns bins with detla=1 bins
counts, xedges, yedges = np.histogram2d(x, y, bins=(bins_x, bins_y))
counts = counts/len(df) * 100
counts = np.flip(counts, axis = 0)
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
xnew = np.flip(xnew, axis = 0)
xnew = np.append(xnew, ['Sum', 'Accumulative']) #add additional column for the sum and the cumulative sum

ynew = []
for i in range(len(yedges)):
    if i == len(yedges)-1:
        break
    else:
        d = str(yedges[i]) + ' - ' + str(yedges[i+1])  
        ynew = np.append(ynew, d)

ynew = np.append(ynew, ['Sum', 'Accumulative']) #add additional column for the sum and additonal column

sum_col_arr = np.sum(counts, axis = 0).reshape(1,-1)
acc_col = [] #accumulative of each column
for i in range(1,np.shape(sum_col_arr)[1]+1):
    acc_col = np.append(acc_col, np.sum(sum_col_arr[0, 0:i])).reshape(1, -1)

sum_col = np.append(sum_col_arr, acc_col, axis = 0) #merge the two columns together for the sums
#sum_col = np.round(sum_col, 3)
counts = np.append(counts, sum_col, axis = 0)


sum_row_arr = np.sum(counts, axis = 1, keepdims = True)
acc_row = [] #accumulative of each row
for i in range(1,np.shape(sum_row_arr)[0]+1):
    acc_row = np.append(acc_row, np.sum(sum_row_arr[:i, 0])).reshape(-1, 1)
sum_row = np.append(sum_row_arr, acc_row, axis = 1)
#sum_row = np.round(sum_row, 3)
counts = np.append(counts, sum_row, axis = 1)

counts[np.shape(counts)[0]-1, np.shape(counts)[1]-1] = 0
counts[np.shape(counts)[0]-1, np.shape(counts)[1]-1-1] = 0
counts[np.shape(counts)[0]-1-1, np.shape(counts)[1]-1] = 0



mask = counts == 0 #exclue all 0s. cant change colour
#change the last row and the last column to True and mask it
#this will exclude them from the plotting of heatmap
#the main heatmap will still be of the actual content within the counts array
mask[-2:, :] = True
mask[:, -2:] = True


plt.figure(figsize = (30,30))
#x and y labels are reversed to change orientation of the curve

#mask all elements except the last row and last column
mask2 = counts == 0 #exclue all 0s. cant change colour
mask2[:,:] = True
mask2[-2,:] = False
mask2[:,-2] = False
mask2[np.shape(counts)[0]-1, np.shape(counts)[1]-1] = True#remove the 0s at the end of the two rows and columns
mask2[np.shape(counts)[0]-1, np.shape(counts)[1]-1-1] = True
mask2[np.shape(counts)[0]-1-1, np.shape(counts)[1]-1] = True

mask3 = counts == 0 #exclue all 0s. cant change colour
mask3[:,:] = True
mask3[-1:,:] = False
mask3[:,-1:] = False
mask3[np.shape(counts)[0]-1, np.shape(counts)[1]-1] = True#remove the 0s at the end of the two rows and columns
mask3[np.shape(counts)[0]-1, np.shape(counts)[1]-1-1] = True
mask3[np.shape(counts)[0]-1-1, np.shape(counts)[1]-1] = True

ax = sns.heatmap(counts, annot = True, linewidths=0.5, mask = mask,\
                 cbar = False, xticklabels=ynew, yticklabels=xnew, annot_kws={"size": 'small'})
    
ax2 = sns.heatmap(counts, mask = mask2, annot = True, linewidths=0.5,\
                 cbar = False, xticklabels=ynew, yticklabels=xnew, annot_kws={"size": 'small'}, fmt = 'f')

ax3 = sns.heatmap(counts, mask = mask3, annot = True, linewidths=0.5,\
                 cbar = False, xticklabels=ynew, yticklabels=xnew, annot_kws={"size": 'small'}, fmt = 'f')
    
z = []
for t in ax.texts: 
    
    a = float(t.get_text())
    z = np.append(z, a)
    if (a < 0.01) & (a != 0):
        t.set_text('{0:.0E}'.format(a))
    if (a > 0.01):
        t.set_text('{:.2f}'.format(a))
    if (a > 99):
        t.set_text('{:.3f}'.format(a))
    if (a == 0):
        t.set_text('{:.0f}'.format(a))




plt.tick_params('both', bottom=False, left=False)
plt.ylabel('mwp (s)')
plt.xlabel('swh (m)')
plt.title('Frequency of Occurance (mwp vs $swh$)')

plt.tight_layout()

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

plt.savefig('Plots/'+current_time + '.pdf')
'''
