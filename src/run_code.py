#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 18:40:57 2021

@author: goharshoukat
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from netCDF4 import Dataset, num2date
import time
import sys
sys.path.append('/Users/goharshoukat/Documents/GitHub/Met-Ocean-Assessment/src/')
from ERA5 import ERA5

def run_script():
    directory = input('Enter the directory of the data folder: \n')
    #directory = '/Users/goharshoukat/Documents/GitHub/Met-Ocean-Assessment/some_data/'
    #files = np.sort(os.listdir(directory)[1:])
    x = ERA5(directory)
    k = list(x.f.variables.keys())
    print('List of variables stored within the data files is: {} \n'.format(k[:]))
    #provide warning for missing data variables
    set_k = set(k)
    must_haves = set(['mwp', 'swh', 'pp1d'])
    if not all (must_haves) in set_k:
        print('Warning: Critical Variables are missing. The following variables are missing: {}\n'.format(must_haves - set_k))
        
    time.sleep(0.5)
    

    variable = np.array(input('Please enter the variable(s) you want to extract \n').split())
    
    #need to pass on at least one of the variables from the file so that the class can extract
    #latitude longitude values
    
    cache = x.load_variable(variable)
    
    print('The range of Latitudnal values is: {} < Lat < {} \n'.format(x.lat[-1], x.lat[0]))
    print('The range of Longitudnal values is: {} < Lon < {} \n'.format(x.lon[0], x.lon[-1]))
    lat = float(input('Enter the Latitude: \n'))
    lon = float(input('Enter the Longitude: \n'))

    #confirms the nearest point
    nearest = x.nearest_point(lat, lon)
    
    df, avail = x.df_generator(variable)

        
    if_save = input('Do you wish to save the data for your selected coordinate? \n')
    if if_save == 'yes':
            out_direc = input('Please provide directory to save the data \n')
            x.write_coordinate_data(df, variable, out_direc)
            print('Successfully Saved \n\n')
            return df, variable, cache["Units"]

    if not all(i == 100 for i in avail):
        #if availability of selected point is less than 100, user will be given an optino to select a new coordinate. 
        select_new_coord = input('Do you want to select a new coordinate because your previous selection had low availability?')
   
        if select_new_coord == 'yes': 
                lat = float(input('Enter the Latitude: \n'))
                lon = float(input('Enter the Longitude: \n'))
                nearest2 = x.nearest_point(lat, lon)
                df2, avail2 = x.df_generator(variable)
                
                 
                if_save = input('Do you wish to save the data for this coordinate? \n')
                if if_save == 'yes':
                    out_direc = input('Please provide directory to save the data \n')
                    x.write_coordinate_data(df2, variable, out_direc)
                    print('Successfully Saved \n\n')
                    return df2, variable, cache["Units"]
                    

    
#x = run_script()
