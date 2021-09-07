#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 18:50:29 2021

@author: goharshoukat

script to generate wave rose diagrams with edited source codes for windrose library 
to generate customised labels and have a calm circle in the middle

this script uses windRose_waves.py as the source code. its a modified version for waves-swh only
"""


from windRose_waves import WindroseAxes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.ticker import MaxNLocator, MultipleLocator
import cartopy as ct
from matplotlib.font_manager import FontProperties
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap


def wave_rose(df, var_direction, variable, units, Coordinates, date_range, direc):
    #inputs
    #df : pd.DataFrame : the entire dataframe as it is passed through from the run_code script
    #var_direction: str : for wave roses, this is mwd
    #variable: str : input variable name like swh
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #units : pd.DataFrame : df of units with columns as variable names
    #direc : str : output directory entered by user
    
        
    bins = np.arange(1, 6, 1)
    bins = np.append(bins, 6)
    ax = WindroseAxes.from_ax()
    #cmap can be adjusted. default is also good. 
    ax.bar(df[var_direction].to_numpy(), df[variable].to_numpy(), bins = bins,normed = True, 
           opening=0.8,edgecolor='gray',lw=0.1, cmap = cm.Spectral_r)
    
    ax.set_thetagrids(range(0,360,45), [90, 45, 0, 315, 270, 225, 180, 135])
    ax.set_theta_zero_location('W', offset=-180)
    ax.set_xticklabels(['E', 'NE', 'N', 'NW',  'W', 'SW', 'S', 'SE'])
    #ax.add_patch(circle1)
    ax.set_rorigin(-2)
    t = plt.text(-2., -2., "Calm", size=9, ha="center", va="center",
                 bbox=dict(boxstyle="circle", facecolor = 'white', 
                           edgecolor = 'white'))
    leg_title = (variable + '(' + units.loc[0, variable] + ')')
    #t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red'))
    ax.set_legend(title = leg_title, bbox_to_anchor = (1, 0.1))
    ax.set_title('{}\nWave Rose Diagram - {}'.format(Coordinates, date_range))
    plt.show()
    plt.savefig(direc + variable + ' wave rose.pdf')
    plt.close()
    
    
def monthly_wave_rose(df, var_direction, variable, units, Coordinates, date_range, direc):
    #function to generate montly wave roses
    #inputs
    #df : pd.DataFrame : the entire dataframe as it is passed through from the run_code script
    #var_direction: str : for wave roses, this is mwd
    #variable: str : input variable name like swh
    #Coordinates : str : The coordinates for which this data is extracted
    #date_range : str : The date interval for which this data corresponds to
    #units : pd.DataFrame : df of units with columns as variable names
    #direc : str : output directory entered by user
    
    bins = np.arange(1, 6, 1)
    bins = np.append(bins, 6)
    
    
    #declare an array of int to to specify the months
    months = np.linspace(1,12,12).astype(int) #for data filtering using datetime
    #specify month names to be put in the title
    columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
                                  'Oct', 'Nov', 'Dec']

    #loop to extract monthly dataframes and plot them, save them
    for m, col in zip(months, columns):
        month_df = df[df['Date'].dt.month==m].reset_index(drop=True)
        
        
        ax = WindroseAxes.from_ax()
        ax.bar( month_df[var_direction].to_numpy(),  month_df[variable].to_numpy(), bins = bins,normed = True, 
           opening=0.8,edgecolor='gray',lw=0.1, cmap = cm.Spectral_r)
    
        ax.set_thetagrids(range(0,360,45), [90, 45, 0, 315, 270, 225, 180, 135])
        ax.set_theta_zero_location('W', offset=-180)
        ax.set_xticklabels(['E', 'NE', 'N', 'NW',  'W', 'SW', 'S', 'SE'])
        #ax.add_patch(circle1)
        ax.set_rorigin(-2)
        t = plt.text(-2., -2., "Calm", size=9, ha="center", va="center",
                     bbox=dict(boxstyle="circle", facecolor = 'white', 
                               edgecolor = 'white'))
        leg_title = (variable + '(' + units.loc[0, variable] + ')')
        #t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red'))
        ax.set_legend(title = leg_title, bbox_to_anchor = (1, 0.1))
        ax.set_title('{}\n{} Wave Rose Diagram - {}'.format(Coordinates, col, date_range))
        plt.show()
        plt.savefig(direc + variable +' ' + col + '_' + ' wave rose.pdf')
        plt.close()
       
#direc = 'tests/results/'
#df = pd.read_csv(direc + '07_23-12_57_PM.csv', index_col = False)
#df['Date'] = pd.to_datetime(df['Date'])
#df = df.rename(columns = {'swh (m)':'swh', 'mwd (Degree true)':'mwd'})


'''
bins = np.arange(1, 6, 1)
bins = np.append(bins, 6)
ax = WindroseAxes.from_ax()
#circle1 = plt.Circle((0, 0), 5,  transform=ax.transData._b, color='white', fill=True)
ax.bar(df.mwd.to_numpy(), df.swh.to_numpy(), bins = bins,normed = True, 
       opening=0.8,edgecolor='gray',lw=0.1)

ax.set_thetagrids(range(0,360,45), [90, 45, 0, 315, 270, 225, 180, 135])
ax.set_theta_zero_location('W', offset=-180)
ax.set_xticklabels(['E', 'NE', 'N', 'NW',  'W', 'SW', 'S', 'SE'])
#ax.add_patch(circle1)
ax.set_rorigin(-2)
t = plt.text(-2., -2., "Calm", size=9, ha="center", va="center", bbox=dict(boxstyle="circle", facecolor = 'white') )
#t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red'))
ax.set_legend(title = 'swh (m)', bbox_to_anchor = (1, 0.1))
ax.set_title('try')
plt.show()
'''