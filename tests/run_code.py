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
    must_haves = set(['mwp', 'swh', 'x'])
    if not all (must_haves) in set_k:
        print('Warning: Critical Variables are missing. The following variables are missing: {}\n'.format(must_haves - set_k))
        
    time.sleep(0.5)
    
    variable = input('Which parameter would you like to analyse: \n')

    cache= x.load_single_variable(variable)
    print('The range of Latitudnal values is: {} < Lat < {} \n'.format(x.lat[-1], x.lat[0]))
    print('The range of Longitudnal values is: {} < Lon < {} \n'.format(x.lon[0], x.lon[-1]))
    lat = float(input('Enter the Latitude: \n'))
    lon = float(input('Enter the Longitude: \n'))
    #lon = 45
    #lat = 80
    nearest = x.nearest_point(lat, lon)

    df, avail = x.extract_coordinate_data(nearest['latitude index'], nearest['longitude index'])
    if_save = input('Do you wish to save the data for your selected coordinate? \n')
    if if_save == 'yes':
            out_direc = input('Please provide directory to save the data \n')
            x.write_coordinate_data(df, out_direc)
            print('Successfully Saved \n\n')

    
    if avail != 100:
        #if availability of selected point is less than 100, user will be given an optino to select a new coordinate. 
        select_new_coord = input('Do you want to select a new coordinate because your previous selection had low availability?')
   
        if select_new_coord == 'yes': 
                lat = float(input('Enter the Latitude: \n'))
                lon = float(input('Enter the Longitude: \n'))
                nearest2 = x.nearest_point(lat, lon)
                df2, avail2 = x.extract_coordinate_data(nearest2['latitude index'], nearest2['longitude index'])
                 
                if_save = input('Do you wish to save the data for this coordinate? \n')
                if if_save == 'yes':
                    out_direc = input('Please provide directory to save the data \n')
                    x.write_coordinate_data(df2, out_direc)
                    print('Successfully Saved \n\n')
                    


        
    
    
    
    
    ''' 
    if_more_variables = input('Do you wish to include other variables within the output file?')
    if if_more_variables:
        pass
    '''
    
    
while True:
    run_script()
