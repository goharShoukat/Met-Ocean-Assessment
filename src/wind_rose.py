#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Aug 18 12:21:51 2021

@author: goharshoukat


script to create wind rose diagrams
the bins are hard coded
<5 is calm
>25
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windRose_wind import WindroseAxes #edited version of the library. 
import matplotlib.cm as cm
import matplotlib as mpl

def wind_rose(df, var_direction, variable, units, Coordinates, date_range, direc):
    #inputs
    #df : pd.DataFrame : the entire dataframe as it is passed through from the run_code script
    #var_direction: str : for wave roses, this is mwd
    #variable: str : input variable name like swh
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #units : pd.DataFrame : df of units with columns as variable names
    #direc : str : output directory entered by user
    
    
        
    bins = np.arange(5, 22, 1)

    ax = WindroseAxes.from_ax()
    #circle1 = plt.Circle((0, 0), 5,  transform=ax.transData._b, color='white', fill=True)
    ax.bar(df[var_direction].to_numpy(), df[variable].to_numpy(), bins = bins,normed = True, 
           opening=0.8,edgecolor='gray',lw=0.1)
    
    ax.set_thetagrids(range(0,360,45), [90, 45, 0, 315, 270, 225, 180, 135])
    ax.set_theta_zero_location('W', offset=-180)
    ax.set_xticklabels(['E', 'NE', 'N', 'NW',  'W', 'SW', 'S', 'SE'])
    #ax.add_patch(circle1)
    ax.set_rorigin(-1.5)
    t = plt.text(-1.5, -1.5, "Calm", size=12, ha="center", va="center", 
                 bbox=dict(boxstyle="circle", facecolor = 'white', 
                           edgecolor = 'white'))
    leg_title = (variable + '(' + units.loc[0, variable] + ')')
    #t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red'))
    ax.set_legend(title = leg_title, bbox_to_anchor = (1, 0.1))
    mpl.rcParams.update(mpl.rcParamsDefault)
    ax.set_title('{}\nWind Rose Diagram - {}'.format(Coordinates, date_range))
    plt.show()
    plt.savefig(direc + variable + ' wind rose.pdf')
    plt.close()

    
'''
def bearing(vector):
#function to calculate the bearing. takes in the resultant vector
#outputs the bearing
    
    #calculates the angle from the postive x axis counter clockwise. neg is clockwise
    return np.mod(180 + 180/np.pi * np.arctan2(vector[:, 1], vector[:,0]), 360)




direc = 'results/'
df = pd.read_csv(direc + '09_06-09_53_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns = {'u10 (m s**-1)' : 'u10', 'v10 (m s**-1)' : 'v10'})
df['magnitude'] = np.sqrt(df['u10']**2 + df['v10']**2)

#creates an array of resultant array to be passed on to the bearing function
resultant_vector = np.array(df[{'u10', 'v10'}].values.tolist())
angle = bearing(resultant_vector)    
df['angle'] = angle
df.to_csv('results1.csv')
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

bar = ax.bar(angle, df.magnitude,normed = True, bins = bins, blowto = False,
       opening=0.8,edgecolor='gray',lw=0.1, cmap = cm.Spectral_r, alpha = 1)

ax.set_thetagrids(range(0,360,45), [90, 45, 0, 315, 270, 225, 180, 135])
ax.set_theta_zero_location('W', offset=-180)
ax.set_xticklabels(['E', 'NE', 'N', 'NW',  'W', 'SW', 'S', 'SE'])
ax.set_legend(units = 'm/s', loc = (1,0), title = 'Wind Speed')
plt.show()

'''