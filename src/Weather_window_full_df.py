#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 11:44:34 2021

@author: goharshoukat
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 20:24:46 2021
@author: goharshoukat
Script for weather window analysis
Use logical operators to filter array
Extract indices for where element switches from true to false or vice versa
Use those indices to extract windows
remove the bearing and magnitude calculation from this file when automating. 
dump wind calculation functions into another file
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


def bearing(vector):
#function to calculate the bearing. takes in the resultant vector
#outputs the bearing
    
    #calculates the angle from the postive x axis counter clockwise. neg is clockwise
    ang = np.rad2deg(np.arctan2(vector[:, 1], vector[:,0]))
    ang[ang < 0] = abs(ang[ang < 0]) + 90 #iii and iv the quadrants are covered
    
    #i and ii need to be treated seperately
    ang[(ang > 0) & (ang < 90)] = 90 - ang[(ang > 0) & (ang < 90)] #i quadrant
    ang[(ang > 90) & (ang < 180)] = 360 - (ang[(ang > 90) & (ang < 180)] - 90) #i quadrant
    ang[(ang==90)] = 0
    ang[(ang==180)] = 270
    return ang


direc = 'tests/results/'
df = pd.read_csv(direc + '08_25-08_27_PM.csv', index_col = False)
df = df.rename(columns = {'swh (m)' : 'swh', 'Date' : 'Start Date'})
df = df.rename(columns = {'u10 (m s**-1)' : 'u10', 'v10 (m s**-1)' : 'v10'})
df['Start Date'] = pd.to_datetime(df["Start Date"])
df['magnitude'] = np.sqrt(df['u10']**2 + df['v10']**2)

#creates an array of resultant array to be passed on to the bearing function
resultant_vector = np.array(df[{'u10', 'v10'}].values.tolist())
angle = bearing(resultant_vector)    
df['angle'] = angle

#implement filtering
swh_limit = 1.5
vel_limit = 5


#codntion should be with or condition. otherwise, nan comes because both 
#conditions ahve to be met for a False which isnt always the case. when any
# of the two conditions become invalid, a false should be registered. 
#For true however, both conditions should be met
df.loc[(df['swh'] <= swh_limit) & (df['magnitude'] <= vel_limit), 'bool'] = True
df.loc[(df['swh'] > swh_limit) | (df['magnitude'] > vel_limit), 'bool'] = False 


v = np.array(df['bool'])

#two methods for identifying when the boolean changes from true to false and vice versa
#this method is deprecated and hence error prone. however, for future reference, 
#can be interesting
#x = np.where(v[:-1] != (v[1:]))

#gives us the index everytime boolean changes
#one has to be added to i and subtracted from i+1
y = np.where(np.diff(v))[0]
new_df = df.loc[y] #queries the original dataframe to extract only relevent indices where the conditions are met
#create another column with the end date
#first reset the indices 
new_df = new_df.reset_index(drop = True)

new_df.insert(1, 'End Date', '')#specifies location for adding the end date column
new_df.loc[0:(len(new_df)-2), 'End Date'] = new_df['Start Date'][1:].reset_index(drop = True)
new_df['End Date'] = pd.to_datetime(new_df["End Date"])
#calculate the difference between each element 
new_df.insert(2, 'Duration', (new_df['End Date'] - new_df['Start Date']).astype('timedelta64[h]'))