#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Aug 18 12:21:51 2021

@author: goharshoukat

Script to create tables and graphs for weather-window analysis

bearing and magnitude functions needs to be put in a seperate file

these functions are used by more than one file

angles need to be reversed for the frequency of occurance tables

they need not be reversed just for the windrose plot because blowto command
allows the functionality to reverse the directions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes #edited version of the library. 
import matplotlib.cm as cm


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
df = pd.read_csv(direc + '08_25-08_36_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns = {'u10 (m s**-1)' : 'u10', 'v10 (m s**-1)' : 'v10'})
df['magnitude'] = np.sqrt(df['u10']**2 + df['v10']**2)

#creates an array of resultant array to be passed on to the bearing function
resultant_vector = np.array(df[{'u10', 'v10'}].values.tolist())
angle = bearing(resultant_vector)    
df['angle'] = angle
df.to_csv('results.csv')
bins = np.arange(0, np.max(df.magnitude), 2)
ax = WindroseAxes.from_ax()
#calculates the radius of the circle to be plotted
#circle1 = plt.Circle((0, 0), len(df[df['swh'] < 1])/22.5 / len(df) * 100,  transform=ax.transData._b, color='white', fill=True)

#bins for frequency can be adjusted. bins for angle are set at 22.5 deg each. apparently cant be adjusted. 

#function to reverse the direction
#as per documentattion, wind direction is blowing towards
#wave direction is blowing from
#for consistency, wind direction is reversed
#blowto command rotates by pi

bar = ax.bar(angle, df.magnitude,normed = True, bins = bins, blowto = True,
       opening=0.8,edgecolor='gray',lw=0.1, cmap = cm.Spectral_r, alpha = 1)

ax.set_thetagrids(range(0,360,45), [90, 45, 0, 315, 270, 225, 180, 135])
ax.set_theta_zero_location('W', offset=-180)
ax.set_xticklabels(['E', 'NE', 'N', 'NW',  'W', 'SW', 'S', 'SE'])
ax.set_legend(units = 'm/s', loc = (1,0), title = 'Wind Speed')