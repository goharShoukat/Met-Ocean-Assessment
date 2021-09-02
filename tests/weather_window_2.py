#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 14:00:00 2021

@author: goharshoukat
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.font_manager import FontProperties


direc = 'tests/results/'
df = pd.read_csv(direc + '08_26-09_01_PM.csv', index_col = False)
df = df.rename(columns = {'swh (m)' : 'swh', 'Date' : 'Start Date'})
df = df.rename(columns = {'u10 (m s**-1)' : 'u10', 'v10 (m s**-1)' : 'v10'})
df['Start Date'] = pd.to_datetime(df["Start Date"])
df['magnitude'] = np.sqrt(df['u10']**2 + df['v10']**2)

month_df = df[df['Start Date'].dt.month==7].reset_index(drop=True)
swh_limit = 3.5
vel_limit = 20
columns = ['>= Period (h)', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
                                  'Oct', 'Nov', 'Dec', 'Year']
results = pd.DataFrame(columns = columns, dtype = float)
results['>= Period (h)'] = [3, 6, 12, 24, 48, 72]


#codntion should be with or condition. otherwise, nan comes because both 
#conditions ahve to be met for a False which isnt always the case. when any
# of the two conditions become invalid, a false should be registered. 
#For true however, both conditions should be met
month_df.loc[(month_df['swh'] <= swh_limit) & (month_df['magnitude'] <= vel_limit), 'bool'] = True
month_df.loc[(month_df['swh'] > swh_limit) | (month_df['magnitude'] > vel_limit), 'bool'] = False 
month_df = month_df.drop(['latitude (degrees_north)', 'longitude (degrees_east)', 'u10', 'v10', 'magnitude', 'swh'], axis = 1)

v = np.array(month_df['bool'])

#two methods for identifying when the boolean changes from true to false and vice versa
#this method is deprecated and hence error prone. however, for future reference, 
#can be interesting
#x = np.where(v[:-1] != (v[1:]))

#gives us the index everytime boolean changes
#one has to be added to i and subtracted from i+1
y = np.where(np.diff(v))[0]
new_df = month_df.loc[y] #queries the original dataframe to extract only relevent indices where the conditions are met
#create another column with the end date
#first reset the indices 

#check for the first element in the month_df if it is true
#add all the elements to new_df from the beginning which are true
#repeat for elements towards the end
if month_df['bool'][0] == True:
    idx_top = (month_df[month_df['bool'] == False]['bool']).index[0]
    #concactenate the new values. 
    new_df = pd.concat([month_df.loc[0:idx_top], new_df])
    
#repeat above for bottom of month_df
if month_df['bool'][month_df.index[-1]] == True:
    idx_end = (month_df[month_df['bool'] == False]['bool']).index[-1]
    #concactenate the new values. 
    new_df = new_df.append(month_df.loc[(idx_end+1):])
    

new_df = new_df.reset_index()

new_df.insert(2, 'End Date', None)#specifies location for adding the end date column
new_df.loc[0:(len(new_df)-2), 'End Date'] = new_df['Start Date'][1:].reset_index(drop = True)

new_df['End Date'] = pd.to_datetime(new_df["End Date"])
#calculate the difference between each element 
#these are hourly calculations
new_df.insert(3, 'Duration', (new_df['End Date'] - new_df['Start Date']).astype('timedelta64[h]'))

#when binning monthly, there is a cell when the year changes. 
#this means that the duration will always be around a year's difference
#we first identify where the year changes, then make that cell none
#np.where identifies where the year changes
#with loc, we alter the cell value

new_df.loc[np.where((new_df['End Date'].dt.year - new_df['Start Date'].dt.year) >= 1)[0], 'Duration'] = None

#convert the added values at the top and at the bottom 
#locate where the nan values are. this will serve as the 
nan_idx_top = np.where(new_df['Duration'][:idx_top].isnull().values)[0]

#above operation is not possible for the values at the end because the 
#index was reset. we first locate the previous index 
new_idx_bottom = (new_df[new_df['index'] == idx_end]).index[0]
nan_idx_bott = np.where(new_df['Duration'][(new_idx_bottom + 1):].isnull().values)[0]

#for loop to readjust the final dataframe with all the information about durations etc
#create new dataframe with the final array with durations
index_df2 = np.arange(0, len(y) + len(nan_idx_top) + len(nan_idx_bott)+1, 1)
df2 = pd.DataFrame(columns = ['Start Date', 'End Date', 'Duration'], index = index_df2)
for idx, i in zip(nan_idx_top, range(len(nan_idx_top))):
    if idx == nan_idx_top[0]:
        df2.loc[0]['Start Date'] = new_df.loc[0]['Start Date']
        df2.loc[0]['End Date'] = new_df.loc[idx-1]['End Date']
        df2.loc[0]['Duration'] = new_df['Duration'][0:idx].sum(axis = 0)
    else:
        df2.loc[i]['Start Date'] = new_df.loc[idx]['Start Date']
        df2.loc[i]['End Date'] = new_df.loc[idx + 1]['End Date']
        #df2.loc[i]['Duration'] = new_df.loc[idx]['Start Date']
        
        



for i in results['>= Period (h)']:
    x = (new_df[new_df['Duration'] >= 3])['Duration'].sum(axis = 0)/(len(month_df)) * 100
    results.loc[results['>= Period (h)'] == 3, 'Jan'] = x
#calculate the percentages for when the values are greater than each 
#of the durations specified by the period column of results
