#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 20:24:46 2021

@author: goharshoukat

Script for weather window analysis, creates only tables. graphs in another sccript

Use logical operators to filter array

Extract indices for where element switches from true to false or vice versa

Use those indices to extract windows

remove the bearing and magnitude calculation from this file when automating. 
dump wind calculation functions into another file

when automating the script, run the entire code from filteration of monthly values to the end in a loop 12 times

Implement a detla time calculation to confirm hourly data


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

month_df = df[df['Start Date'].dt.month==1].reset_index(drop=True)
swh_limit = 3.5
vel_limit = 20
columns = ['>= Period (h)', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
                                  'Oct', 'Nov', 'Dec', 'Year']
results = pd.DataFrame(columns = columns, dtype = float)
results['>= Period (h)'] = [3, 6, 12, 24, 48, 72]


#13th month is not month
#it is added to provide iteration for the year
months = np.linspace(1,13,13).astype(int) #for data filtering using datetime

#dataframe with the compiled results which will be published
columns = ['>= Period (h)', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
                                  'Oct', 'Nov', 'Dec', 'Year']
results = pd.DataFrame(columns = columns, dtype = float)
results['>= Period (h)'] = [3, 6, 12, 24, 48, 72]

for m, col in zip(months, columns[1:]):
    if m == 13:
        month_df = df
    else:    
        month_df = df[df['Start Date'].dt.month==m].reset_index(drop=True)
         
        
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
    #new_df is the dataframe is the df which will at the end house all the 
    #dates for which the condition are met
    #in the first step, we will just assign values where the boolean flips
    new_df = month_df.loc[y] #queries the original dataframe to extract only relevent indices where the conditions are met
    #create another column with the end date
    #first reset the indices 
    
    #check for the first element in the month_df if it is true
    #add all the elements to new_df from the beginning which are true
    #repeat for elements towards the end
    if month_df['bool'][0] == True:
        idx_top = (month_df[month_df['bool'] == False]['bool']).index[0]
        #concactenate the new values. 
        new_df = pd.concat([month_df.loc[0:idx_top - 2], new_df])
        
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
    if month_df['bool'][0] == True:
        nan_idx_top = np.where(new_df['Duration'][:idx_top].isnull().values)[0]
    
    #above operation is not possible for the values at the end because the 
    #index was reset. we first locate the previous index
    
    
    #the first part of the equation only gives the indices from the starting index, 
    #which in this case is not 0. we add the length of the new_df to this to make it readjust to the current index
    
    #important to delete the final nan as that is only due to the fact
    #that the dataframe ends. hence the value is deleted. important to calculate
    #bott_df down below
    
    if month_df['bool'][month_df.index[-1]] == True: 
        new_idx_bottom = (new_df[new_df['index'] == idx_end]).index[0]
        nan_idx_bott = np.where(new_df['Duration'][(new_idx_bottom + 1):].isnull().values)[0] + new_idx_bottom
        if (len(new_df) - 1) in nan_idx_bott:
            nan_idx_bott = nan_idx_bott[:-1]
    
    
    #for loop to readjust the final dataframe with all the information about durations etc
    #create new dataframe with the final array with durations
                                                        #index_df2 = np.arange(0, len(y) + len(nan_idx_top) + len(nan_idx_bott)+1, 1)
    #df2 is the final dataframe which houses the exact start and end dates along with the duration only
    df2 = pd.DataFrame(columns = ['Start Date', 'End Date', 'Duration'])
    if month_df['bool'][0] == True:
        df2 = pd.DataFrame(columns = ['Start Date', 'End Date', 'Duration'], index = np.arange(0, len(nan_idx_top), 1))
        
        for idx, i in zip(nan_idx_top, range(len(nan_idx_top))):
            if idx == nan_idx_top[0]:
                df2.loc[0]['Start Date'] = new_df.loc[0]['Start Date']
                df2.loc[0]['End Date'] = new_df.loc[idx-1]['End Date']
                #df2.loc[0]['Duration'] = new_df['Duration'][0:idx].sum(axis = 0)
            elif i < len(nan_idx_top)-1:
                df2.loc[i]['Start Date'] = new_df.loc[idx+1]['Start Date']
                df2.loc[i]['End Date'] = new_df.loc[nan_idx_top[i+1]]['Start Date']
                #df2.loc[i]['Duration'] = new_df.loc[idx]['Start Date']
            else:
                df2.loc[i]['Start Date'] = new_df.loc[idx+1]['Start Date']
                df2.loc[i]['End Date'] = new_df.loc[y[0]]['Start Date']
        
        #insert the values from the flipping true false part of the new_df into df2
    
    if  (month_df['bool'][0] == True) or (month_df['bool'][month_df.index[-1]] == True):    
        df2 = df2.append(new_df[y[0]:(y[0] + len(y))], ignore_index = True).drop(['bool','index'], axis = 1)
    
    #perform the oepration with nan_idx_bott the same way it was done for nan_idx_top
    #craete a new dataframe and then append it to df2. creating a seperate frame 
    #because the index will have to be predefined in df2 which adds unnecessary complexity
    if month_df['bool'][month_df.index[-1]] == True:
        bott_df = pd.DataFrame(columns = ['Start Date', 'End Date'], index = np.arange(0, len(nan_idx_bott), 1))
        for idx, i in zip(nan_idx_bott, range(len(nan_idx_bott))):
            if i == 0:
                #gives us the starting point for the bottom remaining celss
                bott_df.loc[i]['Start Date'] = new_df.loc[new_idx_bottom+1]['Start Date']
                bott_df.loc[i]['End Date'] = new_df.loc[idx-1]['Start Date']
            elif i < len(nan_idx_bott)-1:
                bott_df.loc[i]['Start Date'] = new_df.loc[idx+1]['Start Date']
                bott_df.loc[i]['End Date'] = new_df.loc[nan_idx_bott[i+1]]['Start Date']
                #df2.loc[i]['Duration'] = new_df.loc[idx]['Start Date']
            else:
                bott_df.loc[i]['Start Date'] = new_df.loc[idx+1]['Start Date']
                bott_df.loc[i]['End Date'] = new_df.loc[len(new_df) - 1]['Start Date']
                
        df2 = df2.append(bott_df, ignore_index = True)
        df2['Duration'] = (df2['End Date'] - df2['Start Date']).astype('timedelta64[h]')
        df2.loc[np.where((pd.to_datetime(df2['End Date']).dt.year - pd.to_datetime(df2['Start Date']).dt.year) >= 1)[0], 'Duration'] = None
    

        
    
    for i in results['>= Period (h)']:
        if  (month_df['bool'][0] == True) or (month_df['bool'][month_df.index[-1]] == True):    
            x = (df2[df2['Duration'] >= i])['Duration'].sum(axis = 0)/len(month_df) * 100
            results.loc[results['>= Period (h)'] == i, m] = x
        else:
            x = (new_df[new_df['Duration'] >= 3])['Duration'].sum(axis = 0)/len(month_df) * 100
            results.loc[results['>= Period (h)'] == i, m] = x
    #calculate the percentages for when the values are greater than each 
    #of the durations specified by the period column of results

    #plotting the table
results = round(results, 1).astype(float) #np.round and df.round were rounding off to ceiling
col_width = [.1] * 13
col_width.insert(0, 0.2)
fig, ax = plt.subplots(1,1, figsize=(30,30))
tab = ax.table(cellText = results.values, colLabels = results.columns, 
          loc = 'center', cellLoc='center', colWidths = col_width)
plt.axis('off')
plt.tight_layout()
plt.rcParams['axes.titley'] = .65   # y is in axes-relative coordinates.
ax.set_title('rcParam y')
ax.set_title('Wind & Wave Persistance (%) \n$H_s$ <= {} m, V <= {}'.format(swh_limit, vel_limit))
for (row, col), cell in tab.get_celld().items():
  if (row == 0) or (col == -1):
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))

plt.savefig('Plots/weather_window_table_H{}_V{}.pdf'.format(swh_limit, vel_limit))



