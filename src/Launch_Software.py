#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 20:24:27 2021

@author: goharshoukat

This script combinees both the time series extraction and the plotting
libraries. 

It only function with default settings. 


"""

import numpy as np
import pandas as pd
from run_code import run_script
from freq_occurence import frequency_occurence
from time_series import time_series_plot
from tables import tables_monthly_summary, tables_yearly_summary_first_20, tables_yearly_summary_last_20
import os

print('Welcome! This is a Preliminary Wind & Wave Resource Assessment Tool designed inhouse by GDG.\n\n\n')
print('Before proceeding, please choose from amongst the 3 different options available to you:\n\n')
print('1. Extract data for variables of choice at a specified location.\n')
print('2. Extract data for variables associated with waves at a specified choice and plot using default plotting settings. If you chose this option, please ensure that you include swh, mwp, mwd and hmax within your choice of variables.\n')
print('3. Extract data for variables associated with wind at a specified choice and plot using default plotting settings. If you chose this option, please ensure that you include u10 and v10 within your choice of variables.\n')

option = (input('Select your option\n'))

if int(option) == 1:
    _ = run_script()

elif int(option) == 2:
    #structure of the code changed t
    df, variable, units = run_script()
    
    #getting an error in converting Date series to datetime. running a loop through it. come back when you have time
    #write the file first and then read it and then delete it. 
    #df['Date] is not getting converted to datetime. work on it later. possible solution is to rollback pandas to previous version. bug within the library
    df.to_csv('cache.csv', index = False)
    df2 = pd.read_csv('cache.csv', index_col = False)
    df2['Date'] = pd.to_datetime(df2['Date'])
    #lines 37 - 40 check if the 3 important wave variables are present in the data file
    must_var = set(['swh', 'mwp', 'hmax', 'mwd'])
    if len(set(must_var - set(variable))) > 0:
        print('{} variable(s) are missing. Although the time series has been successfully saved, the default plotting algorithm will not be able to execute properly. For option - 2 to execute fully, please fulfill the conditions of the variables\n'.format(must_var - set(variable)))

    
    print('\nWe will now perform computations to produce the following set of curves/tables/plots:\n1. Time Series Plots\n2. Frequency of Occurence Plots\n3. Summary Tables\n4. Wave Rose Diagrams\n5. Contour Plots')
    
    plot_direc = input('Please be patient while the plots are generated. In the meanwhile, please provide the directory where you wish to save the plots.\n')
    if not os.path.isdir(plot_direc):
        os.makedirs(plot_direc)
    
    if (units.loc[0,'latitude'] == 'degrees_north') and (units.loc[0, 'longitude'] == 'degrees_east'): #check for units of longitude and latitude
           
        #we now calculate the location and the date range which 
        #will be used for the title of the plots
        Coordinates_lat = str(df.loc[0, 'latitude']) + '$ ^\circ$N'
        Coordinates_lon = str(df.loc[0, 'longitude'])+ '$ ^\circ$E'
        Coordinates = Coordinates_lat + ', ' + Coordinates_lon
        
        date_range = '({} - {})'.format(df2.loc[0,'Date'].strftime('%Y-%m-%d'), df2.loc[len(df)-1,'Date'].strftime('%Y-%m-%d'))
        
        #df2 needs to be passed just to time_series
        time_series_plot(df2, 'mwp', Coordinates, units.loc[0,'mwp'], plot_direc)
        time_series_plot(df2, 'swh', Coordinates, units.loc[0,'swh'], plot_direc)
        time_series_plot(df2, 'hmax', Coordinates, units.loc[0,'hmax'], plot_direc)
        
        #pass the normal df to all other functions
        #plot heatmap for frequency of occurrence for mwp vs swh
        frequency_occurence(df, 'mwp', 'swh', Coordinates, date_range, 'mwp vs swh', list([units.loc[0,'mwp'], units.loc[0,'swh']]), plot_direc)
    
        #form summary tables - monthly
        tables_monthly_summary(df2, 'swh', 'mwp', 'hmax', units, Coordinates, date_range, plot_direc)
        #yearly summary tables - first 20 years and then the next 20 years
        #first check number of years. if greater than 20, divide into 2 blocks
        
        if (int(df2.loc[len(df2)-1, 'Date'].year) - int(df2.loc[0, 'Date'].year)) == 40:
            #we will assume a 40 year duration
            
            tables_yearly_summary_first_20(df2, 'swh', 'mwp',
                                  'hmax', units, Coordinates, date_range, plot_direc)
   
            tables_yearly_summary_last_20(df2, 'swh', 'mwp',
                                 'hmax', units, Coordinates, date_range, plot_direc)
   
    print('\nAll Plots were successfully generated and saved in the specified directory.')
   
    #permenantly removes cache file
    os.remove('cache.csv')
elif int(option) == 3:
    
    pass

else:
    print('Acceptable inputs are: 1, 2 & 3. Please relaunch and try again. ')
