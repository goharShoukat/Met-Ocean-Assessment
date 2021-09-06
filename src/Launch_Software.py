#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 20:24:27 2021

@author: goharshoukat

This script combinees both the time series extraction and the plotting
libraries. 

It only function with default settings. 

the plots are created if the units of the latitude and longitude are deg N and deg E. if the units are altered, additional selection statements are needed. 
we didnt have time or the data to explore additional feasibilities. 

On Windows OS, the file reading maybe changed. the method of reading file can affect the first file being read. it might be missed out. 

weather window analysis is yet to be completed

the date issue remains unresolved. a cache file is being used. its unelegent but works and does not occupy too much of space. it wouldnt hurt to let it be. 
"""
import os
import numpy as np
import pandas as pd
from run_code import run_script
from freq_occurence import frequency_occurence
from time_series import time_series_plot
from tables import tables_monthly_summary, tables_yearly_summary_first_20, tables_yearly_summary_last_20, tables_wind_monthly, tables_wind_yearly_first_20, tables_wind_yearly_last_20, tables_wind_yearly_lessthan_20, tables_yearly_summary_lessthan_20
from contour_plots import contours
from Wave_Rose import wave_rose
from EVA import EVA

from wind_vel_direction_calc import wind_calc #calculates wind speed and direction necessary for all other wind graphs



print('Welcome! This is a Preliminary Wind & Wave Resource Assessment Tool designed inhouse by GDG.\n\n\n')
print('Before proceeding, please choose from amongst the 3 different options available to you:\n\n')
print('1. Extract data for variables of choice at a specified location.\n')
print('2. Extract data for variables associated with waves at a specified choice and plot using default plotting settings. If you chose this option, please ensure that you include swh, mwp, mwd and hmax within your choice of variables.\n')
print('3. Extract data for variables associated with wind at a specified choice and plot using default plotting settings. If you chose this option, please ensure that you include u10 and v10 within your choice of variables.\n')
print('4. Extract wind and wave data for weather window analysis. (To be developed)')
option = (input('Select your option\n'))

if int(option) == 1:
    _ = run_script()

# %%
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

    
    print('\nWe will now perform computations to produce the following set of curves/tables/plots:\n1. Time Series Plots\n2. Frequency of Occurence Plots\n3. Summary Tables\n4. Wave Rose Diagrams\n5. Contour Plots\n6. Extreme Value Plots')
    
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
        elif (int(df2.loc[len(df2)-1, 'Date'].year) - int(df2.loc[0, 'Date'].year)) < 20:
            tables_yearly_summary_lessthan_20(df2, 'swh', 'mwp',
                                 'hmax', units, Coordinates, date_range, plot_direc) 
        else:
            pass
        #plot contours, gaussian kdes for swh vs mwp
        contours(df2, 'swh', 'mwp', units, Coordinates, date_range, plot_direc)
        
        #plot wave rose diagrams for swh
        wave_rose(df2, 'mwd', 'swh', units, Coordinates, date_range, plot_direc)
        
        #GEV Extreme Value Analysis
        EVA(df2, 'swh', Coordinates, date_range, plot_direc)
        EVA(df2, 'hmax', Coordinates, date_range, plot_direc)
        
    print('\nAll Plots were successfully generated and saved in the specified directory.')
   
    #permenantly removes cache file
    os.remove('cache.csv')
    
    
    
#%%
elif int(option) == 3:
    #option for wind data analysis
    df, variable, units = run_script()
    
    #getting an error in converting Date series to datetime. running a loop through it. come back when you have time
    #write the file first and then read it and then delete it. 
    #df['Date] is not getting converted to datetime. work on it later. possible solution is to rollback pandas to previous version. bug within the library
    df.to_csv('cache.csv', index = False)
    df2 = pd.read_csv('cache.csv', index_col = False)
    df2['Date'] = pd.to_datetime(df2['Date'])
    #lines 37 - 40 check if the 2 important wave variables are present in the data file
    must_var = set(['u10', 'v10'])
    if len(set(must_var - set(variable))) > 0:
        print('{} variable(s) are missing. Although the time series has been successfully saved, the default plotting algorithm will not be able to execute properly. For option - 3 to execute fully, please fulfill the conditions of the variables\n'.format(must_var - set(variable)))
    
    print('\nWe will now perform computations to produce the following set of curves/tables/plots:\n1. Time Series Plots\n2. Summary Tables\n3. Wind Rose Diagrams\n4. Extreme Value Plots')
    
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
        
        bearing, velocity = wind_calc(df) #wind velocity and angle obtained
        df2['Velocity'] =  velocity #need to assign to dataframe because thats how the plotting libraries take in the arguments
        df2['Bearing'] = bearing
        units['Velocity'] = units['u10'] #also need to create columns in the unit dataframe because the units also get transferred around in database and the variable name is the key
        units['Bearing'] = '$^\circ$'
        
        
        #plot time series for velocity and angle
        time_series_plot(df2, 'Velocity', Coordinates, units.loc[0, 'Velocity'], plot_direc)
        time_series_plot(df2, 'Bearing', Coordinates, units.loc[0, 'Bearing'], plot_direc)        
        
        #summary tables
        tables_wind_monthly(df2, 'Velocity', units, date_range, Coordinates, plot_direc)
        if (int(df2.loc[len(df2)-1, 'Date'].year) - int(df2.loc[0, 'Date'].year)) == 40:
        
            tables_wind_yearly_first_20(df2, 'Velocity', units, date_range, Coordinates, plot_direc)
            tables_wind_yearly_last_20(df2, 'Velocity', units, date_range, Coordinates, plot_direc)
        elif (int(df2.loc[len(df2)-1, 'Date'].year) - int(df2.loc[0, 'Date'].year)) < 20:
            tables_wind_yearly_lessthan_20(df2, 'Velocity', units, date_range, Coordinates, plot_direc)
        else:
            pass
        #Extreme Value analysis
        EVA(df2, 'Velocity', Coordinates, date_range, plot_direc)
    print('\nAll Plots were successfully generated and saved in the specified directory.')
   
    #permenantly removes cache file
    os.remove('cache.csv')
else:
    print('Acceptable inputs are: 1, 2 & 3. Please relaunch and try again. ')
