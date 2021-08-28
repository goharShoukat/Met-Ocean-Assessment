#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 23:01:52 2021

@author: goharshoukat

Script for making graphs from weather window analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



#create a list of velocities
velocity = [2, 4, 6, 8, 9, 10, 11, 12, 15, 20, 25]
swh = [1.5, 2, 2.5, 3.5]
months = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
                                  'Oct', 'Nov', 'Dec']
months_int = np.linspace(1, 12, 12).astype(int)

direc = 'tests/results/'
df = pd.read_csv(direc + '08_26-09_01_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df["Date"])
df = df.rename(columns = {'Date' : 'Start Date', 'swh (m)' : 'swh', 'u10 (m s**-1)' : 'u10', 
                          'v10 (m s**-1)' : 'v10'})
df['magnitude'] = np.sqrt(df['u10']**2 + df['v10']**2)

#create a dataframe where the results for the graph will be compiled
#columns are different velocities
#index are months
results = pd.DataFrame(columns=vel, index = months)

month_df = df[df['Start Date'].dt.month==1].reset_index(drop=True)
array = []
for vel in velocity:
        
        
    #codntion should be with or condition. otherwise, nan comes because both 
    #conditions ahve to be met for a False which isnt always the case. when any
    # of the two conditions become invalid, a false should be registered. 
    #For true however, both conditions should be met
    
    #filter month_df to extract relevent information
    month_df.loc[(month_df['swh'] <= 1.5) & (month_df['magnitude'] <= vel), 'bool'] = True
    month_df.loc[(month_df['swh'] > 1.5) | (month_df['magnitude'] > vel), 'bool'] = False 
    v = np.array(month_df['bool'])
    y = np.where(np.diff(v))[0]
    new_df = month_df.loc[y] #queries the original dataframe to extract only relevent indices where the conditions are met
    #create another column with the end date
    #first reset the indices 
    new_df = new_df.reset_index(drop = True)
    
    new_df.insert(1, 'End Date', None)#specifies location for adding the end date column
    new_df.loc[0:(len(new_df)-2), 'End Date'] = new_df['Start Date'][1:].reset_index(drop = True)
    new_df['End Date'] = pd.to_datetime(new_df["End Date"])
    #calculate the difference between each element 
    #these are hossurly calculations
    new_df.insert(2, 'Duration', (new_df['End Date'] - new_df['Start Date']).astype('timedelta64[h]'))
    
    #when binning monthly, there is a cell when the year changes. 
    #this means that the duration will always be around a year's difference
    #we first identify where the year changes, then make that cell none
    #np.where identifies where the year changes
    #with loc, we alter the cell value
    new_df.loc[np.where((new_df['End Date'].dt.year - new_df['Start Date'].dt.year) >= 1)[0], 'Duration'] = None
    
    #searches the new_df where duration exceeds 24 hours
    results.loc['Jan', vel] =  new_df[new_df['Duration'] >= 24]['Duration'].sum(axis = 0) / len(new_df) * 100

